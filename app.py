import streamlit as st

# --- PAGE SETUP ---
intro_page = st.Page(
    "views/intro.py",
    title="The 5 Levels of AI Agents",
    icon="🤖",
    default=True,
)
agno_page_1 = st.Page(
    "views/agno1.py",
    title="Level #1: Tools and Instructions",
    icon="🧭",
)
agno_page_1b = st.Page(
    "views/agno1b.py",
    title="Level #1b: Tools, Instructions, and Context",
    icon="🧭",
)
agno_page_2 = st.Page(
    "views/agno2.py",
    title="Level #2: Knowledge and Storage",
    icon="🧭",
)
agno_page_3 = st.Page(
    "views/agno3.py",
    title="Level #3: Memory and Reasoning",
    icon="🧭",
)
agno_page_4 = st.Page(
    "views/agno4.py",
    title="Level #4: Multi Agent Team",
    icon="🧭",
)
agno_page_5 = st.Page(
    "views/agno5.py",
    title="Level #5: Agentic Systems",
    icon="🧭",
)

# --- NAVIGATION SETUP [WITH SECTIONS]---
pg = st.navigation(
    {
        "Agno Agents": [intro_page],
        "Agno Demos": [
            agno_page_1,
            agno_page_1b,
            agno_page_2,
            agno_page_3,
            agno_page_4,
            agno_page_5,
        ],
    }
)

# --- SHARED ON ALL PAGES ---
st.sidebar.markdown("## Resources")
st.sidebar.markdown(
    """
    * [Agno Documentation](https://docs.agno.com/)
    * [Agno on GitHub](https://github.com/agno-agi/agno)
    * [Agno Cookbook](https://github.com/agno-agi/agno/tree/main/cookbook)
    """
)

# Add separator and space between resources and attribution
st.sidebar.markdown("---")
st.sidebar.markdown("")  # Empty line for spacing

# Attribution with slightly enhanced styling
st.sidebar.markdown(
    "<div style='text-align: center; margin-top: 10px;'>Made with ❤️ by <a href='https://hiremax.now'>Max Braglia</a></div>",
    unsafe_allow_html=True,
)

# Running the app
pg.run()
