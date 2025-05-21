import streamlit as st
from textwrap import dedent
import httpx
import json
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools

load_dotenv()


st.title("📊 Level 1b: Agent with tools and instructions PLUS context")
st.write(
    "Agent Context is another amazing feature of Agno. context is a dictionary that contains a set of functions (or dependencies) \
        that are resolved before the agent runs.Instructions 'teach' the Agent how to achieve its task and tools \
            let Agents interact with external environments to push or pull data."
)

# Initialize session state for messages
if "level1b_messages" not in st.session_state:
    st.session_state.level1b_messages = []


@st.cache_data(ttl=600)  # Cache for 10 minutes
def get_top_hackernews_stories(num_stories: int = 5) -> str:
    """Fetch and return the top stories from HackerNews.

    Args:
        num_stories: Number of top stories to retrieve (default: 5)
    Returns:
        JSON string containing story details (title, url, score, etc.)
    """
    # First, get the list of top story IDs
    response = httpx.get("https://hacker-news.firebaseio.com/v0/topstories.json")
    all_story_ids = response.json()

    # Take only the first num_stories IDs
    top_story_ids = all_story_ids[:num_stories]

    # Create an empty list to store our story details
    stories = []

    # Loop through each story ID and get its details
    for story_id in top_story_ids:
        # Get the details for this story
        story_url = f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json"
        story_response = httpx.get(story_url)
        story_data = story_response.json()

        # Create a new dictionary for this story, excluding 'kids'
        filtered_story = {}
        for key, value in story_data.items():
            # Skip the 'kids' field which contains comment IDs
            if key != "kids":
                filtered_story[key] = value

        # Add this story to our list
        stories.append(filtered_story)

    # Convert the list of stories to a formatted JSON string
    return json.dumps(stories, indent=4)


# Initialize components with caching to prevent recreation on each rerun
@st.cache_resource
def initialize_components():

    agno_assist = Agent(
        name="Agno AGI",
        model=OpenAIChat(id="gpt-4.1-mini"),
        # Each function in the context is evaluated when the agent is run, think of it as dependency injection for Agents
        context={"top_hackernews_stories": get_top_hackernews_stories},
        instructions=dedent(
            """\
            You are an insightful tech trend observer! 📰

            Here are the top stories on HackerNews:
            {top_hackernews_stories}\
            
            Your job is to summarize the top stories on HackerNews on demand and provide details on them when asked. Use the search tool to find more information about specific news stories if you don't have enough information.
        """
        ),
        # add_state_in_messages will make the `top_hackernews_stories` variable available in the instructions
        add_state_in_messages=True,
        tools=[DuckDuckGoTools()],
        add_datetime_to_instructions=True,
        markdown=True,
        debug_mode=True,
    )

    return agno_assist


# Get agent instance
agent = initialize_components()

# Display the code as an expandable component above the chat
with st.expander("📚 View the Code for the Agno Agent Level 1b", expanded=False):
    code = """
    def initialize_components():

        agno_assist = Agent(
            name="Agno AGI",
            model=OpenAIChat(id="gpt-4.1-mini"),
            # Each function in the context is evaluated when the agent is run, think of it as dependency injection for Agents
            context={"top_hackernews_stories": get_top_hackernews_stories},
            instructions=dedent(
                \"""You are an insightful tech trend observer! 📰

                Here are the top stories on HackerNews:
                {top_hackernews_stories}
                            
                Your job is to summarize the top stories on HackerNews on demand and provide details on them when asked. Use the search tool to find more information about specific news stories if you don't have enough information.
            \"""
            ),
            # add_state_in_messages will make the `top_hackernews_stories` variable available in the instructions
            add_state_in_messages=True,
            tools=[DuckDuckGoTools()],
            add_datetime_to_instructions=True,
            markdown=True,
            debug_mode=True,
        )

        return agno_assist
    """

    st.code(code, language="python")


# Display chat message history
for message in st.session_state.level1b_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Summarize the top stories on HackerNews."):
    # Add user message to chat history
    st.session_state.level1b_messages.append({"role": "user", "content": prompt})

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
            st.session_state.level1b_messages.append(
                {"role": "assistant", "content": full_response}
            )

# "Clear Chat" button below the chat
if st.session_state.level1b_messages and st.button(
    "Clear Chat", use_container_width=True, key="clear_chat"
):
    # Only clear the messages, not all session state
    st.session_state.level1b_messages = []
    st.rerun()
