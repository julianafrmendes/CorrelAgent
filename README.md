# CorrelAgent
Correl-Agent is an advanced AI agent built on the LlamaIndex framework using the ReAct (Reasoning and Action) architecture. It acts as an autonomous researcher for the Netherlands' Open Data Portal (overheid.nl).

Correl-Agent: Autonomous Data Discovery Specialist
1. Overview
Correl-Agent is an advanced AI agent built on the LlamaIndex framework using the ReAct (Reasoning and Action) architecture. It acts as an autonomous researcher for the Netherlands' Open Data Portal (overheid.nl).

Unlike standard search tools, this agent interprets user intent, queries a localized vector catalog, scrapes live metadata from web URLs, and formulates a grounded analytical plan based on real-world variables.

2. Technical Stack & Architecture
Reasoning Engine: ReAct Agent loop for multi-step problem solving.

Orchestration: LlamaIndex (Data Framework for LLMs).

LLM & Inference: Llama 3.1 (via Groq) for high-speed, low-latency reasoning.

Vector Search: Persistent VectorStoreIndex with Multilingual-E5 embeddings for semantic precision.

Live Web Scraping: SimpleWebPageReader for real-time extraction of Dutch dataset descriptions (Beschrijving).

3. Key Features
Intent Mapping: Translates natural language questions (e.g., "correlation between unemployment and education") into specific data search queries.

Fact-Grounded Planning: Explicitly avoids "hallucinating" variables; the agent only suggests analysis based on verified metadata.

Automated Workflow: Orchestrates three custom tools: search_catalog, read_dataset_details, and analyze_and_plan.

4. Roadmap & Future Enhancements (Vision)
User Experience (UI/UX)
Streamlit Interactive Dashboard: Transitioning from a CLI to a web-based interface where users can view the agent’s "thought process" logs and interactive data cards.

Multilingual Support: Enhancing the agent’s ability to bridge the gap between English queries and Dutch metadata.

Community Integration: Developing a Slack/Discord bot interface for real-time collaborative data discovery.

Deployment & Scalability
Dockerization: Containerizing the environment to ensure seamless deployment across cloud providers.

Serverless Architecture: Deploying via AWS Lambda or Google Cloud Functions to optimize costs and trigger execution via API webhooks.

CI/CD Pipeline: Implementing automated testing for tool reliability and index updates.

5. Quick Start
Dependencies: pip install llama-index llama-index-llms-groq llama-index-embeddings-huggingface nest-asyncio

Configuration: Place catalog_overheid.csv in the root directory and export your GROQ_API_KEY.

Execution: Run the script to initiate the asynchronous agent workflow.
