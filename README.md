# Agno Five: The 5 Levels of AI Agents

![Agno Five Banner](https://placehold.co/1200x300?text=Agno+Five)

An interactive educational project demonstrating the 5 levels of AI agent architecture based on [Ashpreet Bedi](https://twitter.com/ashpreetbedi)'s framework. This project provides working demos for each level of agent complexity using the [Agno](https://agno.com) framework.

## 📚 Overview

This project demonstrates the progressive complexity of AI agents, from simple instruction-following tools to complete agentic systems. As Ashpreet Bedi notes: **"Always start with level 1 and add complexity as needed."**

Each level builds upon the previous one:

1. **Level 1:** Agent with tools and instructions
2. **Level 2:** Agent with knowledge and storage
3. **Level 3:** Agent with memory and reasoning
4. **Level 4:** Multi-agent teams
5. **Level 5:** Agentic systems

## 🛠️ Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/jmedia65/agno-five.git
   cd agno-five
   ```

2. Create a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create a `.env` file with your API keys:
   ```
   OPENAI_API_KEY=your_key_here
   ```

## 📋 Usage

Run the Streamlit app:

```bash
streamlit run app.py
```

Navigate through the different levels using the sidebar. Each level includes:

- An explanation of the concept
- A live chat demo showing the agent in action
- Code examples that you can expand to see how it's implemented

## 🧩 Project Structure

```
agno-five/
├── app.py            # Main Streamlit application
├── views/            # Individual level views
│   ├── intro.py      # Introduction and overview
│   ├── agno1.py      # Level 1: Agent with tools and instructions
│   ├── agno1b.py     # Level 1B: Enhanced agent with additional tools
│   ├── agno2.py      # Level 2: Agent with knowledge and storage
│   ├── agno3.py      # Level 3: Agent with memory and reasoning
│   ├── agno4.py      # Level 4: Multi-agent teams
│   └── agno5.py      # Level 5: Agentic systems
└── tmp/              # Storage for databases (not tracked in git)
```

## 💻 Development

- This project uses Streamlit for the UI
- The agents are built using the Agno framework
- Local file-based databases (SQLite and LanceDB) are used for storage and vector search

## 🌐 Deployment

This project can be deployed using Docker and Render:

### Local Docker Deployment

1. Build and run the Docker container locally:

   ```bash
   # Build and start the container
   docker-compose up --build
   ```

2. Access the application at http://localhost:8501

### Render Deployment with Persistent Storage

1. Create a Render account and connect your GitHub repository

2. Create a new Web Service:

   - Select "Docker" as the environment
   - Name your service (e.g., "agno-five")
   - Keep all other default Docker settings

3. Add environment variables:

   - Add `OPENAI_API_KEY` with your API key value

4. Create a disk for persistent storage:

   - In the "Disks" section, create a new disk
   - Set mount path to `/app/tmp`
   - Choose an appropriate size (start with 1GB)
   - This ensures your database files persist between deployments

5. Deploy your service:
   - Render will build and deploy your Docker container
   - Once complete, you'll get a URL to access your application

Note: For production deployment, consider:

- Creating API keys with usage limits
- Monitoring your disk usage as the vector database grows
- Adding proper error handling for API limits

## 🙏 Acknowledgments

- [Ashpreet Bedi](https://twitter.com/ashpreetbedi), CEO of Agno, for the "5 Levels of AI Agents" concept
- [Agno](https://agno.com) for their powerful agent framework
- All contributors to the open-source libraries used in this project

## 📄 License

MIT License

Copyright (c) 2025 [Max Braglia]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

Built with ❤️ by [Max Braglia](https://hiremax.now/)
