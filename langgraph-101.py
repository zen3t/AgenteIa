from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
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

# Configura o modelo de linguagem
model = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0.5, api_key=API_KEY)

# Define o prompt do sistema
system_message = SystemMessage(
    content="Você é um assistente útil que me ajuda com tarefas como buscar informações na web e abrir o Google Drive."
)

@tool
def search_web(query: str = "") -> str:
    """Busca informações na web baseada na consulta fornecida."""
    tavily_search = TavilySearchResults(max_results=5)
    search_docs = tavily_search.invoke(query)
    if not search_docs:
        return "Nenhum resultado encontrado."
    return "\n".join([f"{i+1}. {doc['content']}" for i, doc in enumerate(search_docs)])

@tool
def abrir_google_drive() -> str:
    """Abre o Google Drive no navegador padrão."""
    url = "https://drive.google.com/"
    webbrowser.open(url)
    return "Google Drive aberto no navegador."

# Lista de ferramentas
tools = [search_web, abrir_google_drive]

# Configura a memória
memory = InMemorySaver()

# Cria o agente ReAct com memória
graph = create_react_agent(model, tools=tools, prompt=system_message)
