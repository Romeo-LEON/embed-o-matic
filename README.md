# Embed-o-Matic 🤖

A Streamlit application that creates embeddings from DOCX documents, stores them in PostgreSQL using pgvector, and enables semantic search with RAG (Retrieval-Augmented Generation) capabilities using OpenAI's GPT models.

## Features

- 📄 DOCX document processing
- 🔤 Text chunking and embedding generation using OpenAI
- 💾 Vector storage in PostgreSQL using pgvector
- 🔍 Semantic search functionality
- 🤖 RAG-powered responses using OpenAI's GPT models
- 🎯 Adjustable search results

## Prerequisites

- Python 3.8+
- PostgreSQL with pgvector extension
- OpenAI API key
- PostgreSQL database with vector extension enabled

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd vector_db_proj
```

2. Install required packages:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with the following variables:
```bash
OPENAI_API_KEY=your_openai_api_key
CONNECTION_STRING=postgresql://user:password@host:port/database
```

## Project Structure

```
vector_db_proj/
├── app.py              # Streamlit application
├── utils.py            # Utility functions
├── constant.py         # Configuration constants
└── requirements.txt    # Project dependencies
```

## Usage

1. Start the Streamlit application:
```bash
streamlit run app.py
```

2. Upload a DOCX document using the file uploader
3. Click 'Process Document' to create embeddings
4. Use the search box to query your document
5. Adjust the number of results using the slider

## Key Components

### Document Processing
- Uses `Docx2txtLoader` for DOCX file processing
- Implements `RecursiveCharacterTextSplitter` for text chunking
- Generates embeddings using OpenAI's embedding model

### Vector Storage
- Utilizes PostgreSQL with pgvector for vector storage
- Automatically manages collections based on document content
- Supports reuse of existing collections for identical documents

### Search and RAG
- Performs semantic similarity search on stored vectors
- Implements RAG using OpenAI's GPT models
- Combines search results with user queries for context-aware responses

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `CONNECTION_STRING`: PostgreSQL connection string with pgvector support

## Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Uses [LangChain](https://python.langchain.com/) for RAG implementation
- Powered by [OpenAI](https://openai.com/) models