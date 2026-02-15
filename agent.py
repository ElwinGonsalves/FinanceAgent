import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from dotenv import load_dotenv

try:
    from langgraph.prebuilt import create_react_agent
except ImportError:
    # If langgraph is not found, we really can't proceed with this architecture
    raise ImportError("langgraph is required but not installed.")

# Import our local tools
# Note: In Streamlit, imports might need adjustment depending on how it's run.
# We will assume running from root or finance_agent directory.
try:
    from tools.currency import get_exchange_rates
    from tools.stocks import get_stock_data
    from tools.maps import get_maps_link
except ImportError:
    # Fallback for running from parent directory
    from finance_agent.tools.currency import get_exchange_rates
    from finance_agent.tools.stocks import get_stock_data
    from finance_agent.tools.maps import get_maps_link

load_dotenv()

@tool
def currency_tool(country: str):
    """
    Get official currency and exchange rates (USD, INR, GBP, EUR) for a specific country.
    """
    return get_exchange_rates(country)

@tool
def stock_tool(country: str):
    """
    Get major stock indices and current market data for a specific country.
    """
    return get_stock_data(country)

@tool
def maps_tool(country: str):
    """
    Get the Google Maps link for the main Stock Exchange HQ of a specific country.
    """
    return get_maps_link(country)

def initialize_agent():
    """
    Initializes the LangGraph agent with Groq (Llama 3) and financial tools.
    """
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY not found in environment variables.")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0,
        groq_api_key=api_key
    )

    tools = [currency_tool, stock_tool, maps_tool]
    
    # State prompt is handled internally by create_react_agent or we can pass messages_modifier
    # We will pass a system message as state_modifier
    system_message = (
        "You are an expert Financial Intelligence Agent. "
        "Your goal is to provide accurate financial data for a given country. "
        "You MUST use the provided tools to get exchange rates, stock indices, and location links. "
        "Do not make up data. If a tool returns specific data, use it exactly. "
        "Output the final answer as a structured summary, but you can also include the raw JSON in a code block if requested."
    )

    # create_react_agent returns a CompiledGraph which acts as the 'agent executor'
    # We remove state_modifier as it is not supported in this version.
    # We will pass the system prompt in the messages list at runtime.
    agent_graph = create_react_agent(llm, tools=tools)
    
    return agent_graph
