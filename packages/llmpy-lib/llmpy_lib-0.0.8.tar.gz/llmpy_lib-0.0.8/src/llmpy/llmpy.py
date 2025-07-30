from anthropic import Anthropic
from dotenv import load_dotenv
from enum import Enum, auto
from google import genai
from groq import Groq
from llmpy_models import Model, Provider, model_to_provider
from openai import OpenAI
import os

class LLM:
    def __init__(self):
        load_dotenv()
        self.clients = {}
        self.handlers = {
            Provider.ANTHROPIC : self._ask_anthropic,
            Provider.GOOGLE : self._ask_google,
            Provider.GROQ : self._ask_groq,
            Provider.OPENAI : self._ask_openai,
        }

    def _init_client(self, provider):
        match provider:
            case Provider.ANTHROPIC:
                return Anthropic(api_key=os.environ.get('ANTHROPIC_KEY')) # Anthropic
            case Provider.GOOGLE:
                return genai.Client(api_key=os.environ.get('GOOGLE_KEY')) # Google
            case Provider.GROQ:
                return Groq(api_key=os.environ.get('GROQ_KEY'))           # Groq
            case Provider.OPENAI:
                return OpenAI(api_key=os.environ.get('OPENAI_KEY'))       # OpenAI


    def _load_models(self, *models):
        # init connection
        for model in models:
            # check in map of models if maker already present, which means that client was already loaded and skip
            provider = model_to_provider[model]
            if provider not in self.clients:
                self.clients[provider] = self._init_client(provider)


    def _ask_anthropic(self, client, model, question):
        response = client.messages.create(
            model=model.value,
            max_tokens=1024,
            messages=[
                {'role': 'user', 'content': question}
            ]
        )
        return response.content[0].text

    def _ask_google(self, client, model, question):
        return client.models.generate_content(
            model=model.value,
            contents=question,
        ).text

    def _ask_groq(self, client, model, question):
        # groq
        return client.chat.completions.create(
            messages=[
                {'role': 'user', 'content': question,}
            ],
            model=model.value,
        ).choices[0].message.content
    
    def _ask_openai(self, client, model, question):
        return client.responses.create(
            model = model.value,
            input = question,
        ).output_text

    def ask(self, model, question):
        self._load_models(model)
        provider = model_to_provider[model]
        client = self.clients[provider]
        return self.handlers[provider](client, model, question)
    
    def ask_many(self, models, question):
        self._load_models(models)
        results = {}
        for model in models:
            results[model] = self.ask(model, question)
        return results
            
