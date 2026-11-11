import os

from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from yarl import Query

load_dotenv()
from langchain.agents import create_agent
from langchain.tools import tool
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
#from langchain_tavily import TavilySearch
from tavily import TavilyClient

tavily_client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search(query: str) -> str:
    """
    Tool that searches over internet
    Args:
        query (str): The search query.

    Returns:
        str: The search result.
    """
    print(f"Searching for: {query}")
    return tavily_client.search(query = query)
    #return "Tokyo weather is sunny"


gemini_key = os.getenv("GEMINI_API_KEY")
gemini_model = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash-lite")

llm = ChatOpenAI(model = gemini_model,api_key = gemini_key,temperature = 0.7,max_tokens = 100,base_url="https://generativelanguage.googleapis.com/v1beta/openai/")
#tools = [TavilySearch(api_key=os.getenv("TAVILY_API_KEY"))]
tools = [search]
agent = create_agent(llm, tools)

def main():
    print("Hello from lang-chain")
    #response = agent.invoke({"messages": HumanMessage(content="What's the weather in Tokyo?")})
    response = agent.invoke({"messages": HumanMessage(content="search for 3 jobs for ai engineer in hyderabad, banglore?")})
    print(response["messages"][-1].content)

if __name__ == "__main__":
    main()