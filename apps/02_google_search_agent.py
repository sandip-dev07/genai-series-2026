from dotenv import load_dotenv
load_dotenv()

from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langchain_community.utilities.google_serper import GoogleSerperAPIWrapper
from langchain_core.tools import tool

# checkpoint
from langgraph.checkpoint.memory import InMemorySaver


search = GoogleSerperAPIWrapper()


@tool
def google_search(query: str) -> str:
    """Search Google and return relevant search results."""
    return search.run(query)


llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
)


agent = create_agent(
    model=llm,
    tools=[google_search],
    system_prompt="""
You are a research assistant.

Use Google Search whenever the question requires current
or factual information.

Answer the user's question based on the search results.
If something cannot be verified, clearly say so.

Give a concise, direct answer.
""",
checkpointer=InMemorySaver(),
)

thread_config = {
    "configurable": {
        "thread_id": "google-search-cli",
    }
}

while True:
    query = input("Your Query: ")
    
    if query.strip().lower() == "exit":
        break
    
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": query,
                }
            ]
        },
        config=thread_config,
    )

    print(response)
