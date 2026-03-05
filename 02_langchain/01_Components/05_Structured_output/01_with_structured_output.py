# Typed Dict, tells the vscode what value in expected according to the mentioned key 

from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from typing import TypedDict, Annotated

load_dotenv()

chat_model = ChatGoogleGenerativeAI(
    model='models/gemini-2.5-flash',
    temperature=0.5
)

class Review(TypedDict):

    summary: Annotated[str, " A brief summary of the provided review"]
    sentiment: Annotated[str, "return sentiment of the review either negative, positive or neutral"]

structured_model = chat_model.with_structured_output(Review)

result = structured_model.invoke('''This movie felt like a complete waste of time—slow, predictable, and painfully dull from start to finish.
Even the decent visuals couldn’t save a story that dragged on without any real payoff. ''')  # important point over here that I have called structured_model not chat_model. 

print(result)  # getting primted in the form of dictionery only 
