from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.vectorstores.pgvector import PGVector
from langchain_community.document_loaders import Docx2txtLoader
from typing import List, Optional
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from constant import open_ai_message_config


def initialize_environment():
    """Initialize environment variables from .env file"""
    load_dotenv()
    # Optionally verify the key exists
    if not (os.getenv("OPENAI_API_KEY") or os.getenv("CONNECTION_STRING")):
        raise ValueError("OPENAI_API_KEY or CONNECTION_STRING not found in environment variables")
    else:
        print('Succesfully created env variables.')

def initialize_embeddings() -> OpenAIEmbeddings:
    """Initialize OpenAI embeddings using environment variable."""
    # OpenAIEmbeddings will automatically use OPENAI_API_KEY from environment
    return OpenAIEmbeddings()

def initialize_openai_chat() -> ChatOpenAI:
    """Initialize OpenAI chat using environment variable."""
    # ChatOpenAI will automatically use OPENAI_API_KEY from environment
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0.5,
        max_tokens=None,
        timeout=None,
        max_retries=2,
    )

def load_and_split_document(file_path: str, 
                          chunk_size: int = 1000, 
                          chunk_overlap: int = 20) -> List:
    """Load document and split into chunks."""
    loader = Docx2txtLoader(file_path)
    data = loader.load()
    
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap
    )
    
    return text_splitter.split_documents(data)

def create_vector_store(documents: List,
                       embeddings: OpenAIEmbeddings,
                       connection_string: str,
                       collection_name: str,
                       pre_delete_collection: bool = True) -> PGVector:
    """Create vector store in PostgreSQL."""
    return PGVector.from_documents(
        embedding=embeddings,
        documents=documents,
        collection_name=collection_name,
        connection_string=connection_string,
        pre_delete_collection=pre_delete_collection
    )

def perform_similarity_search(db: PGVector,
                            query: str,
                            k: int = 2) -> List:
    """Perform similarity search on vector store."""
    return db.similarity_search(query, k=k)

# def create_messages(user_query: str) -> list:
#     return [
#         open_ai_message_config[0],
#         (open_ai_message_config[1][0], open_ai_message_config[1][1].format(user_query))
#     ]

def perform_rag(llm: ChatOpenAI,
                query: str,
                context_docs: List
                ) -> str:
    # Create an enhanced query by combining the original query with search results
    context = "\n".join([doc.page_content for doc in context_docs])
    enhanced_query = f"Query: {query}\nContext from similar documents:\n{context}"
    
    chain = open_ai_message_config | llm
    return chain.invoke(
        {
            "input": enhanced_query,
        }
    )

