from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "NousResearch/Llama-3-8B-Instruct-GPTQ"

tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
