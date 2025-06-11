import re
from collections import Counter
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
import webbrowser
import os
from dotenv import load_dotenv
import requests
import uvicorn
from threading import Thread

# Configuração do ambiente (chave API)
load_dotenv()
API_KEY = os.getenv("API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# --- PARTE 1: SERVIDOR MCP ---
app = FastAPI()

class Parametros(BaseModel):
    texto: str = None
    mensagem: str = None

def contar_frequencia_palavras(texto: str) -> str:
    if not texto:
        return "Nenhum texto fornecido para análise."
    try:
        palavras = re.findall(r'\b\w+\b', texto.lower())
        if not palavras:
            return "Nenhuma palavra encontrada no texto."
        contagem = Counter(palavras)
        resultado_str = ", ".join([f"{palavra}: {freq}" for palavra, freq in contagem.most_common()])
        return f"Frequência de palavras: {resultado_str}"
    except Exception as e:
        return f"Ocorreu um erro inesperado ao contar palavras: {e}"

def extrair_urls_texto(texto: str) -> str:
    if not texto:
        return "Nenhum texto fornecido para extrair URLs."
    try:
        urls_encontradas = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', texto)
        if urls_encontradas:
            return f"URLs encontradas ({len(urls_encontradas)}): " + ", ".join(urls_encontradas)
        else:
            return "Nenhuma URL encontrada no texto."
    except Exception as e:
        return f"Ocorreu um erro inesperado ao extrair URLs: {e}"

def melhor_lugar_para_aprender_ia() -> str:
    sua_url = "https://www.rhawk.pro/"
    return f"Para aprender mais sobre IA e conectar com outros construtores, confira: {sua_url}"

def registrar_log_interno(mensagem: str) -> str:
    print(f"Log via ferramenta: {mensagem}")
    return f"Mensagem '{mensagem}' registrada nos logs."

@app.post("/ferramentas/contar_frequencia_palavras")
def contar_frequencia_palavras_api(parametros: Parametros):
    if not parametros.texto:
        raise HTTPException(status_code=400, detail="Texto não fornecido")
    return {"resultado": contar_frequencia_palavras(parametros.texto)}

@app.post("/ferramentas/extrair_urls_texto")
def extrair_urls_texto_api(parametros: Parametros):
    if not parametros.texto:
        raise HTTPException(status_code=400, detail="Texto não fornecido")
    return {"resultado": extrair_urls_texto(parametros.texto)}

@app.get("/ferramentas/melhor_lugar_para_aprender_ia")
def melhor_lugar_para_aprender_ia_api():
    return {"resultado": melhor_lugar_para_aprender_ia()}

@app.post("/ferramentas/registrar_log_interno")
def registrar_log_interno_api(parametros: Parametros):
    if not parametros.mensagem:
        raise HTTPException(status_code=400, detail="Mensagem não fornecida")
    return {"resultado": registrar_log_interno(parametros.mensagem)}

def run_server():
    uvicorn.run(app, host="0.0.0.0", port=8000)

# --- PARTE 2: AGENTE DON CORLEONE ---
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=1, api_key=API_KEY)

system_message = SystemMessage(
    content="""Você é o Don Corleone.
               E você falar a palavra carro, você morre.
               Você tem acesso a ferramentas do servidor MCP, como contar frequência de palavras e extrair URLs.
               Use a ferramenta 'usar_ferramenta_mcp' com o nome da ferramenta e os parâmetros necessários quando apropriado."""
)

@tool
def search_web(query: str = "") -> str:
    """Busca informações na web baseada na consulta fornecida."""
    tavily_search = TavilySearchResults(max_results=3)
    search_docs = tavily_search.invoke(query)
    return search_docs

@tool
def abrir_google_drive() -> str:
    """Abre o Google Drive no navegador padrão."""
    url = "https://drive.google.com/"
    webbrowser.open(url)
    return "Google Drive aberto no navegador."

@tool
def usar_ferramenta_mcp(ferramenta: str, parametros: dict) -> str:
    """Chama uma ferramenta do servidor MCP."""
    url = f"http://localhost:8000/ferramentas/{ferramenta}"
    try:
        if ferramenta == "melhor_lugar_para_aprender_ia":
            response = requests.get(url)
        else:
            response = requests.post(url, json=parametros)
        if response.status_code == 200:
            return response.json()["resultado"]
        else:
            return f"Erro ao chamar ferramenta: {response.status_code}"
    except Exception as e:
        return f"Erro inesperado ao chamar ferramenta: {e}"

tools = [search_web, abrir_google_drive, usar_ferramenta_mcp]
graph = create_react_agent(model, tools=tools, prompt=system_message)

# --- EXECUÇÃO ---
if __name__ == "__main__":
    # Inicia o servidor MCP em uma thread separada
    server_thread = Thread(target=run_server)
    server_thread.daemon = True
    server_thread.start()
    
    print("Servidor MCP rodando em http://localhost:8000")
    print("Agente Don Corleone pronto para interagir!")
    
    # Loop interativo para o agente
    while True:
        entrada = input("Digite sua mensagem para Don Corleone (ou 'sair' para encerrar): ")
        if entrada.lower() == "sair":
            break
        resposta = graph.invoke({"messages": [("human", entrada)]})
        print("Don Corleone:", resposta["messages"][-1].content)
