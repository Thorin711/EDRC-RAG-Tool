# Research Paper Search Engine

This project is a Streamlit web application that allows you to search through a collection of research papers using natural language queries. It uses a vector database to store the embeddings of the research papers, and it uses a Hugging Face model to perform the similarity search.

## Features

*   **Natural Language Search**: Ask questions in plain English to find relevant information in your research papers.
*   **Vector-Based Search**: Utilizes state-of-the-art sentence transformers to understand the semantic meaning of your queries and the document content.
*   **Streamlit Web App**: An easy-to-use and interactive web interface for searching and viewing results.
*   **PDF and XML Processing**: Includes scripts to process PDF and XML files, extract their content, and prepare them for indexing.

## Getting Started

### Prerequisites

*   Python 3.8+
*   Grobid (for processing PDFs). See the [Grobid documentation](https://grobid.readthedocs.io/en/latest/Install-Grobid/) for installation instructions.

### Installation

1.  Clone the repository:
    ```bash
    git clone <repository-url>
    ```
2.  Navigate to the `Code/` directory:
    ```bash
    cd Code
    ```
3.  Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

**Note:** The paths in `simple_process_pdfs.py` and `create_vectordb.py` are hardcoded. You will need to update these paths to match your local environment.

1.  **Process your documents**:
    *   Place your PDF files in the `Papers/EDRC - PDF` directory.
    *   Run the `simple_process_pdfs.py` script to process the PDFs using Grobid. This will generate XML files in the `Papers/EDRC - XML` directory.
        ```bash
        python simple_process_pdfs.py
        ```
    *   Run the `xml_to_md.py` script to convert the XML files to Markdown files. This will save the Markdown files in the `Papers/EDRC - Text` directory.
        ```bash
        python xml_to_md.py
        ```

2.  **Create the vector database**:
    *   Run the `create_vectordb.py` script to create the vector database from the Markdown files. This will create a `vector_db_1` directory.
        ```bash
        python create_vectordb.py
        ```

3.  **Run the Streamlit app**:
    *   Run the `app.py` script to start the Streamlit web application.
        ```bash
        streamlit run app.py
        ```
    *   Open your web browser and navigate to the URL provided by Streamlit (usually `http://localhost:8501`).

## File Descriptions

*   `app.py`: The main Streamlit web application.
*   `create_vectordb.py`: A script to create the vector database from the Markdown files.
*   `simple_process_pdfs.py`: A script to process PDF files using Grobid.
*   `xml_to_md.py`: A script to convert Grobid XML files to Markdown files.

## Built With

*   [Streamlit](https://streamlit.io/) - The web framework used to build the application.
*   [LangChain](https://python.langchain.com/) - The framework used for the language model and vector database integration.
*   [Hugging Face Transformers](https://huggingface.co/transformers/) - The library used for the sentence embeddings.
*   [ChromaDB](https://www.trychroma.com/) - The vector database used to store the document embeddings.
*   [Grobid](https://github.com/kermitt2/grobid) - The tool used to extract structured text from PDF files.
