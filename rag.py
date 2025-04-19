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

class RAG:

    REAL_ESTATE_LAW_PDF = "RCW_59.18.pdf"
    LAW_VECTOR_DB = None
    USER_DATA_VECTOR_DB = None

    def __init__(self):
        print("Initializing RAG...")
        self.LAW_VECTOR_DB = self._create_vector_datastore(self.REAL_ESTATE_LAW_PDF, False)
        print("Data store created, RAG initialized successfully.")

    def _create_vector_datastore(self, pdf_path, create_user_data):
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
    
    def create_user_data_vector_store(self, user_data):
        try:
            print(f"Creating user data vector store from {user_data}...")
            self.USER_DATA_VECTOR_DB = self._create_vector_datastore(user_data, True)
            print("User data vector store created successfully.")
        except Exception as e:
            print(f"Error creating user data vector store: {e}")
            return False
        
        return True

    def rag(self, query):

        if not self.LAW_VECTOR_DB:
            print("Error: Law vector database not initialized.")
            return None
        if not self.USER_DATA_VECTOR_DB:
            print("Error: User data vector database not initialized.")
            return None
        
        relevant_law = self.LAW_VECTOR_DB.similarity_search(query, k=3)
        relevant_user_data = self.USER_DATA_VECTOR_DB.similarity_search(query, k=3)

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
    
