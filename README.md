# CorrelAgent

**Autonomous AI Agent for Discovering Relationships in Dutch Open Data**

CorrelAgent is an AI-powered research assistant designed to explore datasets from the Netherlands Open Data ecosystem.
Built with modern LLM infrastructure, the agent autonomously discovers relevant datasets, extracts metadata, and proposes grounded analytical strategies for correlation and exploratory analysis.

The goal is to help analysts, researchers, and civic-tech communities **quickly identify relationships between public variables** using the Dutch Open Data Portal.

---

# Overview

CorrelAgent is built using a **Reasoning + Action architecture (ReAct)** that allows the system to:

* Understand analytical questions in natural language
* Search structured dataset catalogs
* Retrieve metadata from real dataset sources
* Propose possible analytical paths based on verified variables

Instead of acting as a simple search tool, CorrelAgent behaves like a **data discovery researcher**.

Example question:

> *“Is there a relationship between unemployment levels and education indicators in Dutch regions?”*

The agent will:

1. Search the dataset catalog
2. Identify relevant datasets
3. Retrieve metadata directly from the source
4. Suggest possible variables for correlation analysis

---

# Architecture

The system combines modern AI orchestration tools with semantic search.

### Core Components

**Reasoning Engine**

ReAct agent loop for multi-step reasoning and tool execution.

**Agent Framework**

LlamaIndex orchestrates the data pipeline and tool interaction.

**Language Model**

Llama 3.1 running through Groq for fast inference and reasoning.

**Semantic Search**

VectorStoreIndex with multilingual E5 embeddings enables semantic retrieval across dataset descriptions.

**Live Metadata Extraction**

The agent reads real dataset descriptions from overheid.nl using a web scraping reader.

---

# Key Features

### Intelligent Dataset Discovery

The agent translates natural language questions into structured dataset searches.

### Fact-Grounded Analysis

CorrelAgent avoids hallucinating variables.
All analytical suggestions are derived from real dataset metadata.

### Autonomous Tool Workflow

The agent orchestrates a multi-step workflow using three custom tools:

* `search_catalog`
* `read_dataset_details`
* `analyze_and_plan`

---

# Project Architecture

```
User Question
      ↓
ReAct Agent
      ↓
Catalog Search Tool
      ↓
Dataset Metadata Extraction
      ↓
Analysis Planning
      ↓
Suggested Analytical Strategy
```

---

# Roadmap

## User Experience

**Interactive Dashboard**

Future versions will include a Streamlit interface where users can:

* visualize the agent reasoning process
* inspect dataset cards
* interactively explore discovered variables

**Multilingual Support**

Improved handling of English queries against Dutch dataset metadata.

**Community Integration**

Potential Slack or Discord interface to support collaborative data discovery within research communities.

---

## Deployment

**Docker**

Containerized environment for reproducible deployments.

**Serverless Execution**

Planned deployment options:

* AWS Lambda
* Google Cloud Functions

This will allow the agent to run as an API endpoint triggered by webhooks.

**CI/CD Pipeline**

Future versions will include automated testing for:

* dataset catalog updates
* tool reliability
* index refresh

---

# Quick Start

### Install dependencies

```
pip install llama-index llama-index-llms-groq llama-index-embeddings-huggingface nest-asyncio
```

### Configure environment

Place the dataset catalog file in the root directory:

```
catalog_overheid.csv
```

Then configure your API key:

```
export GROQ_API_KEY=your_api_key
```

### Run the agent

```
python agent3_pilot_test.py
```

The agent will start the reasoning loop and begin interacting with the dataset catalog.

---

# Vision

CorrelAgent aims to become a **data discovery layer for open government data**, helping analysts and civic-tech communities quickly identify relationships between public datasets.

By combining LLM reasoning with verified metadata retrieval, the project explores how AI agents can support **evidence-based public data analysis**.

---

# Author

Juliana Mendes
Data-Driven Business Development | Revenue Operations | Analytics

