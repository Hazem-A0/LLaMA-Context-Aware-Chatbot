# agent/agent_runner.py
import os
import json
from typing import Optional

from langchain.agents import initialize_agent, AgentType
from langchain_ollama import OllamaLLM

# Local tools
from tools.context_presence_judge import build_context_presence_checker
from tools.pdf_relevance_checker import (
    ensure_vectorstore_ready,
    add_pdf_if_new,
    retrieve_relevant_context,
    attach_persistent_cache,
)
from tools.web_search_tool import build_advanced_web_search

HASH_CACHE_FILE = "processed_pdfs.json"
VECTOR_STORE_DIR = "vector_store"

# ------------------------
# LLM (deterministic)
# ------------------------
llm = OllamaLLM(model="llama3", temperature=0)

# ------------------------
# Deterministic context checker
# ------------------------
check_context_presence, judge_context = build_context_presence_checker(llm)

# ------------------------
# Web search tool
# ------------------------
web_search_tool = build_advanced_web_search()

# ------------------------
# Persistent PDF hash cache
# ------------------------
def _load_hash_cache() -> set:
    if os.path.exists(HASH_CACHE_FILE):
        try:
            with open(HASH_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return set(data) if isinstance(data, list) else set()
        except Exception:
            return set()
    return set()

def _save_hash_cache(cache: set) -> None:
    try:
        with open(HASH_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(sorted(list(cache)), f)
    except Exception:
        pass

_pdf_cache = _load_hash_cache()
attach_persistent_cache(_pdf_cache, on_flush=_save_hash_cache)
ensure_vectorstore_ready(VECTOR_STORE_DIR)

# ------------------------
# Helpers
# ------------------------
def _answer_from_pdf(llm: OllamaLLM, question: str, context: str) -> str:
    prompt = (
        "You are a meticulous assistant. Answer the question **only** using the provided PDF excerpts.\n"
        "If the PDF does not contain enough information, say: 'INSUFFICIENT'.\n\n"
        "PDF Context:\n"
        "----------------\n"
        f"{context}\n"
        "----------------\n\n"
        f"Question: {question}\n\n"
        "Answer:"
    )
    out = llm.invoke(prompt)
    return out if isinstance(out, str) else str(out)

def _answer_via_web(llm: OllamaLLM, question: str) -> str:
    agent = initialize_agent(
        tools=[web_search_tool],
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        handle_parsing_errors=True,
        verbose=False,
    )
    try:
        out = agent.run(question)
        text = out if isinstance(out, str) else str(out)
        if not text.strip().lower().startswith("final answer:"):
            return f"Final Answer: {text.strip()}"
        return text.strip()
    except Exception as e:
        return f"Final Answer: (Web search error) {str(e)}"

def _is_greeting_or_goodbye(text: str) -> Optional[str]:
    greetings = ["hi", "hello", "hey", "good morning", "good evening"]
    goodbyes = ["bye", "goodbye", "see you", "take care", "good night"]

    lowered = text.strip().lower()
    if any(lowered == g for g in greetings):
        return "Hello! How can I help you today?"
    if any(lowered == g for g in goodbyes):
        return "Goodbye! Have a great day!"
    return None

# ------------------------
# Public API
# ------------------------
def ask_agent(question: str, pdf_bytes: Optional[bytes] = None) -> str:
    """
    Routing logic:
      1) Greeting/Goodbye → answer directly.
      2) If PDF relevant:
         - Answer from PDF.
         - If insufficient → fallback to web.
      3) Else → answer via web search.
    """
    # 1) Handle greetings/goodbyes
    direct = _is_greeting_or_goodbye(question)
    if direct:
        return direct

    # 2) PDF pipeline (if PDF provided)
    if pdf_bytes:
        try:
            add_pdf_if_new(pdf_bytes, vectorstore_dir=VECTOR_STORE_DIR)
            pdf_context = retrieve_relevant_context(question, k=4)
        except Exception:
            pdf_context = ""

        if pdf_context.strip():
            pdf_answer = _answer_from_pdf(llm, question, pdf_context).strip()
            if pdf_answer.upper().startswith("INSUFFICIENT"):
                return f"From the PDF: not enough info.\n{_answer_via_web(llm, question)}"
            return f"Final Answer: {pdf_answer}"

    # 3) Web fallback for all other cases
    return _answer_via_web(llm, question)
