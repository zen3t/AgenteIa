# LangGraph 101

Documentação concisa para uso do script `langgraph-101.py`.

Código do vídeo: https://www.youtube.com/watch?v=9bSzZ-9eUkM

## Requisitos

- Python 3.10 ou superior
- Google Generative AI API Key
- Tavily API Key

## Recomendações

Crie e ative um ambiente virtual antes de instalar as dependências:

No vídeo
```bash
python3.12 -m venv .venv
source .venv/bin/activate # Linux/macOS
# .\.venv\Scripts\activate # Windows
```

## Instalação

```bash
pip install -r requirements.txt
```

## Configuração

Na raiz do projeto, crie o arquivo `.env` com as chaves:

```dotenv
API_KEY=sua_chave_api
TAVILY_API_KEY=sua_chave_tavily
```

## Uso

No terminal, execute:

```bash
langgraph dev
```

O script:

- Usa `dotenv` para carregar variáveis de ambiente
- Inicializa o modelo `gemini-2.0-flash`
- Define a ferramenta `search_web` com Tavily
- Cria um agente ReAct via `create_react_agent`

## Atenção

Alguns usuários relataram problemas com uso de windows.
O problema foi resolvido através do comando.
```bash
langgraph dev --allow-blocking
```

Lembresse que ao executar o agente será exibido em seu navegador padrão.
Como demonstrado no vídeo o meu navegador(Brave) bloqueia a execução mas no chrome funciona perfeitamente.
