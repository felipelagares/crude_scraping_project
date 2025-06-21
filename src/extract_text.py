import os
import re
from bs4 import BeautifulSoup

def extract_texts():
    # Pasta de saída para os textos extraídos
    pasta_saida = "textos"
    os.makedirs(pasta_saida, exist_ok=True)

    # Varre todos os arquivos XML da pasta
    for nome_arquivo in os.listdir('xmls'):
        caminho_entrada = os.path.join('xmls', nome_arquivo)
        # Lê o conteúdo do XML
        with open(caminho_entrada, "r", encoding="utf-8") as f:
            xml_content = f.read()
        # Parseia com BeautifulSoup
        soup = BeautifulSoup(xml_content, "xml")
        texto_tag = soup.find("Texto")
        if texto_tag:
            # Extrai o conteúdo da tag <Texto> (com HTML interno)
            texto_html = texto_tag.text
            # Limpa o HTML interno
            texto_limpo = BeautifulSoup(texto_html, "html.parser").get_text()
            # Remove quebras e espaços excessivos
            texto_final = re.sub(r'\s+', ' ', texto_limpo).strip()
            # Gera o nome do arquivo de saída
            nome_saida = os.path.splitext(nome_arquivo)[0] + ".txt"
            caminho_saida = os.path.join(pasta_saida, nome_saida)
            # Salva o texto limpo
            with open(caminho_saida, "w", encoding="utf-8") as f:
                f.write(texto_final)
        else:
            print(f"[!] Tag <Texto> não encontrada em: {nome_arquivo}")

if __name__ == "__main__":
    extract_texts()
    print("Extração de textos concluída.")