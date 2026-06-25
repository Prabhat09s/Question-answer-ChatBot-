# import streamlit as st
# from langchain_google_genai import ChatGoogleGenerativeAI
# from langchain_core.output_parsers import StrOutputParser
# from langchain_core.prompts import ChatPromptTemplate
# import os 
# from dotenv import load_dotenv
# load_dotenv()

# ## Langchain Tracking
# import os
# from dotenv import load_dotenv

# load_dotenv()

# langchain_key = os.getenv("LANGCHAIN_API_KEY")

# if langchain_key:
#     os.environ["LANGCHAIN_API_KEY"] = langchain_key
# # os.environ["LANGCHAIN_API_KEY"]=os.getenv("LANGCHAIN_API_KEY")
#     os.environ["LANGCHAIN_TRACKING_V2"]="true"
#     os.environ["LANGCHAIN_PROJECT"]="Simple Q&A ChatBot"

# ## Prompt Tempate
# prompt = ChatPromptTemplate.from_messages(
#     [
#         ("system","You are a helpful massistant. please response to the user queries"),
#         ("user","Question:{question}")
#     ]
# )

# def generate_response(question,api_key,engine,temperature,max_token):
#     # Set Gemini API key
#     # api_ky=os.environ["GOOGLE_API_KEY"] 
#     api_ky = os.getenv("GOOGLE_API_KEY")

#     # llm=ChatGoogleGenerativeAI(model=engine)
#     llm = ChatGoogleGenerativeAI(
#     model="gemini-2.0-flash",
#     google_api_key=api_ky,
#     temperature=temperature,
#     max_tokens=max_token
# )
#     output_parser=StrOutputParser()
#     chain=prompt|llm|output_parser
#     answer=chain.invoke({"question":question})
#     return answer

# ## Title of the app
# st.title("Enhance Q&A ChatBot With OpenAI")

# ## Side Bar Setting 
# st.sidebar.title('Setting')
# api_key=st.sidebar.text_input("Enter the Gemini API Key",type="password")

# ## Select the OpenAI model
# engine=st.sidebar.selectbox("Selcet Gemini model",["gemini-2.5-flash"])

# ## Adjust response parameter
# temperature=st.sidebar.slider("Temparature",min_value=0.0,max_value=1.0,value=0.7)
# max_token=st.sidebar.slider("Max Token",min_value=50,max_value=300,value=150)

# ## main Interface for user input
# st.write("Go Ahead and Aske Any Question")
# user_input=st.text_input("You:")

# if user_input and api_key:
#     response=generate_response(user_input,api_key,engine,temperature,max_token)
#     st.write(response)

# elif user_input:
#     st.warning("Please enter the Gemini api key in the sider bar")

# else:
#     st.write("Plear provide the user input")        

    

import os
import streamlit as st
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate

load_dotenv()

# LangChain tracking - optional
langchain_key = os.getenv("LANGCHAIN_API_KEY")
if langchain_key:
    os.environ["LANGCHAIN_API_KEY"] = langchain_key
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_PROJECT"] = "Simple Q&A ChatBot"

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are a helpful assistant. Please respond clearly to the user's question."),
    ("user", "Question: {question}")
])

def generate_response(question, api_key, engine, temperature, max_token):
    if not api_key:
        st.error("Gemini API key is missing.")
        st.stop()

    llm = ChatGoogleGenerativeAI(
        model=engine,
        google_api_key=api_key,
        temperature=temperature,
        max_tokens=max_token
    )

    output_parser = StrOutputParser()
    chain = prompt | llm | output_parser
    return chain.invoke({"question": question})


st.title("Gemini Q&A ChatBot")

st.sidebar.title("Settings")

api_key = st.sidebar.text_input(
    "Enter Gemini API Key",
    type="password",
    value=os.getenv("GOOGLE_API_KEY", "")
)

engine = st.sidebar.selectbox(
    "Select Gemini Model",
    ["gemini-2.0-flash-lite", "gemini-2.0-flash", "gemini-2.5-flash"]
)

temperature = st.sidebar.slider(
    "Temperature",
    min_value=0.0,
    max_value=1.0,
    value=0.7
)

max_token = st.sidebar.slider(
    "Max Tokens",
    min_value=50,
    max_value=500,
    value=150
)

st.write("Ask any question below:")

user_input = st.text_input("You:")

if user_input:
    try:
        response = generate_response(
            user_input,
            api_key,
            engine,
            temperature,
            max_token
        )
        st.write(response)

    except Exception as e:
        st.error("Something went wrong. Check your Gemini API key, quota, or model name.")
        st.write(str(e))
else:
    st.info("Please enter a question.")