from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder

# chat template

chat_template = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful customer {chat_template} support chat bot'),
    MessagesPlaceholder(variable_name='chat_template'),  # loads all the previous chat histroy stored in db, messageplaceholer a key and looks for it 
    ('human', '{query}')
])

# Load chat history

chat_history = []
with open('01_Components/04_Messages/02.01_chat_history.txt') as f:
    chat_history.extend(f.read().splitlines()) 

print(chat_history)

# create prompt 

prompt = chat_template.invoke({'chat_history_1': chat_history, 'query': 'Where is my refund ?'})

print(prompt)