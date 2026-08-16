from dotenv import load_dotenv
load_dotenv()

import streamlit as st

from langchain_groq import ChatGroq
from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import AIMessage



# DATABASE
db = SQLDatabase.from_uri("sqlite:///tasks.db")

db.run(
    """
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        status TEXT CHECK (
            status IN ('pending', 'in_progress', 'completed')
        ) DEFAULT 'pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """
)



# MEMORY
if "memory" not in st.session_state:
    st.session_state.memory = InMemorySaver()

memory = st.session_state.memory

# LLM
llm = ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.3,
)

# TOOLS
toolkit = SQLDatabaseToolkit(
    db=db,
    llm=llm
)

tools = toolkit.get_tools()



# SYSTEM PROMPT
system_prompt = """
You are a task management assistant that interacts with a SQL database
containing a 'tasks' table.

TASK RULES:

1. Limit SELECT queries to 10 results maximum.
2. For task lists, use ORDER BY created_at DESC.
3. After CREATE, UPDATE, or DELETE operations, confirm the operation
   with a SELECT query.
4. If the user requests a list of tasks, present the output in a
   structured table format.

CRUD OPERATIONS:

CREATE:
    INSERT INTO tasks(title, status)

READ:
    SELECT * FROM tasks
    WHERE ...
    ORDER BY created_at DESC
    LIMIT 10

UPDATE:
    UPDATE tasks
    SET status=?
    WHERE id=? OR title=?

DELETE:
    DELETE FROM tasks
    WHERE id=? OR title=?

TABLE SCHEMA:

id
title
status (pending/in_progress/completed)
created_at
"""



# AGENT
agent = create_agent(
    llm,
    tools,
    checkpointer=memory,
    system_prompt=system_prompt
)



# THREAD CONFIG
thread_config = {
    "configurable": {
        "thread_id": "sql-agent",
    }
}



# UI
st.subheader("AI Task Manager")


# CHAT HISTORY
if "messages" not in st.session_state:
    st.session_state.messages = []


for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])


query = st.chat_input("Ask me things about your tasks")


if query:

    # USER MESSAGE
    with st.chat_message("user"):
        st.markdown(query)

    st.session_state.messages.append(
        {
            "role": "user",
            "content": query
        }
    )


    # AI MESSAGE
    with st.chat_message("ai"):

        with st.spinner("Thinking..."):

            response = agent.invoke(
                {
                    "messages": [
                        {
                            "role": "user",
                            "content": query
                        }
                    ]
                },
                config=thread_config,
            )
            
            print(response)


            
            # GET FINAL AI MESSAGE
            ai_response = None

            for message in reversed(response["messages"]):

                if isinstance(message, AIMessage):

                    ai_response = message.content
                    break


            if ai_response:

                st.markdown(ai_response)

                st.session_state.messages.append(
                    {
                        "role": "ai",
                        "content": ai_response
                    }
                )