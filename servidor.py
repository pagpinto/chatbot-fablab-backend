import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cliente_ia = Groq(api_key=os.environ.get("GROQ_API_KEY"))


class Mensagem(BaseModel):
    role: str
    content: str


class PedidoChat(BaseModel):
    mensagens: list[Mensagem] | None = None
    messages: list[Mensagem] | None = None


@app.get("/")
def raiz():
    return {"status": "ok", "servico": "chatbot-fablab-backend"}


@app.post("/chat")
def responder(pedido: PedidoChat):
    historico = pedido.mensagens or pedido.messages or []
    historico_recente = [msg.model_dump() for msg in historico[-10:]]

    nome_ficheiro = (
        "base_fablab_biobip.md"
        if os.path.exists("base_fablab_biobip.md")
        else "base_conhecimento.txt"
    )
    conteudo_site = ""
    if os.path.exists(nome_ficheiro):
        with open(nome_ficheiro, "r", encoding="utf-8") as f_site:
            conteudo_site = f_site.read()

    regulamento = ""
    if os.path.exists("regulamento-fablab.md"):
        with open("regulamento-fablab.md", "r", encoding="utf-8") as f_reg:
            regulamento = f_reg.read()

    info_manual = ""
    if os.path.exists("conhecimento_manual.md"):
        with open("conhecimento_manual.md", "r", encoding="utf-8") as f_manual:
            info_manual = f_manual.read()

    instrucoes_sistema = f"""
És o assistente virtual oficial do FabLab BioBIP.
Responde às perguntas dos visitantes em português de Portugal, de forma clara, simpática e objetiva.

REGRAS IMPORTANTES:
1. Baseia as tuas respostas EXCLUSIVAMENTE na informação fornecida abaixo.
2. Dá prioridade à secção "INFORMAÇÃO OFICIAL CURADA" e ao "REGULAMENTO DO FABLAB".
3. Nunca inventes preços, horários, regras ou serviços que não estejam no texto.
4. Se a resposta não estiver na informação abaixo, diz educadamente que não tens essa informação e sugere o contacto através do e-mail biobip@uportalegre.pt ou telefone (+351) 245 301 555.

=== INFORMAÇÃO OFICIAL CURADA ===
{info_manual}

=== REGULAMENTO DO FABLAB ===
{regulamento}

=== CONTEÚDO DO SITE ===
{conteudo_site}
"""

    mensagens_api = [{"role": "system", "content": instrucoes_sistema}] + historico_recente

    resposta = cliente_ia.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=mensagens_api,
        temperature=0.2,
    )

    texto = resposta.choices[0].message.content or ""

    return {
        "resposta": texto,
        "reply": texto,
        "response": texto,
        "message": texto,
    }