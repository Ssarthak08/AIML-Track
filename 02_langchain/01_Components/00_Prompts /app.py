import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
import os 
from dotenv import load_dotenv

# Loading environment variables
load_dotenv()

# initialized the model
chat_model = ChatGoogleGenerativeAI(
    model = "models/gemini-2.5-flash",
    temperature = 0.5
)

st.title("Basic Gemini Summarizer")

text = st.text_area("Enter text:")

if st.button("Summarize"):
    if text.strip() == "":
        st.write("Please enter some text.")
    else:
        prompt = f"Summarize the following text in exactly 5 lines:\n\n{text}"
        
        response = chat_model.invoke(prompt)
        
        st.write("Summary:")
        st.write(response.content)

# this is all static promopts, in which user has the control over the prompts and he's deciding what to write 

# press ctlr C for stopping the session on the strealit app 