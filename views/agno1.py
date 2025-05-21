import streamlit as st
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()

st.title("📊 Level 1: Agent with tools and instructions")

st.write(
    """
    Instructions 'teach' the Agent how to achieve its task and tools let Agents interact with external environments to push or pull data.
    
    **This Agent:**
    * Has access to web search through DuckDuckGo
    * Is configured to explain the Agno framework
    * Can provide code examples and explanations
    
    **Try asking:**
    * "What is Agno and what can it do?"
    * "Show me an example of creating a simple Agno agent"
    * "How do Agno agents use tools?"
    """
)

# Initialize session state for messages
if "level1_messages" not in st.session_state:
    st.session_state.level1_messages = []


# Initialize components with caching to prevent recreation on each rerun
@st.cache_resource
def initialize_components():

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
        instructions="Search the web for information about Agno.",
        tools=[DuckDuckGoTools()],
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=True,
    )

    return agno_assist


# Get agent instance
agent = initialize_components()

# Display the code as an expandable component above the chat
with st.expander("📚 View the Code for the Agno Agent Level 1", expanded=False):
    code = """
    def initialize_components():
    
        agno_assist = Agent(
            name="Agno AGI",
            model=OpenAIChat(id="gpt-4.1-mini"),
            description=dedent(
                \"""You are `Agno AGI`, an autonomous AI Agent that can build agents using the Agno 
                framework. Your goal is to help developers understand and use Agno by providing 
                explanations, working code examples, and optional visual and audio explanations 
                of key concepts.\"""
            ),
            instructions="Search the web for information about Agno.",
            tools=[DuckDuckGoTools()],
            add_datetime_to_instructions=True,
            markdown=True,
            debug_mode=True,
        )
    
        return agno_assist
    
    # Get agent instance
    agent = initialize_components()
    """

    st.code(code, language="python")


# Display chat message history
for message in st.session_state.level1_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("What do you want to learn about Agno?"):
    # Add user message to chat history
    st.session_state.level1_messages.append({"role": "user", "content": prompt})

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
            st.session_state.level1_messages.append(
                {"role": "assistant", "content": full_response}
            )

# "Clear Chat" button below the chat
if st.session_state.level1_messages and st.button(
    "Clear Chat", use_container_width=True, key="clear_chat"
):
    # Only clear the messages, not all session state
    st.session_state.level1_messages = []
    st.rerun()
