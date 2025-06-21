from transformers import AutoTokenizer, AutoModelForTokenClassification, pipeline
from nltk.tokenize import sent_tokenize, word_tokenize
import nltk
import os

def extract_bio():
    nltk.download("punkt")
    nltk.download("punkt_tab")
    # Modelo NER pronto para uso
    model_name = "pierreguillou/ner-bert-base-cased-pt-lenerbr"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForTokenClassification.from_pretrained(model_name)

    ner_pipeline = pipeline("ner", model=model, tokenizer=tokenizer, aggregation_strategy="simple")

    # Texto de entrada
    caminho_entrada = "full_text.txt"
    with open(caminho_entrada, "r", encoding="utf-8") as f:
        texto = f.read()

    # Divide o texto em sentenças
    sentencas = sent_tokenize(texto, language="portuguese")

    bio_linhas = []

    for sent in sentencas:
        resultados = ner_pipeline(sent)
        tokens_ja_anotados = set()
        palavras_sent = word_tokenize(sent, language="portuguese")

        for r in resultados:
            palavras = r['word'].split()
            for i, p in enumerate(palavras):
                tag = "B-" + r['entity_group'] if i == 0 else "I-" + r['entity_group']
                bio_linhas.append(f"{p} {tag}")
                tokens_ja_anotados.add(p)

        for t in palavras_sent:
            if t not in tokens_ja_anotados:
                bio_linhas.append(f"{t} O")

        bio_linhas.append("")  # separa sentenças

    # Salva em BIOs/
    os.makedirs("BIOs", exist_ok=True)
    saida = os.path.join("BIOs", "bios.txt")
    with open(saida, "w", encoding="utf-8") as f:
        f.write("\n".join(bio_linhas))
