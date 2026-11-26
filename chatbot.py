import ollama

# 1. Ler o ficheiro de texto com o conteúdo do teu site
with open("base_conhecimento.txt", "r", encoding="utf-8") as ficheiro:
    conteudo_site = ficheiro.read()

# 2. Definir a personalidade e as regras do chatbot (System Prompt)
instrucoes_sistema = f"""
És o assistente virtual oficial deste site.
Responde às perguntas dos visitantes em português de Portugal, de forma clara, simpática e objetiva.

REGRAS IMPORTANTES:
1. Baseia as tuas respostas EXCLUSIVAMENTE na informação fornecida abaixo.
2. Nunca inventes preços, horários, regras ou serviços que não estejam no texto.
3. Se a resposta não estiver na informação abaixo, diz educadamente que não tens essa informação e sugere que entrem em contacto através dos meios disponíveis no site.

INFORMAÇÃO DO SITE:
{conteudo_site}
"""

print("Chatbot local pronto! Faz uma pergunta sobre o teu site (ou escreve 'sair' para terminar).\n")

# 3. Ciclo contínuo de conversa no terminal
while True:
    pergunta = input("Tu: ")

    if pergunta.lower() == "sair":
        print("A encerrar o chatbot. Até breve!")
        break

    if pergunta.strip() == "":
        continue

    # 4. Enviar as instruções e a pergunta para o modelo local no Mac
    resposta = ollama.chat(
        model="llama3.2",
        messages=[
            {"role": "system", "content": instrucoes_sistema},
            {"role": "user", "content": pergunta},
        ],
        options={
            "temperature": 0.2,
            "num_ctx": 8192,
        },
    )

    print(f"\nAssistente: {resposta['message']['content']}\n")