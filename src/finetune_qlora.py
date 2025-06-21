from transformers import AutoTokenizer, AutoModelForCausalLM, TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset
import torch
from peft import LoraConfig, get_peft_model, TaskType, prepare_model_for_kbit_training

model_name = "NousResearch/Llama-3.2-1B"

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    load_in_4bit=True,
    torch_dtype=torch.bfloat16,
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_quant_type="nf4"
)

model = prepare_model_for_kbit_training(model)

lora_config = LoraConfig(
    task_type=TaskType.CAUSAL_LM,
    inference_mode=False,
    r=16,
    lora_alpha=32,
    lora_dropout=0.05
)

model = get_peft_model(model, lora_config)

dataset = load_dataset("json", data_files="data/annotated.jsonl", split="train")

def tokenize_function(examples):
    return tokenizer(
        examples['prompt'] + "\nResposta:\n" + examples['response'],
        truncation=True,
        padding="max_length",
        max_length=512
    )

tokenized_datasets = dataset.map(tokenize_function, batched=True)

data_collator = DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False)

training_args = TrainingArguments(
    output_dir="./llama3-ner-finetuned",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=8,
    learning_rate=2e-5,
    num_train_epochs=3,
    save_strategy="epoch",
    logging_steps=20,
    fp16=True,
    optim="paged_adamw_32bit",
    report_to="none"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets,
    data_collator=data_collator
)

trainer.train()
trainer.save_model("./Llama-3.2-1B-finetuned")
