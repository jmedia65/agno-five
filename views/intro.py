import streamlit as st
import streamlit as st
from pathlib import Path

# Header section
st.title("🤖 The 5 Levels of AI Agents")

# Introduction and attribution
st.markdown(
    """
### Inspired by [Ashpreet Bedi](https://x.com/ashpreetbedi), CEO of [Agno](https://agno.com)

This project is based on a social media post by Ashpreet Bedi that outlines the progressive complexity
of AI agents. The concept: **always start with level 1 and add complexity as needed**.

---
"""
)

# Create columns for a cleaner layout
col1, space1, col2 = st.columns([5, 0.5, 5])

with col1:
    # Level 1
    st.markdown("## Level 1: Agent with tools and instructions")

    st.info(
        """
    "When people say agents are just LLM + tool calls in a loop, this is what they mean (this also tells you their level of understanding)."
    
    **Instructions** "teach" the Agent how to achieve its task and **tools** let Agents interact with external environments 
    to push or pull data.
    """
    )

    if Path("views/agno1.py").exists() or Path("agno1.py").exists():
        if st.button("Explore Level 1 Demo", key="level1_btn"):
            st.switch_page("views/agno1.py")

with col2:
    # Level 2
    st.markdown("## Level 2: Agent with knowledge and storage")

    st.info(
        """
    Rarely does a model have all the information it needs to achieve its task, and we obviously can't jam everything 
    in the context, so we give the Agent knowledge that it searches at runtime (i.e., Agentic RAG or Dynamic few-shot).
    
    **Knowledge search** needs to be hybrid (full-text and semantic). Hybrid search + reranking is the best 
    out-of-the-box Agentic Search strategy.
    
    **Storage** saves the Agent's state in a database, making "stateless" LLM calls "stateful" by storing messages.
    """
    )

    if Path("views/agno2.py").exists() or Path("agno2.py").exists():
        if st.button("Explore Level 2 Demo", key="level2_btn"):
            st.switch_page("views/agno2.py")

st.markdown("---")

col3, space2, col4 = st.columns([5, 0.5, 5])

with col3:
    # Level 3
    st.markdown("## Level 3: Agent with memory and reasoning")

    st.info(
        """
    **Memory** lets an Agent remember details about a user and personalize its responses across sessions.
    This is a fairly new concept that everyone is still exploring.
    
    **Reasoning** is a key feature that every agent builder should know when and how to use. It improves 
    cognitive reasoning (understanding of data and instructions) and increases the success rate of each step.
    """
    )

    if Path("views/agno3.py").exists() or Path("agno3.py").exists():
        if st.button("Explore Level 3 Demo", key="level3_btn"):
            st.switch_page("views/agno3.py")

with col4:
    # Level 4
    st.markdown("## Level 4: Multi Agent Teams")

    st.info(
        """
    Agents work best when they have a narrow scope (specialized to a domain) and a reasonably small set of tools (<10).
    By putting agents together in a team, we can increase overall capabilities and solve broader, more complex problems.
    
    Add reasoning, otherwise the Team leader struggles with complex tasks. Current (2025) belief is that 
    autonomous multi-agent teams work less than half the time.
    
    Agno provides an industry-leading multi-agent architecture with 3 modes: coordinate, route, and collaborate.
    """
    )

    if Path("views/agno4.py").exists() or Path("agno4.py").exists():
        if st.button("Explore Level 4 Demo", key="level4_btn"):
            st.switch_page("views/agno4.py")

st.markdown("---")

# Level 5 (full width)
st.markdown("## Level 5: Agentic Systems")

st.info(
    """
**APIs** (servers) that take in a request, asynchronously complete the task, and stream back the result.
These are hard to implement - when the request comes in, we need to save the state in a database, 
trigger an async job, and stream results back as they're ready.

Websockets can work here, but they are not an easy tech to work with. Agentic systems is where the money is, 
and what everyone is trying to build. Agno has released the Agent API, Agent UI, and detailed documentation 
to help AI engineers build better systems.
"""
)

if Path("views/agno5.py").exists() or Path("agno5.py").exists():
    if st.button("Explore Level 5 Demo", key="level5_btn"):
        st.switch_page("views/agno5.py")

# Footer and final quote
st.markdown("---")
st.markdown(
    """
> "Always start with level 1 and add complexity as needed." - Ashpreet Bedi, CEO of Agno

This project was created to demonstrate these concepts in action.
"""
)

# Additional links and resources
with st.expander("Resources", expanded=False):
    st.markdown(
        """
    * [Agno Documentation](https://docs.agno.com/)
    * [Agno on GitHub](https://github.com/agno-agi/agno)
    * [Follow Agno on X](https://x.com/agnoagi)
    """
    )
