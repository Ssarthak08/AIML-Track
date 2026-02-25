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

# st.title("Basic Gemini Summarizer")

# text = st.text_area("Enter text:")

# if st.button("Summarize"):
#     if text.strip() == "":
#         st.write("Please enter some text.")
#     else:
#         prompt = f"Summarize the following text in exactly 5 lines:\n\n{text}"
        
#         response = chat_model.invoke(prompt)
        
#         st.write("Summary:")
#         st.write(response.content)

# this is all static promopts, in which user has the control over the prompts and he's deciding what to write 

# press ctlr C for stopping the session on the strealit app

st.title("Dynamic Gemini Summarizer")

# Text input
text = st.text_area("Enter text:")

# Dropdown 1: Paper Type
paper_type = st.selectbox(
    "Select paper type:",
    ["Research Paper", "Technical Paper", "Blog Post", "General Article"]
)

# Dropdown 2: Difficulty Level
difficulty = st.selectbox(
    "Select explanation level:",
    ["Simple", "Moderate", "Advanced"]
)

# Dropdown 3: Summary Length
length = st.selectbox(
    "Select summary length:",
    [3, 5, 8]
)

if st.button("Summarize"):
    if text.strip() == "":
        st.write("Please enter some text.")
    else:
        #Dynamic Prompt Construction
        prompt = f"""
        You are an expert summarizer.

        Paper Type: {paper_type}
        Explanation Level: {difficulty}

        Summarize the following text in exactly {length} concise lines.
        Adapt the explanation style according to the selected difficulty level.

        Text:
        {text}
        """

        response = chat_model.invoke(prompt)

        st.write("Summary:")
        st.write(response.content)