from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
import json
import os

model_name = "Davlan/xlm-roberta-base-ner-hrl"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name)

ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

input_file = "data/full_text.txt"
output_file = "data/annotated.jsonl"

os.makedirs("data", exist_ok=True)

with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", encoding="utf-8") as f_out:
    for i, line in enumerate(f_in, 1):
        text = line.strip()
        if not text:
            continue
        entities = ner_pipeline(text)
        ents = {}
        for ent in entities:
            label = ent['entity_group']
            ents.setdefault(label, []).append(ent['word'])
        example = {
            "prompt": f"Extraia as entidades nomeadas do seguinte texto: '{text}'",
            "response": json.dumps(ents, ensure_ascii=False)
        }
        f_out.write(json.dumps(example, ensure_ascii=False) + "\n")
        if i % 100 == 0:
            print(f"{i} linhas processadas")