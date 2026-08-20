import os

from dotenv import load_dotenv

load_dotenv()

from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_groq import ChatGroq
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

import streamlit as st


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "docs" not in st.session_state:
    st.session_state["docs"] = False

if "agent" not in st.session_state:
    st.session_state["agent"] = None

if "vector_store" not in st.session_state:
    st.session_state["vector_store"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []


# ---------------------------------------------------------------------------
# Pipeline: load -> split -> embed -> vector store -> tool -> agent
# ---------------------------------------------------------------------------
def process_documents(path: str) -> None:
    try:
        # 1. Load documents
        loader = PyPDFDirectoryLoader(path)
        documents = loader.load()

        if not documents:
            st.error("No readable text found in the uploaded PDF(s).")
            return

        # 2. Split documents
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=600,
            chunk_overlap=100,
        )
        docs = text_splitter.split_documents(documents=documents)

        # 3. Create embeddings
        embeddings = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2-preview")

        # 4. Create vector store
        vector_store = InMemoryVectorStore.from_documents(
            documents=docs,
            embedding=embeddings,
        )
        st.session_state["vector_store"] = vector_store

        # 5. Create search tool
        @tool
        def search(query: str) -> str:
            """
            Search the resume and return relevant context.
            """
            results = vector_store.similarity_search(query=query, k=5)
            return "\n\n".join(doc.page_content for doc in results)

        # 6. Create LLM
        llm = ChatGroq(model="qwen/qwen3.6-27b", temperature=0)

        # 7. System prompt
        system_prompt = """
        You are a helpful assistant that answers questions about Sandip's resume.

        Use the search tool whenever the question requires information
        from the resume.

        Only answer using information that can be verified from the resume.

        If the answer cannot be found in the resume, say:
        "I couldn't find that information in the resume."
        """

        # 8. Memory
        memory = InMemorySaver()

        # 9. Create agent
        agent = create_agent(
            model=llm,
            tools=[search],
            system_prompt=system_prompt,
            checkpointer=memory,
        )

        st.session_state["agent"] = agent
        st.session_state["docs"] = True

    except Exception as e:
        st.error(f"Failed to process documents: {e}")
        st.session_state["docs"] = False
        st.session_state["agent"] = None


# ---------------------------------------------------------------------------
# Thread configuration
# ---------------------------------------------------------------------------
thread_config = {
    "configurable": {
        "thread_id": "rag-agent"
    }
}


# ---------------------------------------------------------------------------
# Streamlit UI
# ---------------------------------------------------------------------------
st.title("Resume Agent 🚀")
st.markdown("Resume Agent powered by Langchain and Google GenAI")

# File upload
if not st.session_state["docs"]:
    uploaded = st.file_uploader(
        label="Upload a PDF file",
        type=["pdf"],
        accept_multiple_files=True,
    )

    if uploaded:
        with st.spinner("Processing..."):
            path = "./doc_files/"
            os.makedirs(path, exist_ok=True)

            for file in uploaded:
                with open(os.path.join(path, file.name), "wb") as f:
                    f.write(file.getvalue())

            process_documents(path)

        if st.session_state["docs"]:
            st.rerun()

# Chat UI
if st.session_state["docs"] and st.session_state["agent"]:

    for message in st.session_state["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    query = st.chat_input("Your Query")

    if query:
        st.chat_message("user").markdown(query)
        st.session_state["messages"].append({"role": "user", "content": query})

        try:
            response = st.session_state["agent"].invoke(
                {"messages": [{"role": "user", "content": query}]},
                config=thread_config,
            )
            answer = response["messages"][-1].content
        except Exception as e:
            answer = f"Error while generating a response: {e}"

        st.chat_message("assistant").markdown(answer)
        st.session_state["messages"].append({"role": "assistant", "content": answer})