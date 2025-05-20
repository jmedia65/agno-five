import streamlit as st

st.title("📊 Level 5: Agentic Systems")
st.write(
    """
    APIs that take requests, asynchronously complete tasks, and stream back results. This is the most advanced 
    level of agent implementation, where your agents become production services.
    """
)

# Two-column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Agent API")
    st.info(
        """
        A robust, production-ready application for serving Agents as an API:
        
        * FastAPI server for handling API requests
        * PostgreSQL database for storage
        * Pre-built Agents to use as starting points
        * Docker-based setup for easy deployment
        """
    )
    st.markdown("[GitHub: Agent API](https://github.com/agno-agi/agent-api)")

with col2:
    st.subheader("Agno Workspaces")
    st.info(
        """
        Standardized codebases for production Agentic Systems:
        
        * REST API for serving Agents, Teams and Workflows
        * Admin interface for testing and debugging
        * Database for session and vector storage
        * Production-ready deployment options
        """
    )
    st.markdown(
        "[Documentation: Workspaces](https://docs.agno.com/workspaces/introduction)"
    )

st.markdown("---")

st.markdown(
    """
    ### Why Agentic Systems Matter
    
    Agentic systems represent the commercial end-point of agent development:
    
    * They handle request routing, state management, and asynchronous processing
    * They provide robust APIs that other services can consume
    * They manage database connections, scaling, and deployment
    * They incorporate monitoring, evaluation, and continuous improvement
    
    As Ashpreet Bedi noted: "Agentic systems is where the $ is and what everyone is trying to build."
    """
)

st.markdown("---")

st.markdown(
    """
    ### Getting Started
    
    1. Explore the [Agent API](https://github.com/agno-agi/agent-api) for a production-ready foundation
    2. Learn about [Agno Workspaces](https://docs.agno.com/workspaces/introduction) for standardized codebases
    3. Start with the `agent-app` template: `ag ws create` (via Agno CLI)
    4. Run locally using Docker: `ag ws up`
    5. Deploy to AWS: `ag ws up prd:aws`
    """
)
