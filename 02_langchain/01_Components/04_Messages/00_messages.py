from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv

load_dotenv()

chat_model = ChatGoogleGenerativeAI(
    model = "models/gemini-2.5-flash",
    temperature = 0.5
)

messages = [
    SystemMessage(content="You are a helpful Assistant"),
    HumanMessage(content="Tell me about langchain and langraph")
]

Result = chat_model.invoke(messages)

messages.append(AIMessage(content=Result.content))
print(messages)