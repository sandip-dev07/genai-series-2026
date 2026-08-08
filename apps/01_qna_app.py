from dotenv import load_dotenv
load_dotenv()

from langchain.chat_models import init_chat_model
import streamlit as st

model = init_chat_model(
    model="gemini-3.5-flash-lite",
    model_provider="google_genai"
)

# while True:
#     query = input("Your Query: ")
    
#     if(query == "exit"):
#         break
    
#     response = model.invoke(query)
#     print(response.content[0]["text"])


st.title("QnA App 🚀")    
st.markdown("QnA App powered by Langchain and Google GenAI")

# store the conversation history (session storage)
if "messages" not in st.session_state: 
    st.session_state.messages = []
    
# display the chat messages
for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    
    st.chat_message(role).write(content)

query = st.chat_input("Ask any question")

if query:
    st.chat_message("user").write(query)
    st.session_state.messages.append({"role": "user", "content": query})
    
    response = model.invoke(query)
    
    st.chat_message("assistant").write(response.content[0]["text"])
    st.session_state.messages.append({"role": "assistant", "content": response.content[0]["text"]})