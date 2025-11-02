# tools/context_presence_judge.py
from langchain_core.prompts import PromptTemplate

def build_context_presence_checker(llm):
    """
    Returns two callables:
    - check_context_presence(text) -> 'context_provided' | 'context_missing'
    - judge_context(query, pdf_text) -> 'pdf' | 'web'
    """

    prompt = PromptTemplate(
        template=(
            "You are a context detection system.\n"
            "Determine if the following user message includes BACKGROUND CONTEXT "
            "beyond a direct question.\n\n"
            "Rules:\n"
            "1) If the message contains extra background info beyond the direct question, output: context_provided\n"
            "2) If it's just a question without extra details, output: context_missing\n"
            "3) If the message is a greeting (e.g., 'hi', 'hello') or a goodbye (e.g., 'bye', 'good night'), "
            "treat it as context_provided because it can be answered directly.\n"
            "4) Output exactly one of these two tokens, nothing else.\n\n"
            "Message: {input}\n\n"
            "Output:"
        ),
        input_variables=["input"]
    )

    # New style pipeline: prompt | llm
    chain = prompt | llm

    def check_context_presence(text: str) -> str:
        raw = chain.invoke({"input": text}).strip().lower()
        if "provided" in raw:
            return "context_provided"
        if "missing" in raw:
            return "context_missing"
        # Fallback is conservative
        return "context_missing"

    def judge_context(query: str, pdf_text: str) -> str:
        """
        Decide if the answer should come from the PDF or from the web.
        - If query terms appear in the PDF text -> use 'pdf'
        - Otherwise -> use 'web'
        """
        if query.lower() in pdf_text.lower():
            return "pdf"
        return "web"

    return check_context_presence, judge_context
