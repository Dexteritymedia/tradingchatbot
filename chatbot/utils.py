import os
import requests
import json

from django.conf import settings

from langchain.utilities import GoogleSerperAPIWrapper
from langchain.llms.openai import OpenAI
from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain import LLMMathChain
from langchain.memory import ConversationBufferMemory

openai_api_key = settings.OPENAI_API_KEY
alpha_vantage_api_key = settings.ALPHA_VANTAGE_API_KEY

os.environ["OPENAI_API_KEY"] = openai_api_key


def multiple_stock_price():
    symbols= ["IBM", "MSFT", "APPL"]
    for symbol in symbols:
        url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}=5min&apikey=alpha_vantage_api_key'
        r = requests.get(url)
        data = r.json()
        data_as_json = json.dumps(data)
    return data_as_json
	
def stock_price_url():
    API_URL = "https://www.alphavantage.co/query"
    symbols= ["IBM", "MSFT", "APPL"]
    for symbol in symbols:
        data = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": "P03P4EKA8ACV2PPN",
        }
        response = requests.get(API_URL, params=data)
        data = response.json()
        data_as_json = json.dumps(data)
        return data_as_json

def stock_price_url():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=alpha_vantage_api_key'
    r = requests.get(url)
    data = r.json()
    data_as_json = json.dumps(data)
    return data_as_json
	
def ema_stock_price_url():
    url = 'https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=alpha_vantage_api_key'
    r = requests.get(url)
    data = r.json()
    data_as_json = json.dumps(data)
    return data_as_json

def sma_stock_price_url():
    url = "https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=alpha_vantage_api_key"
    r = requests.get(url)
    data = r.json()
    data_as_json = json.dumps(data)
    return data_as_json
	
def macd_stock_price_url():
    url = "https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=open&apikey=alpha_vantage_api_key"
    r = requests.get(url)
    data = r.json()
    data_as_json = json.dumps(data)
    return data_as_json
	
def chatbot(message):
    llm = OpenAI(temperature=0)
    search_func = GoogleSerperAPIWrapper()
    llm_math_chain = LLMMathChain(llm=llm)
    tools = [
        Tool(
            name = "Google Search",
            func=search_func.run,
            description="useful for when you need to answer questions about current events"
        ),
    	Tool(
    	    name = "Calculator",
    	    func=llm_math_chain.run,
    	    description="useful for when you need to answer math questions"
        ),
    	Tool(
    	    name='Stock DB',
    	    func=stock_price_url.run,
    	    description="Useful for when you need to answer questions about stocks and their prices."
        )
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)
    chain_run = agent_chain.run(input=message)
	
    #self_ask_with_search = initialize_agent(tools, llm, agent=AgentType.SELF_ASK_WITH_SEARCH, verbose=True)
    #self_ask_with_search.run("What is the hometown of the reigning men's U.S. Open champion?")
    return chain_run
	
def indicator_chatbot(message):
    llm = OpenAI(temperature=0)
    tools = [
        Tool(
            name = "EMA Stock",
            func=ema_stock_price_url.run,
            description="useful for when you need to answer questions about stocks exponential moving average (EMA) values"
        ),
    	Tool(
    	    name = "SMA Stock",
    	    func=sma_stock_price_url.run,
    	    description="useful for when you need to answer questions about simple moving average (SMA) values"
        ),
    	Tool(
    	    name='MACD Stock',
    	    func=macd_stock_price_url.run,
    	    description="Useful for when you need to answer questions about stocks moving average convergence / divergence (MACD) values and their prices."
        )
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)
    chain_run = agent_chain.run(input=message)
    return chain_run
