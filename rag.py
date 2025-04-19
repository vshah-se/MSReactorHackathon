# rag_real_estate.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from google.generativeai import configure, GenerativeModel
import os

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set your API key
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

def create_vector_datastore(pdf_path, create_user_data):
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents = loader.load()
    
    # Split Text
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP
    )
    chunks = text_splitter.split_documents(documents)
    
    # Create Vector Store
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    vector_db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory="./real_estate_db" if not create_user_data else "./user_data_db"
    )
    
    return vector_db

def rag(user_data, query):
    # Initialize Gemini
    pdf_path = "RCW_59.18.pdf"
    law_vector_db = create_vector_datastore(pdf_path,False)
    user_vector_db = create_vector_datastore(user_data, True)

    relevant_law = law_vector_db.similarity_search(query, k=3)
    relevant_user_data = user_vector_db.similarity_search(query, k=3)

    law_context = "\n".join([doc.page_content for doc in relevant_law])
    user_data_context = "\n".join([doc.page_content for doc in relevant_user_data])

    return law_context, user_data_context
    
    # configure(api_key=GEMINI_API_KEY)
    # gemini = GenerativeModel("gemini-2.0-flash")

    # # Query Interface
    # while True:
    #     query = input("\nEnter legal query (q to quit): ")
    #     if query.lower() == 'q':
    #         break
            
    #     # Retrieval
    #     relevant_docs = vector_db.similarity_search(query, k=3)
    #     context = "\n".join([doc.page_content for doc in relevant_docs])
        
    #     # Generation with Gemini
    #     response = gemini.generate_content(
    #         f"Answer based on real estate laws:\nContext: {context}\nQuestion: {query}"
    #     )
    #     print(f"\nLegal Response: {response.text}")

if __name__ == "__main__":
    print(rag("rental_agreement.pdf", "What are the tenant's rights in Washington State?"))
