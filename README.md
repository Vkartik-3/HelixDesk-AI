# SupportX AI Assist

SupportX AI Assist is an intelligent IT ticket resolver that leverages Azure OpenAI, vector search, and agent-based automation to provide instant solutions to IT issues. If the AI cannot resolve an issue, it escalates the ticket to IT support via email.


<img width="1280" height="720" alt="Copy of Intellegent IT Ticket Resolver-Multiagent project-Autogen" src="https://github.com/user-attachments/assets/c41a7f2b-7a27-4e94-977f-8702dc1a2b05" />


## Features

- **Natural Language IT Support:** Users describe their IT issues in plain English.
- **Automated Ticket Classification:** Classifies issues into categories (e.g., Password Reset, Network Issue).
- **Knowledge Base Search:** Uses vector similarity search to find the most relevant solutions from a curated knowledge base.
- **Escalation Workflow:** Unresolved issues are automatically escalated to IT support via email, with ticket creation.
- **Streamlit UI:** User-friendly web interface for submitting issues and receiving solutions.

## Project Structure

```
.
├── app.py                      # Streamlit web app
├── group_chat.py               # Agent orchestration and group chat logic
├── agents/
│   ├── classifier_agent.py     # Ticket classification agent
│   ├── knowledge_base_agent.py # Knowledge base retrieval agent
│   └── notification_agnet.py   # Notification/escalation agent
├── tools/
│   ├── knowledge_base_tool.py  # Vector search tool for knowledge base
│   └── send_email.py           # Email escalation tool
├── utility/
│   ├── llm_config.py           # LLM configuration (Azure OpenAI)
│   └── prompt.py               # Prompts for agents
├── data/
│   └── knowledge_base.json     # IT solutions knowledge base
├── create_and_upload_index.py  # Script to create Azure Search index and upload data
├── agent_test.py               # Agent testing scripts
├── style.css                   # Custom UI styles
├── .env                        # Environment variables (Azure/OpenAI/Search keys)
├── requiremnets.txt            # Python dependencies
└── README.md                   # Project documentation
```

## Setup Instructions

1. **Clone the repository**


2. **Install dependencies**

   ```sh
   pip install -r requiremnets.txt
   ```

3. **Configure environment variables**

   - Copy `.env` and fill in your Azure OpenAI and Azure Search credentials.

4. **Create and upload the Azure Search index**

   ```sh
   python create_and_upload_index.py
   ```

5. **Run the Streamlit app**

   ```sh
   streamlit run app.py
   ```

6. **Open your browser**

   - Visit `http://localhost:8501` to use SupportX AI Assist.

## How It Works

- **User submits an IT issue** via the web UI.
- **Agents collaborate**: 
  - The classifier agent determines the issue category.
  - The knowledge base agent retrieves relevant solutions using vector search.
  - If the solution is not helpful, the notification agent escalates the issue via email.
- **Feedback loop**: Users can mark solutions as helpful or escalate if unresolved.

## Customization

- **Knowledge Base**: Edit [`data/knowledge_base.json`](data/knowledge_base.json) to add or update IT solutions.
- **Prompts**: Adjust agent behavior in [`utility/prompt.py`](utility/prompt.py).
- **Email Settings**: Configure SMTP credentials in [`tools/send_email.py`](tools/send_email.py).


## License

MIT License

---

**Developed by Sandesh Hase**

All rights reserved.
