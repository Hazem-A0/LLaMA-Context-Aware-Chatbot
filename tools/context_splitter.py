from langchain.tools import Tool

def build_context_splitter(llm):
    def split_context(input_text):
        prompt = f"""
        You are a context splitter.
        Given the user input, separate it into:
        1. Background Context
        2. Actual Question

        Format output as:
        Background: <text>
        Question: <text>

        Input:
        {input_text}
        """
        return llm.invoke(prompt).strip()

    return Tool.from_function(
        func=split_context,
        name="ContextSplitter",
        description="Splits the background context from the main question."
    )
