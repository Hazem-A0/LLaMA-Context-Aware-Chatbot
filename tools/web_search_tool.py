from langchain.tools import Tool
from ddgs import DDGS

def build_advanced_web_search(memory=None, max_results=3):
    def advanced_web_search(query: str) -> str:
        """
        Performs an advanced web search using DuckDuckGo with context from chat history.

        params:
            query (str): The search query from the user.

        returns:
            str: The search results or an error message.
        """
        try:
            # Prepare history context
            history_context = ""
            if memory:
                mem_vars = memory.load_memory_variables({})
                if "chat_history" in mem_vars:
                    if isinstance(mem_vars["chat_history"], list):
                        history_context = " ".join(
                            [m.content for m in mem_vars["chat_history"][-5:]]
                        )
                    else:
                        history_context = mem_vars["chat_history"]

            # Combine history and query
            full_query = f"{history_context} {query}".strip()

            output_lines = []
            query_keywords = set(query.lower().split())

            # Fetch fewer results for speed
            with DDGS() as ddgs:
                for result in ddgs.text(full_query, max_results=max_results * 2):  
                    body_text = result.get("body", "").lower()
                    # Fast relevance check
                    if any(word in body_text for word in query_keywords):
                        output_lines.append(
                            f"{result.get('title','No Title')}\n"
                            f"{result.get('href','')}\n"
                            f"{result.get('body','')}\n"
                        )
                        # Stop early if enough results
                        if len(output_lines) >= max_results:
                            break

            return "\n".join(output_lines) if output_lines else "No relevant results found."

        except Exception as e:
            return f"Search failed: {str(e)}"

    return Tool.from_function(
        func=advanced_web_search,
        name="WebSearchTool",
        description="Searches the web using DuckDuckGo with context from recent chat history to improve relevance."
    )
