# -*- coding: utf-8 -*-
"""
Created on Fri Sep  5 15:36:42 2025

@author: td00654
"""

import streamlit as st
import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# --- CONFIGURATION ---
DB_PERSIST_DIR = './vector_db_1'
EMBEDDING_MODEL_NAME = "all-MiniLM-L6-v2"

# --- CACHING ---
# Cache the embedding model and vector store for faster re-runs
@st.cache_resource
def load_embedding_model():
    """
    Loads the embedding model from Hugging Face.

    This function is cached to avoid reloading the model on every app rerun,
    which significantly improves performance.

    Returns:
        HuggingFaceEmbeddings: The loaded embedding model.
    """
    return HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL_NAME)

@st.cache_resource
def load_vector_store(_embeddings):
    """
    Loads the vector store from the persistent directory.

    This function is cached to avoid reloading the vector store on every app
    rerun. It depends on the embedding model, which is passed as an argument.

    Args:
        _embeddings (HuggingFaceEmbeddings): The embedding model to use for the
        vector store.

    Returns:
        Chroma: The loaded vector store.
    """
    return Chroma(persist_directory=DB_PERSIST_DIR, embedding_function=_embeddings)

# --- MAIN APP ---
# --- MAIN APP ---
def main():
    """
    The main function for the Streamlit app.

    This function sets up the Streamlit page, handles user input, performs
    the similarity search, and displays the results. It also includes error
    handling for the vector database and model loading.
    """
    st.set_page_config(page_title="Research Paper Search", page_icon="📚", layout="wide")
    
    st.title("📚 Research Paper Search")
    st.write("Ask a question about your documents, and the app will find the most relevant information.")

    # --- ERROR HANDLING ---
    if not os.path.exists(DB_PERSIST_DIR):
        st.error(f"Vector database not found! Please run the `create_vectordb.py` script first.")
        st.stop()

    # --- LOAD MODELS AND VECTOR STORE ---
    try:
        embeddings = load_embedding_model()
        vector_store = load_vector_store(embeddings)
        # --- NEW: Add this line to display the document count ---
        st.caption(f"ℹ️ Database loaded with {vector_store._collection.count()} documents.")

    except Exception as e:
        st.error(f"An error occurred while loading the models or database: {e}")
        st.stop()

    # --- USER INPUT ---
    user_query = st.text_input("Ask a question:", placeholder="e.g., What are the effects of policy on renewable energy adoption?")
    
    # Add a slider to control the number of results
    k_results = st.slider("Number of results to return:", min_value=1, max_value=10, value=3)

    # --- SEARCH AND DISPLAY ---
    if user_query:
        with st.spinner("Searching for relevant documents..."):
            try:
                # Perform the similarity search
                results = vector_store.similarity_search(user_query, k=k_results)

                st.subheader(f"Top {len(results)} Relevant Documents:")

                if not results:
                    st.info("No relevant documents found for your query.")
                else:
                    # Display each result in a container
                    for i, doc in enumerate(results):
                        with st.container(border=True):
                            # Extract metadata, with fallbacks for missing keys
                            title = doc.metadata.get('title', 'No Title Found')
                            authors = doc.metadata.get('authors', 'No Authors Found')
                            source = doc.metadata.get('source', 'Unknown Source')
                            
                            st.markdown(f"### {i+1}. {title}")
                            st.markdown(f"**Authors:** {authors}")
                            
                            # Use an expander for the content to keep the UI clean
                            with st.expander("Show content snippet"):
                                st.write(doc.page_content)

                            st.caption(f"Source: {os.path.basename(source)}")
                            
            except Exception as e:
                st.error(f"An error occurred during the search: {e}")

if __name__ == "__main__":
    main()