# LLaMA Context-Aware Chatbot 🦙

A context-aware chatbot built with LangChain, Streamlit, and Ollama LLM that can understand and respond to questions based on uploaded PDF documents and web search results.

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

## Troubleshooting

### FAISS Installation Issues

If you encounter problems installing FAISS on Windows:

1. Try installing via pip:
```bash
pip install faiss-cpu
```

2. If that fails, use conda:
```bash
conda install -c pytorch faiss-cpu
```

### Ollama Issues

1. Ensure Ollama is running:
```bash
# Check if Ollama is running
ollama list
```

2. If you get connection errors:
- Verify the Ollama service is running
- Check if the model is downloaded:
```bash
ollama pull llama3
```

3. Model alternatives:
- You can modify the model in `agent_runner.py` to use a different Ollama model
- Or switch to another LLM provider (requires code changes)

### Vector Store Issues

If you encounter problems with the FAISS vector store:

1. Clear the vector store:
- Delete the `vector_store/index.faiss` file
- The system will recreate it when you upload new PDFs

2. Check file permissions:
- Ensure the `vector_store` directory is writable
- Verify `uploaded_pdfs` directory exists and is writable

## Development

### Customization

1. Modify LLM settings:
- Edit `agent_runner.py` to change the model or parameters
- Adjust temperature for more/less creative responses

2. Change embeddings:
- Edit `pdf_relevance_checker.py` to use different embedding models
- Configure chunk size and overlap for document processing

3. UI customization:
- Modify `app.py` to change the Streamlit interface
- Custom CSS is included for styling

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.