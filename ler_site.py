import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

paginas = [
    "https://www.biobip.pt/fablab/",
    "https://fablab.ipportalegre.pt/sobre/",
    "https://fablab.ipportalegre.pt/regulamento-do-fablab/",
    "https://fablab.ipportalegre.pt/carta-de-principios-fab-chart/",
    "https://fablab.ipportalegre.pt/tabela-de-precos/",
    "https://fablab.ipportalegre.pt/protocolos-e-parcerias/"
    # adiciona aqui as restantes páginas
]

cabecalhos = {"User-Agent": "Mozilla/5.0"}
conteudo_total = []

for url in paginas:
    print(f"A ler página: {url}...")
    resposta = requests.get(url, headers=cabecalhos)

    if resposta.status_code == 200:
        sopa = BeautifulSoup(resposta.text, "html.parser")

        for elemento in sopa(["script", "style", "nav", "footer", "header"]):
            elemento.decompose()

        # Converte o HTML limpo para Markdown, preservando títulos e listas
        texto_markdown = md(str(sopa), heading_style="ATX").strip()

        bloco_formatado = f"# FONTE: {url}\n\n{texto_markdown}"
        conteudo_total.append(bloco_formatado)

with open("base_conhecimento.md", "w", encoding="utf-8") as ficheiro:
    ficheiro.write("\n\n---\n\n".join(conteudo_total))

print("Concluído! Guardado em 'base_conhecimento.md'.")