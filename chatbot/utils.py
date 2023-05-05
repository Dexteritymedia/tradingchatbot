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
from langchain.utilities import SerpAPIWrapper
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma, FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain.document_loaders import DataFrameLoader
from langchain.embeddings import OpenAIEmbeddings
from langchain.agents import create_pandas_dataframe_agent

import numexpr as ne

import pandas as pd

os.environ['NUMEXPR_MAX_THREADS'] = '4'
os.environ['NUMEXPR_NUM_THREADS'] = '2'

openai_api_key = settings.OPENAI_API_KEY
alpha_vantage_api_key = settings.ALPHA_VANTAGE_API_KEY
serper_api_key = settings.SERPER_API_KEY

os.environ["OPENAI_API_KEY"] = openai_api_key
os.environ["SERPER_API_KEY"] = serper_api_key

splitter = CharacterTextSplitter(
  chunk_size=2000,
  chunk_overlap=50,
  separator=" "
)
llm = OpenAI(model_name="text-davinci-003", temperature=0)

url = "https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=alpha_vantage_api_key"
r = requests.get(url)
wrapped_data = r.content.decode("utf-8")
data_dict = json.loads(wrapped_data)
df_time_series = pd.DataFrame(data_dict['Time Series (5min)'])
df = df_time_series.T
df['ticker'] = 'IBM'
df.reset_index(inplace=True)
stock_price_loader = DataFrameLoader(df, page_content_column="ticker")
stock_price_data = stock_price_loader.load()
stock_price_data_split = splitter.split_documents(stock_price_data)
embeddings = OpenAIEmbeddings()

stock_price_store = FAISS.from_documents(
    stock_price_data_split, embeddings,
)

stock_price_template = """As a Stock analyst bot, your goal is to provide accurate and helpful information about the stock market.
You should answer user inquiries based on the context provided and avoid making up answers.
If you don't know the answer, simply state that you don't know.
Remember to provide relevant information about the stock market prices, values, moving averages, time
and use cases to assist the user in understanding its value for application development.

{context}

Question: {question}"""
STOCK_PROMPT = PromptTemplate(
    template=stock_price_template, input_variables=["context", "question"]
)
stock_price_qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=stock_price_store.as_retriever(),
    chain_type_kwargs={"prompt": STOCK_PROMPT},
)

def pandas_agent(request):
    df = df_time_series.T
    pandas_agent_df = create_pandas_dataframe_agent(OpenAI(temperature=0), df,)
    return pandas_agent_df

def chatbot(message):
    llm = OpenAI(temperature=0)
    #search_func = GoogleSerperAPIWrapper()
    #search = SerpAPIWrapper()
    llm_math_chain = LLMMathChain(llm=llm)
    tools = [
    	Tool(
    	    name = "Calculator",
    	    func=llm_math_chain.run,
    	    description="useful for when you need to answer math questions"
        ),
        Tool(
        name = "Stock",
        func=stock_price_qa.run,
        description="""useful for when a user is interested in various stock price information,
                       use-cases, or applications. A user is not asking for any professional advice, but is only
                       interested in general advice based on the stock price, values and direction.
                       Input should be a fully formed question."""
        ),
        Tool(
        name='Pandas Data frame tool',
        func=pandas_agent,
        description="Useful for when you need to answer questions about a stock open, high, low and close price in a pandas Dataframe"
        ),
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)
    chain_run = agent_chain.run(input=message)
    return chain_run



def multiple_stock_price(request):
	symbols= ["IBM", "MSFT", "APPL"]
	for symbol in symbols:
		url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={symbol}&interval==5min&apikey=alpha_vantage_api_key'
		r = requests.get(url)
		data = r.json()
		data_as_json = json.dumps(data)
		return data_as_json

def multiple_stock_price_url(request):
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

def stock_price_url(request):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&outputsize=compact&apikey=alpha_vantage_api_key'
    r = requests.get(url)
    data = r.json()
    data_as_json = json.dumps(data)
    return data_as_json

def ema_stock_price_url(request):
    url = 'https://www.alphavantage.co/query?function=EMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=alpha_vantage_api_key'
    r = requests.get(url)
    data = r.json()
    data_as_json = json.dumps(data)
    return data_as_json

def sma_stock_price_url(request):
    url = "https://www.alphavantage.co/query?function=SMA&symbol=IBM&interval=weekly&time_period=10&series_type=open&apikey=alpha_vantage_api_key"
    r = requests.get(url)
    data = r.json()
    data_as_json = json.dumps(data)
    return data_as_json

def macd_stock_price_url(request):
    url = "https://www.alphavantage.co/query?function=MACD&symbol=IBM&interval=daily&series_type=open&apikey=alpha_vantage_api_key"
    r = requests.get(url)
    data = r.json()
    data_as_json = json.dumps(data)
    return data_as_json

def chatbot_(message):
    llm = OpenAI(temperature=0)
    search_func = GoogleSerperAPIWrapper()
    google_search = SerpAPIWrapper()
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
    llm_math_chain = LLMMathChain(llm=llm)
    tools = [
        Tool(
    	    name='Stock DB',
    	    func=stock_price_url,
    	    description="Useful for when you need to answer questions about stocks and their prices."
        ),
        Tool(
            name = "EMA Stock",
            func=ema_stock_price_url,
            description="useful for when you need to answer questions about stocks exponential moving average (EMA) values"
        ),
    	Tool(
    	    name = "SMA Stock",
    	    func=sma_stock_price_url,
    	    description="useful for when you need to answer questions about simple moving average (SMA) values"
        ),
    	Tool(
    	    name='MACD Stock',
    	    func=macd_stock_price_url,
    	    description="Useful for when you need to answer questions about stocks moving average convergence / divergence (MACD) values and their prices."
        ),
        Tool(
    	    name = "Calculator",
    	    func=llm_math_chain.run,
    	    description="useful for when you need to answer math questions such as calculating compound and simple interests, interest rate, percentage increase or decrease in price."
        ),
    ]
    memory = ConversationBufferMemory(memory_key="chat_history")
    agent_chain = initialize_agent(tools, llm, agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION, memory=memory)
    chain_run = agent_chain.run(input=message)
    return chain_run
