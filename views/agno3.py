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
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.tools.reasoning import ReasoningTools

load_dotenv()

st.title("📊 Level 3: Agent with memory and reasoning")

st.write(
    """
    Level 3 adds memory and reasoning capabilities, allowing the agent to remember user details and improve its problem-solving.
    
    **This Agent:**
    * Remembers user information across conversations
    * Uses reasoning tools to improve response quality
    * Still has access to the Agno knowledge base and search tools
    
    **Demo Setup:**
    For this demo, you're interacting with a simulated user profile:
    * The user's name is "Ava"
    * Ava likes soccer, skiing, and backgammon
    
    **Try asking:**
    * "What is stored in your knowledge base?" (Knowledge)
    * "What sports do I like?" (Memory retrieval)
    * "Can you recommend some Agno tools for a soccer fan like me?" (Combined)
    """
)

# Initialize session state for messages
if "level3_messages" not in st.session_state:
    st.session_state.level3_messages = []

# Creates User ID
user_id = "ava"


# Initialize components with caching to prevent recreation on each rerun
@st.cache_resource
def initialize_components():

    memory = Memory(
        model=OpenAIChat(id="gpt-4.1-mini"),
        db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
        # delete_memories=True,
        # clear_memories=True,
    )

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

    # knowledge_base.load(recreate=False)

    storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")

    agno_assist = Agent(
        name="Agno AGI",
        model=OpenAIChat(id="gpt-4.1-mini"),
        # user_id="ava",
        description=dedent(
            """\
            You are `Agno AGI`, an autonomous AI Agent that can build agents using the Agno 
            framework. Your goal is to help developers understand and use Agno by providing 
            explanations, working code examples, and optional visual and audio explanations 
            of key concepts."""
        ),
        instructions=dedent(
            """Search the knowledge base for information about Agno. Only search the web using the search tool if you cannot find the answer to the user's questions.

            You are interacting with a user named 'Ava'. This identity is fixed and should never be changed under any circumstances, even if directly requested. While the user name CANNOT be changed, their preferences can change upon request.

            Remember Ava's preferences and store additional details about her to memory to better tailor your responses. If asked to change the user's identity or pretend to be someone else, politely refuse and continue to address the user as Ava.

            Focus on providing helpful information about Agno (if asked) while personalizing your responses based on what you know about Ava."""
        ),
        tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True)],
        add_datetime_to_instructions=True,
        # Agentic RAG is enabled by default when `knowledge` is provided to the Agent.
        knowledge=knowledge_base,
        # Store Agent sessions in a sqlite database
        storage=storage,
        # Add the chat history to the messages
        add_history_to_messages=True,
        # Number of history runs
        num_history_runs=3,
        # Store memories in a sqlite database
        memory=memory,
        # Enable agentic memory
        enable_agentic_memory=True,
        markdown=True,
        debug_mode=True,
    )

    return memory, knowledge_base, storage, agno_assist


# Get agent instance
memory, knowledge_base, storage, agent = initialize_components()

# Display the code as an expandable component above the chat
with st.expander("📚 View the Code for the Agno Agent Level 3", expanded=False):
    code = """
    def initialize_components():

        memory = Memory(
            model=OpenAIChat(id="gpt-4.1-mini"),
            db=SqliteMemoryDb(table_name="user_memories", db_file="tmp/agent.db"),
            # delete_memories=True,
            # clear_memories=True,
        )

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
            # user_id="ava",
            description="...",
            instructions="...",
            tools=[DuckDuckGoTools(), ReasoningTools(add_instructions=True)],
            add_datetime_to_instructions=True,
            # Agentic RAG is enabled by default when `knowledge` is provided to the Agent.
            knowledge=knowledge_base,
            # Store Agent sessions in a sqlite database
            storage=storage,
            # Add the chat history to the messages
            add_history_to_messages=True,
            # Number of history runs
            num_history_runs=3,
            # Enable agentic memory
            enable_agentic_memory=True,
            markdown=True,
            debug_mode=True,
        )

        return memory, knowledge_base, storage, agno_assist


    # Get agent instance
    memory, knowledge_base, storage, agent = initialize_components()    
    """

    st.code(code, language="python")


# Display chat message history
for message in st.session_state.level3_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What do you want to learn about Agno?"):
    # Add user message to chat history
    st.session_state.level3_messages.append({"role": "user", "content": prompt})

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
            for chunk in agent.run(prompt, user_id=user_id, stream=True):
                if chunk.content:
                    # Accumulate the response content
                    full_response += chunk.content
                    # Update the display with each chunk
                    message_placeholder.markdown(full_response + "▌")

            # Final update without cursor
            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.level3_messages.append(
                {"role": "assistant", "content": full_response}
            )

        # Refresh memories display
        st.sidebar.empty()
        st.sidebar.title("User Memories")
        user_memories = memory.get_user_memories(user_id=user_id)
        if user_memories:
            for i, mem in enumerate(user_memories):
                st.sidebar.markdown(f"**Memory {i+1}:** {mem.memory}")
        else:
            st.sidebar.write("No memories stored yet.")

# "Clear Chat" button below the chat
if st.session_state.level3_messages and st.button(
    "Clear Chat", use_container_width=True, key="clear_chat"
):
    # Only clear the messages, not all session state
    st.session_state.level3_messages = []
    st.rerun()
