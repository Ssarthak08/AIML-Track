# Dynamic --> user gives teh tone and we have general template and the user's query gets fit inside it 
from langchain_core.prompts import ChatPromptTemplate

# In chatpromptTemplate we just pass a tuple stating the roles and the content, and put placeholers 

chat_template = ChatPromptTemplate.from_messages([
    ('system', 'You are a helpful {domain} expert'),
    ('human', 'Explain me in simple terms what is {topic}')
])

prompt = chat_template.invoke({'domain' : 'cricket', 'topic' : 'bat'})
print(prompt)