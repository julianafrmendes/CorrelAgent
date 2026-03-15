
# ============================================
# CORREL-AGENT — Unified Script
# ============================================

import os
import re
import nest_asyncio
from typing import List

from llama_index.core import (
    Settings,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)
from llama_index.readers.file import PandasCSVReader
from llama_index.readers.web import SimpleWebPageReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core.tools import FunctionTool
from llama_index.llms.groq import Groq
from llama_index.core.agent import ReActAgent


# ============================================
# 1️⃣ ASYNC SETUP (Jupyter Safe)
# ============================================

nest_asyncio.apply()


# ============================================
# 2️⃣ SYSTEM PROMPT
# ============================================

SYSTEM_PROMPT = """
This agent is a data analysis assistant.

Its purpose is to help users explore datasets and understand possible analyses.

When a user asks a question:
- interpret the intent;
- suggest described datasets and provided variables;
- provide educational and supportive guidance;
- do not invent data or analyses;
- DO NOT suggest variables that are not described in dataset Beschrijving.

The goal is learning and community engagement.
"""


# ============================================
# 3️⃣ GLOBAL SETTINGS
# ============================================

Settings.embed_model = HuggingFaceEmbedding(
    model_name="intfloat/multilingual-e5-base"
)

llm = Groq(
    model="llama-3.1-8b-instant",
    api_key="YOUR_GROQ_API_KEY_HERE",  # 🔐 Replace safely
    system_prompt=SYSTEM_PROMPT
)

Settings.llm = llm


# ============================================
# 4️⃣ PERSISTENT VECTOR INDEX
# ============================================

PERSIST_DIR = "./storage"

if not os.path.exists(PERSIST_DIR):
    print("Creating index for the first time...")
    reader = PandasCSVReader()
    documents = reader.load_data(file="catalog_overheid.csv")

    global_index = VectorStoreIndex.from_documents(documents)
    global_index.storage_context.persist(persist_dir=PERSIST_DIR)

    print("Index created and saved.")
else:
    print("Loading index from disk...")
    storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
    global_index = load_index_from_storage(storage_context)
    print("Index ready.")


# ============================================
# 5️⃣ TOOL 1 — SEARCH CATALOG
# ============================================

def search_catalog(query: str) -> str:
    """
    Searches catalog and returns dataset URLs related to a topic.
    """
    query_engine = global_index.as_query_engine(similarity_top_k=3)

    prompt = (
        f"Regarding '{query}', identify available datasets. "
        "Return the exact dataset URLs found in the catalog. "
        "If multiple exist, list all clearly."
    )

    response = query_engine.query(prompt)
    return str(response)


# ============================================
# 6️⃣ TOOL 2 — READ DATASET DETAILS
# ============================================

def extract_urls_from_text(text: str) -> List[str]:
    pattern = r'https://data\.overheid\.nl/dataset/[^\s]+'
    urls = re.findall(pattern, text)
    return list(dict.fromkeys(urls))  # remove duplicates


def read_dataset_details(input_text: str) -> str:
    """
    Extracts URLs from text and returns their descriptions.
    """
    urls = extract_urls_from_text(input_text)

    if not urls:
        return "No valid URLs found."

    loader = SimpleWebPageReader(html_to_text=True)
    results = []

    for url in urls:
        documents = loader.load_data([url])

        if not documents:
            results.append(f"URL: {url}\nDescription: No content available.\n")
            continue

        text = documents[0].text

        if "## Beschrijving" in text:
            parts = text.split("## Beschrijving", 1)[1]
            desc = parts.split("\n##", 1)[0].strip()
        else:
            desc = text.strip()

        results.append(f"URL: {url}\nDescription:\n{desc}\n")

    return "\n\n".join(results)


# ============================================
# 7️⃣ TOOL 3 — ANALYZE AND PLAN
# ============================================

def analyze_and_plan(input_text: str) -> str:
    """
    Creates structured analytical plan based on dataset descriptions.
    """

    prompt = (
        f"Context:\n{input_text}\n\n"
        "Tasks:\n"
        "1) List all dataset URLs found.\n"
        "2) Identify possible analytical variables explicitly mentioned.\n"
        "3) Suggest analytical uses.\n"
        "4) Propose at least two analytical approaches.\n\n"
        "Do not invent variables not described."
    )

    response = Settings.llm.complete(prompt)
    return str(response)


# ============================================
# 8️⃣ REGISTER TOOLS
# ============================================

search_tool = FunctionTool.from_defaults(
    fn=search_catalog,
    name="search_catalog",
    description="Searches the catalog and returns dataset URLs."
)

read_tool = FunctionTool.from_defaults(
    fn=read_dataset_details,
    name="read_dataset_details",
    description="Reads dataset URLs and extracts descriptions."
)

plan_tool = FunctionTool.from_defaults(
    fn=analyze_and_plan,
    name="analyze_and_plan",
    description="Generates structured analysis plan based on dataset descriptions."
)


# ============================================
# 9️⃣ CREATE REACT AGENT
# ============================================

agent = ReActAgent(
    tools=[search_tool, read_tool, plan_tool],
    llm=llm,
    verbose=True,
    max_iterations=8
)


# ============================================
# 🔟 RUN AGENT
# ============================================

async def run_agent():
    user_question = (
        "I want to correlate unemployment and level of education "
        "in Dutch population."
    )

    print("\n--- STARTING CORREL-AGENT WORKFLOW ---\n")

    response = await agent.run(user_msg=user_question)

    print("\n--- FINAL AGENT RESPONSE ---\n")
    print(response)


# Execute
await run_agent()