from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import ollama

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
    mensagens: list[Mensagem]

@app.post("/chat")
def responder(pedido: PedidoChat):
    with open("conhecimento_manual.md", "r", encoding="utf-8") as f_manual:
        info_manual = f_manual.read()

    with open("base_fablab_biobip.md", "r", encoding="utf-8") as f_manual:
        info_manual = f_manual.read()

    with open("base_conhecimento.txt", "r", encoding="utf-8") as ficheiro:
        conteudo_site = ficheiro.read()

    instrucoes_sistema = f"""
És o assistente virtual oficial do FabLab BioBIP.
Responde às perguntas dos visitantes em português de Portugal, de forma clara, simpática e objetiva.

REGRAS IMPORTANTES:
1. Baseia as tuas respostas EXCLUSIVAMENTE na informação fornecida abaixo.
2. Dá prioridade à secção "INFORMAÇÃO OFICIAL CURADA".
3. Nunca inventes preços, horários, regras ou serviços que não estejam no texto.
4. Se a resposta não estiver na informação abaixo, diz educadamente que não tens essa informação e sugere o contacto através do e-mail biobip@uportalegre.pt ou telefone (+351) 245 301 555.

=== INFORMAÇÃO OFICIAL CURADA ===
{info_manual}

=== CONTEÚDO EXTRAÍDO DO SITE ===
{conteudo_site}
"""

    # 3. Juntar as instruções do sistema às últimas 10 mensagens da conversa
    historico_recente = [msg.model_dump() for msg in pedido.mensagens[-10:]]
    conversa_completa = [{"role": "system", "content": instrucoes_sistema}] + historico_recente

    resposta = ollama.chat(
        model="llama3.2",
        messages=conversa_completa,
        options={
            "temperature": 0.2,
            "num_ctx": 16384,
        },
    )
    return {"resposta": resposta["message"]["content"]}