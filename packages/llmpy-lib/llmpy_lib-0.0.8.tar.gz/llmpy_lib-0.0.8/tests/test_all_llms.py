import llmpy as lm
from llmpy_models import Model, Provider, model_to_provider
import time

def test_all_llms():
    llm = lm.LLM()
    
    # get all models by provider
    provider_models = {provider: [] for provider in Provider}
    for model in Model:
        provider = model_to_provider[model]
        provider_models[provider].append(model)
    
    total_models = sum(len(models) for models in provider_models.values())
    print(f"testing {total_models} models across {len(provider_models)} providers")
    
    success_count = 0
    
    for provider in provider_models:
        models = provider_models[provider]
        print(f"\n=== {provider.name}: {len(models)} models ===")
        
        for i, model in enumerate(models, 1):
            print(f"[{i}/{len(models)}] {model.name}...", end=" ")
            
            try:
                response = llm.ask(model, "what is the capital of france?")
                
                # basic validation
                if isinstance(response, str) and len(response) > 5 and "paris" in response.lower():
                    print("✓")
                    success_count += 1
                else:
                    print(f"✗ invalid response: {response[:50]}...")
                    
            except Exception as e:
                print(f"✗ error: {type(e).__name__}")
                
            time.sleep(0.1)  # rate limiting
    
    print(f"\nresults: {success_count}/{total_models} models passed")

if __name__ == "__main__":
    test_all_llms()