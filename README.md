# crude_scraping_project

## Descrição

Este projeto realiza a raspagem de links de arquivos públicos do site do Diário Oficial da União utilizando Selenium pelo fato do conteúdo ser dinamicamente atualizado (apesar de poder ser pesquisado pelo link o conteúdo desejado tem um delay de carregamento maior do que a página).

salva os links de download encontrados em um arquivo de texto e a partir dele faz o download automático dos arquivos ZIP correspondentes.

Esse arquivo baixado vem com xmls e imagens, muito disso que não cabe ao objetivo do projeto e portanto deve ser limpo e tratado. As imagens são excluidas e o texto útil extraído do xml.

O texto extraído é pré anotado por uma llm em um unico arquivo que é usado para fazer o fine-tunning de um outro modelo tornando especializado no tema.

## Diagrama do pipeline

![Fluxo do projeto](docs/image.png)

## Instruções de execução

1. **Clone o repositório e acesse a pasta:**

   ```sh
   git clone <url-do-repositorio>
   cd crude_scraping_project
   ```

2. **Crie e ative um ambiente virtual:**

   ```sh
   python -m venv venv
   venv\Scripts\activate   # No Windows
   # source venv/bin/activate  # No Linux/Mac
   ```

3. **Instale as dependências:**

   ```sh
   pip install -r requirements.txt
   ```

4. **Execute o script de raspagem para coletar os links:**

   ```sh
   python src/scraping.py
   ```

5. **Execute o script de download para baixar os arquivos ZIP:**

   ```sh
   python src/download.py
   ```

6. **Os arquivos baixados estarão na pasta `src/zips/` e devem ser limpos.**

   ```sh
   python src/extract_xml.py
   ```

7. **Os xmls estarão dentro da pasta `src/xmls` e devem ter seu texto extraído**

   ```sh
   python src/extract_text.py
   ```

8. **Os textos estarão dentro da pasta `src/textos` e são concatenados em um único**

   ```sh
   python src/concat_text.py
   ```

9. **O arquivo gerado `src/data/full_text.txt` pode então ser anotado**

   ```sh
   python src/pre_anotation.py
   ```

10. **`src/data/annotated.jsonl` pode ser usado para treinar o modelo**

   ```sh
   python src/finetune_qlora.py
   ```

11. **O modelo pode ser usado para fazer inferencias**

   ```sh
   python src/inference.py
   ```

## Licenças

Este projeto está licenciado sob a licença MIT. Consulte o arquivo [LICENSE](docs/LICENSE) para mais detalhes.

## Problemas e desenvolvimento futuro

Armazenamento: são muitos arquivos zips, xml e de texto que devem ser armazenados. possivelmente em banco noSQL como mongodb mas o texto pode ser armazenado em postgres também.

Capacidade da máquina: São muitos, muitos arquivos mesmo, ao ponto de ficar perdido e demorar até para extrair o texto de todos os xmls. Piora ainda mais ao tentar fazer o fine-tunning da llm que apesar de possivel é extremamente exaustivo e demorado.

Estrutura: esse pipeline não deveria estar com arquivos soltos dessa forma, deveriam estar orquestrados por um airflow em um container docker para um ambiente profissinal.
