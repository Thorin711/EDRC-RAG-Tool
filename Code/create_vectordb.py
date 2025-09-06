import os
import frontmatter
from langchain.docstore.document import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma

# --- 1. DEFINE PATHS ---
# The directory where you saved your markdown files
md_output_dir = r'C:\Users\td00654\OneDrive - University of Surrey\Documents\EDRC LLM Project\Papers\EDRC - Text'
# The directory where you want to save the vector database
db_persist_dir = r'./vector_db_1'

# --- Custom function to load documents with front matter ---
def load_documents_from_directory(directory):
    """
    Loads all markdown files from a directory, parsing their front matter
    and creating LangChain Document objects.

    Args:
        directory (str): The path to the directory containing the markdown
        files.

    Returns:
        list[Document]: A list of LangChain Document objects, where each
        object represents a markdown file.
    """
    documents = []
    print("Loading documents with custom loader...")
    for filename in os.listdir(directory):
        if filename.endswith(".md"):
            filepath = os.path.join(directory, filename)
            post = frontmatter.load(filepath)
            
            # --- FIX: Convert the list of authors into a single string ---
            if 'authors' in post.metadata and isinstance(post.metadata['authors'], list):
                post.metadata['authors'] = ", ".join(post.metadata['authors'])
            # -------------------------------------------------------------
            
            post.metadata['source'] = filepath
            doc = Document(page_content=post.content, metadata=post.metadata)
            documents.append(doc)
            
    return documents

print("Starting the vector database creation process...")

# --- 2. LOAD DOCUMENTS ---
documents = load_documents_from_directory(md_output_dir)
print(f"Successfully loaded {len(documents)} documents.")

# --- 3. SPLIT DOCUMENTS INTO CHUNKS ---
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
docs = text_splitter.split_documents(documents)
print(f"Split the documents into {len(docs)} chunks.")

# --- 4. CREATE EMBEDDINGS ---
embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
print("Embedding model loaded.")

# --- 5. STORE IN VECTOR DATABASE ---
print("Creating and persisting the vector database... (This may take a few minutes)")
vector_store = Chroma.from_documents(
    documents=docs,
    embedding=embeddings,
    persist_directory=db_persist_dir
)
print("Vector database created successfully!")

#%% --- EXAMPLE SEARCH ---
print("\n--- Running an example search ---")
query = "What are the effects of policy on renewable energy adoption?"
results = vector_store.similarity_search(query, k=3)

print(f"Query: '{query}'")
print("\nTop 3 results:")
for i, doc in enumerate(results):
    title = doc.metadata.get('title', 'No Title Found')
    print(f"--- Result {i+1} ---")
    print(f"Source Title: {title}")
    print(f"Content: {doc.page_content[:300]}...\n")