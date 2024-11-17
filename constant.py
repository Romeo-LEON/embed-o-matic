from langchain_core.prompts import ChatPromptTemplate

open_ai_message_config = ChatPromptTemplate.from_messages([
    (
        "system",
        """
        You are an AI assistant designed to provide accurate and helpful answers to user queries. 
        Specifically, you operate as a Retrieval-Augmented Generation (RAG) system that leverages 
        information fetched from a PostgreSQL vector database. Your task is to combine your general 
        knowledge with the provided context to generate articulate, human-readable responses. 
        Focus on clarity, relevance, and coherence in your answers.
        """,
    ),
    ("human", "{input}"),
])