from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Molde para cada mensagem individual do histórico
class Mensagem(BaseModel):
    role: str
    content: str

# 2. O pedido agora traz a lista completa das mensagens trocadas
class PedidoChat(BaseModel):
    mensagens: list[Mensagem] | None = None
    messages: list[Mensagem] | None = None


@app.post("/chat")
def responder(pedido: PedidoChat):
    historico = pedido.mensagens or pedido.messages or []
    historico_recente = [msg.model_dump() for msg in historico[-10:]]

    nome_ficheiro = (
        "base_fablab_biobip.md"
        if os.path.exists("base_fablab_biobip.md")
        else "base_conhecimento.txt"
    )
    with open(nome_ficheiro, "r", encoding="utf-8") as f_site:
        conteudo_site = f_site.read()

    info_manual = ""
    if os.path.exists("conhecimento_manual.md"):
        with open("conhecimento_manual.md", "r", encoding="utf-8") as f_manual:
            info_manual = f_manual.read()

    instrucoes_sistema = f"""
És o assistente virtual oficial do FabLab BioBIP.
Responde às perguntas dos visitantes em português de Portugal, de forma clara, simpática e objetiva.

REGRAS IMPORTANTES:
1. Baseia as tuas respostas EXCLUSIVAMENTE na informação fornecida abaixo.
2. Dá prioridade à secção "INFORMAÇÃO OFICIAL CURADA" se existir.
3. Nunca inventes preços, horários, regras ou serviços que não estejam no texto.
4. Se a resposta não estiver na informação abaixo, diz educadamente que não tens essa informação e sugere o contacto através do e-mail biobip@uportalegre.pt ou telefone (+351) 245 301 555.

=== INFORMAÇÃO OFICIAL CURADA ===
{info_manual}

=== CONTEÚDO DO SITE ===
{conteudo_site}
"""

    mensagens_api = [{"role": "system", "content": instrucoes_sistema}] + historico_recente

    resposta = cliente_ia.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=mensagens_api,
        temperature=0.2,
    )

    return {"resposta": resposta.choices[0].message.content}
