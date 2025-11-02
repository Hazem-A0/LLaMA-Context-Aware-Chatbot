from langchain.tools import Tool
import PyPDF2
import io

def build_context_relevance_checker(llm):
    """
    Checks if the uploaded PDF is relevant to the user's question.
    If relevant, returns the PDF text for use as context.
    """

    def check_relevance(inputs):
        """
        inputs: dict with keys 'pdf_bytes' and 'question'
        pdf_bytes: binary content of the uploaded PDF
        question: user question string
        """
        pdf_bytes = inputs.get("pdf_bytes")
        question = inputs.get("question")

        if not pdf_bytes or not question:
            return "Missing PDF or question."

        # Extract text from PDF
        try:
            pdf_stream = io.BytesIO(pdf_bytes)
            reader = PyPDF2.PdfReader(pdf_stream)
            pdf_text = "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception as e:
            return f"Error reading PDF: {e}"

        # Ask LLM if relevant
        prompt = f"""
        You are a context relevance checker.
        Determine if the provided PDF content is relevant to the user's question.

        Question:
        {question}

        PDF Content (first 1500 chars shown):
        {pdf_text[:1500]}

        Respond with ONLY:
        - 'relevant' if the PDF contains useful info to answer the question
        - 'irrelevant' if it does not
        """
        decision = llm.invoke(prompt).strip().lower()

        if decision == "relevant":
            return {
                "status": "relevant",
                "context": pdf_text
            }
        else:
            return {
                "status": "irrelevant",
                "context": ""
            }

    return Tool.from_function(
        func=check_relevance,
        name="ContextRelevanceChecker",
        description="Checks if the uploaded PDF is relevant to the question and returns the text if relevant."
    )


