import streamlit as st
import tempfile
import os
from utils import (
    initialize_environment,
    initialize_embeddings,
    load_and_split_document,
    create_vector_store,
    perform_similarity_search,
    initialize_openai_chat,
    perform_rag
)
import json

# Initialize environment at startup
initialize_environment()

# App title
st.title("Embed-o-Matic 🤖")
st.write("Upload a .docx document to create embeddings and store them in PostgreSQL")

# Initialize session state for database connection
if 'db' not in st.session_state:
    st.session_state.db = None

# File uploader
uploaded_file = st.file_uploader("Choose a DOCX file", type=['docx'])

if uploaded_file:
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix='.docx') as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        temp_file_path = tmp_file.name

    # Process button
    if st.button("Process Document"):
        with st.spinner("Processing document..."):
            try:
                # Initialize embeddings
                embeddings = initialize_embeddings()
                
                # Load and split document
                st.info("Loading and splitting document...")
                documents = load_and_split_document(temp_file_path)
                st.success(f"Document split into {len(documents)} chunks")
                
                # Create vector store
                st.info("Creating vector store...")
                connection_string = os.getenv("CONNECTION_STRING")
                collection_name = os.getenv("COLLECTION_NAME", "default_collection")
                
                db = create_vector_store(
                    documents=documents,
                    embeddings=embeddings,
                    connection_string=connection_string,
                    collection_name=collection_name
                )
                st.session_state.db = db
                st.success("Vector store created successfully!")

            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
            finally:
                # Clean up temporary file
                os.unlink(temp_file_path)

# Only show search interface if database is initialized
if st.session_state.db is not None:
    st.divider()
    st.subheader("Search Documents")
    
    # Search interface
    search_query = st.text_input("Enter your search query:")
    k_results = st.slider("Number of results", min_value=1, max_value=5, value=2)
    
    if search_query and st.button("Search"):
        with st.spinner("Searching..."):
            try:
                results = perform_similarity_search(
                    db=st.session_state.db,
                    query=search_query,
                    k=k_results
                )
                
                # Display results from chatgpt
                llm = initialize_openai_chat()
                llm_result = perform_rag(
                    llm=llm,
                    query=search_query,
                    context_docs=results
                )

                st.markdown(f"**Result from LLM**")
                st.write(llm_result.content)
                st.markdown("---")

                # Display results from DB
                for i, doc in enumerate(results, 1):
                    st.markdown(f"**Result {i}:**")
                    st.write(doc.page_content)
                    st.markdown("---")
                    
            except Exception as e:
                st.error(f"Search error: {str(e)}")

# Add some usage instructions
with st.sidebar:
    st.subheader("Instructions")
    st.markdown("""
    1. Upload a DOCX document using the file uploader
    2. Click 'Process Document' to create embeddings
    3. Once processing is complete, use the search box to query your document
    4. Adjust the number of results using the slider
    
    **Note:** Make sure your environment (.env file) variables are properly set up:
    - OPENAI_API_KEY
    - DATABASE_URL
    - COLLECTION_NAME
    """)