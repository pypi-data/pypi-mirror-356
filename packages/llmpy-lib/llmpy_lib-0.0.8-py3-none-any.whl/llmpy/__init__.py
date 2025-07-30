from .llmpy import LLM
from llmpy_models import Model, Provider, model_to_provider

_llm = LLM()

def ask(model, question):
    return _llm.ask(model, question)


def ask_many(models, question):
    return _llm.ask_many(models, question)

__all__ = ['ask', 'ask_many', 'Model', 'Provider']