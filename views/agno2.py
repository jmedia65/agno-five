import streamlit as st
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.knowledge.url import UrlKnowledge
from agno.vectordb.lancedb import LanceDb, SearchType
from agno.embedder.openai import OpenAIEmbedder

# from agno.reranker.cohere import CohereReranker
from agno.storage.sqlite import SqliteStorage

load_dotenv()

st.title("📊 Level 2: Agent with knowledge and storage")
st.write(
    "Rarely does a model have all the information it needs to achieve its task and we obviously can't jam everything in the context, so we give the Agent knowledge that it searches at runtime (i.e Agentic RAG or Dynamic few-shot)."
)

# Initialize session state for messages
if "level2_messages" not in st.session_state:
    st.session_state.level2_messages = []


# Initialize components with caching to prevent recreation on each rerun
@st.cache_resource
def initialize_components():

    knowledge_base = UrlKnowledge(
        urls=["https://docs.agno.com/introduction.md"],
        vector_db=LanceDb(
            uri="tmp/lancedb",
            table_name="agno_docs",
            search_type=SearchType.hybrid,
            embedder=OpenAIEmbedder(id="text-embedding-3-small"),
            # reranker=CohereReranker(model="rerank-multilingual-v3.0"),
        ),
    )

    knowledge_base.load(recreate=False)

    storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

    agno_assist = Agent(
        name="Agno AGI",
        model=OpenAIChat(id="gpt-4.1-mini"),
        description=dedent(
            """\
            You are `Agno AGI`, an autonomous AI Agent that can build agents using the Agno 
            framework. Your goal is to help developers understand and use Agno by providing 
            explanations, working code examples, and optional visual and audio explanations 
            of key concepts."""
        ),
        instructions="Search the knowledge base for information about Agno. Only search the web using the search tool if you cannot find the answer to the user's questions.",
        tools=[DuckDuckGoTools()],
        add_datetime_to_instructions=True,
        # Agentic RAG is enabled by default when `knowledge` is provided to the Agent.
        knowledge=knowledge_base,
        # Store Agent sessions in a sqlite database
        storage=storage,
        # Add the chat history to the messages
        add_history_to_messages=True,
        # Number of history runs
        num_history_runs=3,
        markdown=True,
        debug_mode=True,
    )

    return knowledge_base, storage, agno_assist


# Get agent instance
knowledge_base, storage, agent = initialize_components()

# Display the code as an expandable component above the chat
with st.expander("📚 View the Code for the Agno Agent Level 2", expanded=False):
    code = """
    def initialize_components():

        knowledge_base = UrlKnowledge(
            urls=["https://docs.agno.com/introduction.md"],
            vector_db=LanceDb(
                uri="tmp/lancedb",
                table_name="agno_docs",
                search_type=SearchType.hybrid,
                embedder=OpenAIEmbedder(id="text-embedding-3-small"),
                reranker=CohereReranker(model="rerank-multilingual-v3.0"),
            ),
        )

        storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

        agno_assist = Agent(
            name="Agno AGI",
            model=OpenAIChat(id="gpt-4.1-mini"),
            description=...,
            instructions=...,
            tools=[DuckDuckGoTools()],
            add_datetime_to_instructions=True,
            # Agentic RAG is enabled by default when `knowledge` is provided to the Agent.
            knowledge=knowledge_base,
            # Store Agent sessions in a sqlite database
            storage=storage,
            # Add the chat history to the messages
            add_history_to_messages=True,
            # Number of history runs
            num_history_runs=3,
            markdown=True,
            debug_mode=True,
        )

        return knowledge_base, storage, agno_assist

    # Get agent instance
    agent = initialize_components()    
    """

    st.code(code, language="python")


# Display chat message history
for message in st.session_state.level2_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What do you want to learn about Agno?"):
    # Add user message to chat history
    st.session_state.level2_messages.append({"role": "user", "content": prompt})

    # Display user message in chat
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process and display agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            # Create a placeholder for the streaming response
            message_placeholder = st.empty()
            full_response = ""
            # Get streaming response instead of waiting for complete response
            for chunk in agent.run(prompt, stream=True):
                if chunk.content:
                    # Accumulate the response content
                    full_response += chunk.content
                    # Update the display with each chunk
                    message_placeholder.markdown(full_response + "▌")

            # Final update without cursor
            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.level2_messages.append(
                {"role": "assistant", "content": full_response}
            )

# "Clear Chat" button below the chat
if st.session_state.level2_messages and st.button(
    "Clear Chat", use_container_width=True, key="clear_chat"
):
    # Only clear the messages, not all session state
    st.session_state.level2_messages = []
    st.rerun()
