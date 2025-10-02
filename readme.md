# Lucidya AI-Driven Marketing System Prototype

[![Streamlit](https://img.shields.io/badge/Streamlit-FF6B35?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/) [![LangChain](https://img.shields.io/badge/LangChain-007BFF?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com/) [![Ollama](https://img.shields.io/badge/Ollama-0A0A0A?style=for-the-badge&logo=ollama&logoColor=white)](https://ollama.com/) [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)

## Overview

AI-driven marketing automation system that identifies potential companies, gathers intelligence, finds decision-makers, generates personalized outreach, and manages email communications through a sequential pipeline of six specialized agents.

Key use case: Target E-Commerce, Retail Tech, and Healthcare companies in the GCC, identifying pain points like sentiment analysis in Arabic dialects, and crafting emails highlighting Lucidya's solutions (e.g., Social Listening, Arabic NLP).

## Features

- **Company Discovery**: Filters by industry, size (100+ employees), growth signals.
- **LLM-Powered Research**: Generates key insights, opportunity areas via RAG.
- **Personalized Outreach**: Crafts cold emails with pain points, use cases, CTA.
- **Email Response Handling**: Classifies replies, auto-responds or escalates.
- **Interactive UI**: Streamlit dashboard with metrics, expandable company cards, email previews.
- **Fallbacks**: Graceful handling of LLM failures with mock data/templates.
- **Export**: JSON output of full results.
- **Modular Design**: Agents for easy extension (e.g., LinkedIn API).

## Tech Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| **Core Framework** | Python 3.11+ | Application logic |
| **LLM Integration** | LangChain + Ollama (Llama 3) | Structured generation & parsing |
| **Workflow Orchestration** | LangGraph | Stateful graph-based execution |
| **UI** | Streamlit | Interactive dashboard |
| **Data Models** | Dataclasses + Pydantic | Typed structures & validation |
| **Utilities** | JSON, Re (regex) | Export & parsing helpers |
| **Databases** | PostgreSQL (data), ChromaDB (vectors) | Storage & RAG |
| **APIs** | Perplexity (discovery), Hunter.io (email verify), SendGrid/AWS SES (delivery), Calendly (scheduling) | Integrations |
| **Infrastructure** | Docker + Kubernetes | Deployment |
| **Dependencies** | See `requirements.txt` | Full list below |

### Dependencies
Install via `pip install -r requirements.txt`:
```
dataclasses
ollama>=0.1.0
langchain>=0.2.0
langgraph>=0.0.30
langchain-ollama>=0.0.1
streamlit>=1.30.0
pydantic
requests
beautifulsoup4
chromadb
sendgrid
python-calendly
python-dotenv
```

## Installation

1. **Clone/Setup Repo**:
   ```
   git clone <your-repo-url> lucidya-marketing-app
   cd lucidya-marketing-app
   ```

2. **Virtual Environment** (Recommended):
   ```
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. **Install Dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Configure APIs** (`.env` file):
   ```
   PERPLEXITY_API_KEY=your_key
   HUNTER_API_KEY=your_key
   SENDGRID_API_KEY=your_key
   CALENDLY_API_KEY=your_key
   ```

5. **Start Ollama**:
   - Download: https://ollama.com/
   - Run: `ollama run llama3`
   - Verify: `ollama list`

6. **Folder Structure**:
   ```
   lucidya-marketing-app/
   ├── requirements.txt
   ├── streamlit_app.py          # Main UI entry
   ├── config.py                 # LLM & app config
   ├── models.py                 # Data classes
   ├── data/
   │   └── mock_data.py          # Sample companies/contacts (fallback)
   ├── agents/                   # Modular agents
   │   ├── __init__.py
   │   ├── discovery_agent.py    # Perplexity integration
   │   ├── research_agent.py     # RAG enrichment
   │   ├── outreach_agent.py     # LLM email generation
   │   └── email_handler_agent.py # Response handling + Calendly
   ├── graph.py                  # LangGraph workflow
   └── utils.py                  # Helpers (export, serialization)
   ```

## Usage

1. **Run the App**:
   ```
   streamlit run streamlit_app.py
   ```
   - Opens at http://localhost:8501.

2. **Interact in UI**:
   - **Sidebar**: Adjust "Min Fit Score" (default 85); toggle "Run Email Handling Demo".
   - **Main**: Click **"Run Workflow"** to execute (discovery → enrichment → outreach → handoff).
     - Progress: Spinner for API calls/RAG.
     - Outputs: Metrics, company cards (insights/challenges), email previews.
   - **Export**: Auto-saves `lucidya_marketing_system_output.json`.

3. **CLI Mode** (Optional):
   ```python
   from graph import build_graph
   from utils import export_results
   from data.mock_data import MOCK_COMPANIES

   graph = build_graph()
   state = graph.invoke({"companies": MOCK_COMPANIES})
   export_results(state)
   ```
   Run: `python main.py`.

4. **Customization**:
   - **Real Data**: Enable APIs in `.env`; replace mocks.
   - **LLM Model**: Edit `config.py` → `OLLAMA_MODEL = 'llama3.1'`.
   - **Extend**: Add CRM push in `handoff_node` (graph.py).

## Architecture

### Agent Breakdown
1. **Company Discovery**: Perplexity API query → Filter (industry/size/growth) → Qualified list.
2. **Data Enrichment**: RAG query + scraping → Extract (challenges/tech stack) → Enriched profiles.
3. **Decision Maker Identification**: LinkedIn API/scraping → Target roles (CMO/VP) → Contact list.
4. **Outreach Generation**: LLM personalization → Subject/value/CTA → Email content.
5. **Communication Management**: Reply classification → Auto-response/booking/escalation → Tracked history.
6. **Handoff**: Lead scoring → CRM push (Salesforce/HubSpot) → Notify team.

### Workflow
Sequential with retries:
- Discovery → Enrichment → Identification.
- Generate/Send Email → Handle Reply (loop on no reply/standard; branch on booking/escalation).
- Handoff → End.

**Text Diagram**:
```
Discovery (Perplexity) → Enrichment (RAG/Scrape) → Identification (LinkedIn)
↓
Outreach (LLM) → Send (SendGrid) → Reply Handler (Classify)
↓ (Branch)
No Reply/Standard → Loop | Booking → Calendly | Complex → Escalate
↓
Handoff (CRM Push) → End
```

### Technical Considerations
- **Data Freshness**: Real-time scraping; cache 7d static/24h dynamic; email verification.
- **Reliability**: API redundancy; exponential backoff; stage validation.
- **Compliance/Ethics**: CAN-SPAM/CCPA; 7-day email gaps; public data only; 10% human review.

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| **API Errors** | Missing keys | Add to `.env`; test with `curl`. |
| **RAG Empty** | No ChromaDB | Pre-load vectors: `chroma add_documents()`. |
| **Parsing Failures** | LLM schema echo | Switch to llama3.1; debug raw output. |
| **Streamlit Crashes** | Imports | Restart; check circular imports. |
| **Fallbacks Trigger** | API downtime | Enable mocks; add retries. |

- **Logs**: Console for "⚠️" errors.
- **Debug**: `print(raw_output)` in chains.

## Contributing

1. Fork repo.
2. Branch: `git checkout -b feature/update-agent`.
3. Commit: `git commit -m 'Update agent'`.
4. Push/PR.

Guidelines: Type hints; tests (pytest); update README.

## License

MIT License. See [LICENSE](LICENSE).

## Acknowledgments

- LangChain/LangGraph: Workflow.
- Ollama: Local LLM.
- Streamlit: UI.

*Updated October 02, 2025. Built for MENA marketing.*