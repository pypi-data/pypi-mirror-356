Supported large language models:
the one hosted on groq

The rest is to come:
- anthropic (claude...)
- deepseek (deepseek-70b...)
- google (gemini...)
- meta (llama3.1-7b...)
- openai (gpt3.5...)
- qwen (34b...)


Usage example:

```python
import llmpy as lm

question = 'how many r\'s in strawberry'

model = Model.LLAMA_3_3_70B
models = [
    Model.LLAMA_3_3_70B,
    Model.Deepseek
]

lm.ask(model, question)
lm.ask_many(models, question)
```