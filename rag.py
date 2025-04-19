# rag_real_estate.py
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from google.generativeai import configure, GenerativeModel
from google import genai
from google.genai import types
import os

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")  # Set your API key
EMBEDDING_MODEL = "sentence-transformers/all-mpnet-base-v2"
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200

class RAG:

    REAL_ESTATE_LAW_PDF = ["RCW_59.18.pdf", "law/landlord_tenant_rights.pdf", "law/tenant_rights_big.pdf"]

    def __init__(self):
        print("Initializing RAG...")
        self._create_vector_datastore(self.REAL_ESTATE_LAW_PDF, False)
        print("RAG initialized successfully.")

    def _create_vector_datastore(self, pdf_paths, create_user_data):

        # Check if the Law vector database already exists, 
        persist_directory = "./real_estate_db"
        if os.path.exists(persist_directory) and not create_user_data:
            print(f"Vector DB at {persist_directory} already exists.")
            return Chroma(persist_directory=persist_directory, embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL))
        
        # Load and combine documents from all PDFs
        all_documents = []
        for pdf_path in pdf_paths:
            print(f"Loading PDF: {pdf_path}")
            loader = PyPDFLoader(pdf_path)
            documents = loader.load()
            all_documents.extend(documents)
        
        # Split Text
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=CHUNK_SIZE,
            chunk_overlap=CHUNK_OVERLAP
        )
        chunks = text_splitter.split_documents(all_documents)
        
        # Create Vector Store
        embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
        vector_db = Chroma.from_documents(
            chunks,
            embeddings,
            persist_directory="./real_estate_db" if not create_user_data else "./user_data_db"
        )
        
        return vector_db
    
    def create_user_data_vector_store(self, user_data):
        try:
            print(f"Creating user data vector store from {user_data}...")
            self._create_vector_datastore([user_data], True)
            print("User data vector store created successfully.")
        except Exception as e:
            print(f"Error creating user data vector store: {e}")
            return False
        
        return True
    
    def get_law_context(self, query):
        law_vector_db = None
        persist_directory = "./real_estate_db"
        if os.path.exists(persist_directory):
            print(f"Loading existing vector database from {persist_directory}...")
            law_vector_db = Chroma(persist_directory=persist_directory, embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL))
        else:
            print("Creating new vector database for law...")
            law_vector_db = self._create_vector_datastore(self.REAL_ESTATE_LAW_PDF, False)
        
        relevant_law = law_vector_db.similarity_search(query, k=3)

        law_context = "\n".join([doc.page_content for doc in relevant_law])

        return law_context

    def get_lease_context(self, query):
        user_data_vector_db = None
        persist_directory = "./user_data_db"
        if os.path.exists(persist_directory):
            print(f"Loading existing vector database from {persist_directory}...")
            user_data_vector_db = Chroma(persist_directory=persist_directory, embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL))
        else:
            print("No user data vector database found. Please create one first.")
        relevant_user_data = user_data_vector_db.similarity_search(query, k=3)
        user_data_context = "\n".join([doc.page_content for doc in relevant_user_data])
        return user_data_context

    def rag(self, query):

        law_vector_db = None
        persist_directory = "./real_estate_db"
        if os.path.exists(persist_directory):
            print(f"Loading existing vector database from {persist_directory}...")
            law_vector_db = Chroma(persist_directory=persist_directory, embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL))
        else:
            print("Creating new vector database for law...")
            law_vector_db = self._create_vector_datastore(self.REAL_ESTATE_LAW_PDF, False)

        user_data_vector_db = None
        persist_directory = "./user_data_db"
        if os.path.exists(persist_directory):
            print(f"Loading existing vector database from {persist_directory}...")
            user_data_vector_db = Chroma(persist_directory=persist_directory, embedding_function=HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL))
        else:
            print("No user data vector database found. Please create one first.")
        
        relevant_law = law_vector_db.similarity_search(query, k=3)
        relevant_user_data = user_data_vector_db.similarity_search(query, k=3)

        law_context = "\n".join([doc.page_content for doc in relevant_law])
        user_data_context = "\n".join([doc.page_content for doc in relevant_user_data])

        return law_context, user_data_context

if __name__ == "__main__":
    # Example usage
    rag = RAG()
    rag.create_user_data_vector_store("rental_agreement.pdf")
    # Example query
    query = input("Enter your query: ")
    law_context, user_data_context = rag.rag(query)
    configure(api_key=GEMINI_API_KEY)
    gemini = GenerativeModel("gemini-2.0-flash")

    # Generation with Gemini
    response = gemini.generate_content(
        f"Answer based on real estate laws:\nLaws Context: {law_context}\nAgreement Context: {user_data_context}\nQuestion: {query}"
    )
    print(f"\nLegal Response: {response.text}")
    
