from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage
from langchain_core.tools import tool

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults

import webbrowser
import os
from dotenv import load_dotenv

# Configuração do ambiente (chave API)
load_dotenv()
API_KEY = os.getenv("API_KEY")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=1, api_key=API_KEY)

# Define o prompt do sistema
system_message = SystemMessage(
    content="""Você é o Don Corleone. 
                               E você falar a palavra carro, você morre."""
)


@tool
def search_web(query: str = "") -> str:
    """Busca informações na web baseada na consulta fornecida.

    Args:
        query: Termos para buscar na web

    Returns:
        As informações encontradas na web ou uma mensagem indicando que nenhuma informação foi encontrada.
    """
    tavily_search = TavilySearchResults(max_results=3)
    search_docs = tavily_search.invoke(query)
    return search_docs


def abrir_google_drive() -> str:
    """Abre o Google Drive no navegador padrão"""
    url = "https://drive.google.com/"
    webbrowser.open(url)
    return "Google Drive aberto no navegador."


# Lista de ferramentas
tools = [search_web, abrir_google_drive]


# Criação do agente ReAct com memória
graph = create_react_agent(model, tools=tools, prompt=system_message)
