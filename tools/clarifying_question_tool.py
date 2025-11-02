from langchain.tools import Tool
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

def build_clarifying_question_tool(llm):
    prompt = PromptTemplate(
        template=(
            "The user asked: {input}\n"
            "The message is missing important background details.\n"
            "Ask ONE clear, concise follow-up question to get the missing information.\n"
            "Avoid generic questions like 'Can you provide more details?'.\n"
            "Focus only on what would make the answer more accurate.\n"
            "Question:"
        ),
        input_variables=["input"]
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    return Tool.from_function(
        func=chain.run,
        name="ClarifyingQuestionGenerator",
        description="Generates a specific clarifying question when user input lacks context"
    )
