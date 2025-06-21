import requests
import os

def download_files():
    # Lê os links do arquivo txt
    with open('links_encontrados.txt', 'r', encoding='utf-8') as f:
        links = [line.strip() for line in f if line.strip()]

    for idx, url in enumerate(links, 1):
        if url:
            os.makedirs('zips', exist_ok=True)
            # Gera um nome de arquivo baseado no índice ou parte da URL
            filename = f"arquivo_{idx}.zip"
            filepath = os.path.join('zips', filename)
            # Verifica se o arquivo já existe
            if os.path.exists(filepath):
                print(f"{filename} já existe, pulando download.")
                continue
            resp = requests.get(url)
            if resp.status_code == 200:
                with open(filepath, 'wb') as out:
                    out.write(resp.content)
                print(f"{filename} baixado com sucesso.")
            else:
                print(f"Falha ao baixar {url}")

if __name__ == "__main__":
    download_files()
