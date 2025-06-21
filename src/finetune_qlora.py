from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training

# Modelo escolhido
model_name = "NousResearch/Llama-3.2-1B"

# Carrega o tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
# Corrige o problema de padding
tokenizer.pad_token = tokenizer.eos_token

# Carrega o modelo em CPU, sem quantização
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map={"": "cpu"},
    torch_dtype=torch.float32
)

# Prepara o modelo para LoRA (sem kbit porque estamos no CPU puro)
model = prepare_model_for_kbit_training(model)

# Configuração do LoRA
lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05
)

model = get_peft_model(model, lora_config)

# Carrega o dataset anotado (no formato JSONL)
dataset = load_dataset("json", data_files="data/annotated.jsonl", split="train")

# Tokenização com batched=True (corrigido)
def tokenize_function(examples):
    texts = [
        prompt + "\nResposta:\n" + response
        for prompt, response in zip(examples['prompt'], examples['response'])
    ]
    return tokenizer(
        texts,
        truncation=True,
        padding="max_length",
        max_length=512
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

# Collator de dados padrão para causal LM
data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

# Argumentos de treinamento (tudo CPU)
training_args = TrainingArguments(
    output_dir="./llama3-ner-finetuned",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_steps=20,
    fp16=False,
    optim="adamw_torch",
    report_to="none"
)

# Cria o Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    data_collator=data_collator
)

# Inicia o fine-tuning
trainer.train()

# Salva o modelo final
trainer.save_model("./Llama-3.2-1B-finetuned")
