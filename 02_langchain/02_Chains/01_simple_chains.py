from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser # gives output as string only

load_dotenv()

chat_model = ChatGoogleGenerativeAI(
    model='models/gemini-2.5-flash',
    temperature=0.5
)

prompt = PromptTemplate(
    input_variables=["topic"],
    template="Generate 5 intresting facts about {topic}?"
)

output_parser = StrOutputParser()

chain = prompt | chat_model | output_parser 
result = chain.invoke({"topic": "space exploration"})
print(result)