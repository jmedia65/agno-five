import streamlit as st
from dotenv import load_dotenv
from agno.agent import Agent
from agno.team import Team
from agno.models.openai import OpenAIChat
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools

load_dotenv()

st.title("📊 Level 4: Multi Agent Team")
st.write(
    "Agents work best when they have a narrow scope (i.e. specialized to a domain) and a reasonably small set of tools \
        (<10 ish). By putting agents together in a team, we can increase the overall capabilities and solve broader, \
            more complex problems. Remember to add reasoning, otherwise the Team leader struggles to work on complex tasks."
)

# Initialize session state for messages
if "level4_messages" not in st.session_state:
    st.session_state.level4_messages = []


# Initialize components with caching to prevent recreation on each rerun
@st.cache_resource
def initialize_components():

    # Create individual specialized agents
    financial_researcher = Agent(
        name="Researcher",
        role="Expert at finding and synthesizing financial information online",
        model=OpenAIChat("gpt-4.1-mini"),
        tools=[DuckDuckGoTools()],
        instructions=[
            "You are a financial research assistant responsible for gathering and organizing information for the Writer agent.",
            "When given a financial topic to research:",
            "1. Search for comprehensive, relevant, and current information using DuckDuckGoTools",
            "2. Organize the research findings into a detailed 'Knowledge Report' with clear sections",
            "3. Include key financial data, statistics, expert opinions, and market trends in your report",
            "4. Highlight contradicting viewpoints or diverse perspectives on the topic",
            "5. Always cite your sources clearly for each piece of information",
            "6. Format information for readability with bullet points and short paragraphs where appropriate",
            "7. Prioritize recent and authoritative sources in the financial sector",
            "8. Summarize complex financial concepts in accessible language",
            "9. Focus on finding information from reputable financial publications and institutions",
            "10. Structure your report to help the Writer create a comprehensive financial article",
        ],
    )

    financial_writer = Agent(
        name="Writer",
        role="Writes high-quality financial articles.",
        model=OpenAIChat("gpt-4.1-mini"),
        tools=[ReasoningTools(add_instructions=True)],
        description=(
            "You are a senior writer for highly respected Financial Advisors blog. Given a topic and relevant information from the Researcher Agent, "
            "your goal is to write a high-quality financial article on the topic."
        ),
        instructions=[
            "Wait for the Researcher Agent to provide you with information on the requested topic.",
            "Carefully analyze all provided information before starting your article.",
            "Write a comprehensive, well-researched financial article that would meet the standards of a respected financial publication.",
            "Structure your article with a compelling headline, clear introduction, well-organized body, and insightful conclusion.",
            "Include relevant financial data, trends, expert opinions, and market insights from the provided sources.",
            "Write for a financially literate audience while ensuring clarity on complex concepts.",
            "Aim for 1000-1500 words with proper paragraphing and section headers for readability.",
            "Incorporate balanced perspectives on financial matters, especially for investment-related topics.",
            "Strictly adhere to factual information from the sources - never fabricate quotes, statistics, or data.",
            "Properly attribute information to sources provided by the Researcher.",
            "Use a professional, authoritative tone appropriate for a respected financial publication.",
            "Consider timely relevance - reference current market conditions when appropriate.",
            "Conclude with key takeaways or actionable insights when relevant.",
        ],
        add_datetime_to_instructions=True,
    )

    # Create a team with these agents
    content_team = Team(
        name="Content Team",
        mode="coordinate",
        model=OpenAIChat("gpt-4.1-mini"),
        members=[financial_researcher, financial_writer],
        # show_members_responses=True,
        # enable_agentic_context=True,
        tools=[ReasoningTools(add_instructions=True)],
        instructions="""You are the Financial Content Team for a highly respected Financial Advisors blog. 
        Your team consists of specialized financial researchers and professional writers working together to create authoritative financial content.
        
        As team coordinator, you will:
        1. Manage the workflow between the Researcher and Writer agents
        2. Ensure the Researcher provides comprehensive and relevant financial information through online searches
        3. Guide the Writer to create exceptional financial articles based on the research findings
        4. Review and edit the final content for quality, clarity, and accuracy
        5. Ensure proper attribution of sources and factual integrity
        6. Polish the final article to meet professional publication standards
        7. Add value through your editorial oversight, suggesting improvements when needed
        8. Ensure the final content serves the financial literacy needs of your audience
        
        All content produced should maintain the authoritative tone, factual accuracy, and professional quality expected of a premier financial publication.
        """,
        markdown=True,
        debug_mode=True,
    )

    return financial_researcher, financial_writer, content_team


# Get agent instance
financial_researcher, financial_writer, content_team = initialize_components()

# Display the code as an expandable component above the chat
with st.expander("📚 View the Code for the Agno Agent Level 4", expanded=False):
    code = """
    def initialize_components():

        # Create individual specialized agents
        financial_researcher = Agent(
            name="Researcher",
            role="Expert at finding and synthesizing financial information online",
            model=OpenAIChat("gpt-4o"),
            tools=[DuckDuckGoTools()],
            instructions=[...],
        )

        financial_writer = Agent(
            name="Writer",
            role="Writes high-quality financial articles.",
            model=OpenAIChat("gpt-4o"),
            tools=[ReasoningTools(add_instructions=True)],
            description=[...],
            instructions=[...],
            add_datetime_to_instructions=True,
        )

        # Create a team with these agents
        content_team = Team(
            name="Content Team",
            mode="coordinate",
            model=OpenAIChat("gpt-4o"),
            members=[financial_researcher, financial_writer],
            show_members_responses=True,
            enable_agentic_context=True,
            tools=[ReasoningTools(add_instructions=True)],
            instructions=[...],
            markdown=True,
            debug_mode=True,
        )

        return financial_researcher, financial_writer, content_team


    # Get agent instance
    memory, knowledge_base, storage, content_team = initialize_components()
    """

    st.code(code, language="python")


# Display chat message history
for message in st.session_state.level4_messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
if prompt := st.chat_input("Create an article about big investing ideas for 2025"):
    # Add user message to chat history
    st.session_state.level4_messages.append({"role": "user", "content": prompt})

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
            for chunk in content_team.run(prompt, stream=True):
                if chunk.content:
                    # Accumulate the response content
                    full_response += chunk.content
                    # Update the display with each chunk
                    message_placeholder.markdown(full_response + "▌")

            # Final update without cursor
            message_placeholder.markdown(full_response)

            # Add assistant response to chat history
            st.session_state.level4_messages.append(
                {"role": "assistant", "content": full_response}
            )

# "Clear Chat" button below the chat
if st.session_state.level4_messages and st.button(
    "Clear Chat", use_container_width=True, key="clear_chat"
):
    # Only clear the messages, not all session state
    st.session_state.level4_messages = []
    st.rerun()
