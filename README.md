# LLaMA Context-Aware Chatbot 🦙

A context-aware chatbot built with LangChain, Streamlit, and Ollama LLM that can understand and respond to questions based on uploaded PDF documents and web search results.

<img width="1919" height="905" alt="image" src="https://github.com/user-attachments/assets/6ec25796-5bbd-4325-abe7-28837cbb2c6d" />


## Features

- 📄 PDF Document Processing
  - Upload and process multiple PDF documents
  - Extract and index content using FAISS vector store
  - Semantic search for relevant context
- 🤖 Intelligent Responses
  - Context-aware answers from PDF content
  - Automatic fallback to web search when needed
  - DuckDuckGo integration for web searches
- 🎯 Smart Context Detection
  - Determines if queries need document context
  - Efficient routing between PDF and web sources
- 💻 Dual Interface
  - Beautiful Streamlit web interface
  - Simple command-line interface option

## Project Structure

```
.
├── agent/
│   └── agent_runner.py      # Core agent logic and routing
├── tools/
│   ├── context_presence_judge.py    # Context detection
│   ├── context_relevance_checker.py # Relevance checking
│   ├── pdf_relevance_checker.py     # PDF processing
│   └── web_search_tool.py          # Web search integration
├── vector_store/
│   └── index.faiss          # FAISS vector store
├── uploaded_pdfs/           # PDF storage directory
├── app.py                   # Streamlit web interface
└── main.py                  # CLI interface
```

## Prerequisites

1. Python 3.8 or higher
2. [Ollama](https://ollama.com/) installed and running
3. Windows, macOS, or Linux

## Installation

1. Clone the repository and navigate to the project directory:
```bash
cd "path/to/langchain_chat_with_context"
```

2. Create and activate a virtual environment:
```powershell
# Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Unix/macOS
python -m venv .venv
source .venv/bin/activate
```

3. Install required packages:
```bash
python -m pip install --upgrade pip
pip install streamlit langchain langchain-ollama langchain-community ddgs PyPDF2 faiss-cpu
```

4. Set up Ollama:
- Install Ollama from [ollama.com](https://ollama.com)
- Pull the required model:
```bash
ollama pull llama3
```
- Ensure the Ollama service is running

## Usage

### Web Interface (Recommended)

1. Start the Streamlit app:
```bash
python -m streamlit run app.py
```

2. Open your browser to the displayed URL (typically http://localhost:8501)

3. Use the sidebar to:
   - Upload PDF documents
   - View uploaded documents
   - Delete documents when needed

4. Ask questions in the chat interface:
   - The bot will use PDF context when relevant
   - Automatically searches the web when needed
   - Displays clear context indicators

### Command Line Interface

1. Run the CLI version:
```bash
python main.py
```

2. Type your questions and press Enter
3. Type 'exit' or 'quit' to end the session


## License

This project is open source and available under the MIT License.
