import os

def concat_text(pasta_textos='textos', arquivo_saida='full_text.txt'):
    # Concatena os textos em um arquivo temporário
    with open(arquivo_saida, 'w', encoding='utf-8') as saida:
        for nome_arquivo in os.listdir(pasta_textos):
            if nome_arquivo.lower().endswith('.txt'):
                caminho = os.path.join(pasta_textos, nome_arquivo)
                with open(caminho, 'r', encoding='utf-8') as f:
                    saida.write(f.read())
                    saida.write('\n')  # separa os textos por uma linha em branco
