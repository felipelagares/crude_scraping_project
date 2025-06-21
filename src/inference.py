from transformers import AutoTokenizer, AutoModelForCausalLM

model_name = "./llama3-ner-finetuned"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype="auto")

model.eval()

prompt = "Extraia as entidades nomeadas do seguinte texto: 'O presidente Luiz Inácio Lula da Silva visitou a Petrobras no Rio de Janeiro.'"

inputs = tokenizer(prompt, return_tensors="pt").to("cuda")
outputs = model.generate(**inputs, max_new_tokens=100)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
