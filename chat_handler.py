import chromadb
from chromadb.config import Settings
import requests
from rag import RAG
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os

class ChatHandler:
    """
    A class to handle chat queries and provide responses.
    """

    def __init__(self):
        # Initialize ChromaDB clients for different collections
        # self.chroma_client = chromadb.Client(Settings(
        #     chroma_db_impl="duckdb+parquet",
        #     persist_directory="chroma_vectors"  # Directory to store vectors
        # ))
        # Load or create collections for rental laws and lease
        # self.rentallaws_collection = self.chroma_client.get_or_create_collection(name="rentallaws")
        # self.lease_collection = self.chroma_client.get_or_create_collection(name="lease")

        # Google Gemini API configuration
        self.gemini_api_url = "https://api.gemini-model.com/v1/chat"
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")  # Replace with your actual API key
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Example embedding model

    def determine_intent(self, query):
        """
        Determine the intent of the query (e.g., rental laws or lease).
        :param query: The input query string.
        :return: The intent as a string ('rentallaws' or 'lease').
        """
        # Simple intent determination logic (mocked for now)
        if "rental law" in query.lower():
            return "rentallaws"
        elif "lease" in query.lower():
            return "lease"
        else:
            return None

    def query_vector_db(self, collection, query_vector, n_results=3):
        """
        Query the specified ChromaDB collection for relevant documents.
        :param collection: The ChromaDB collection to query.
        :param query_vector: The vector representation of the query.
        :param n_results: The number of results to retrieve.
        :return: A combined context string from the retrieved documents.
        """
        results = collection.query(
            query_embeddings=[query_vector],
            n_results=n_results
        )

        if results["documents"]:
            return " ".join(results["documents"])
        else:
            return "No relevant documents found."

    def send_to_gemini(self, prompt):
        """
        Send the prompt to the Google Gemini API and retrieve the response.
        :param prompt: The prompt to send to the Gemini API.
        :return: The response from the Gemini API.
        """
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.gemini_api_key}'
        }
        payload = {
            'prompt': prompt
        }

        try:
            response = requests.post(self.gemini_api_url, json=payload, headers=headers)
            response.raise_for_status()  # Raise an error for HTTP codes 4xx/5xx
            return response.json().get('response', 'No response from Gemini API')
        except requests.exceptions.RequestException as e:
            return f"Error communicating with Gemini API: {e}"

    def process_query(self, query):
        """
        Process the chat query, retrieve relevant information from the appropriate ChromaDB,
        and send the combined output to the Google Gemini API for a response.
        :param query: The input query string.
        :return: The response string.
        """
        """
        # Step 1: Determine the intent of the query
        intent = self.determine_intent(query)
        if not intent:
            return "Unable to determine intent. Please specify if the query is about rental laws or lease."

        # Step 2: Select the appropriate collection based on intent
        if intent == "rentallaws":
            collection = self.rentallaws_collection
        elif intent == "lease":
            collection = self.lease_collection
        else:
            return "Invalid intent detected."
        """
        #collection = [self.rentallaws_collection, self.lease_collection]
        # self.rentallaws_collection, self.lease_collection = rag()
        # Step 3: Convert query to vector (mocked for now)
        #query_vector = self.embedding_model.encode(query)  # Replace with actual vector embedding logic

        # Step 4: Query the selected ChromaDB collection
        # context = self.query_vector_db(collection, query_vector)
        vectorsearch = RAG()
        rental_context, lease_context = vectorsearch.rag(query)
        # Step 5: Create a prompt for the Gemini API
        prompt = f"""
        You are an AI assistant. Below are two contexts related to the user's query. Use the information from these contexts to answer the question.

        Context 1 (Rental Laws):
        {rental_context}

        Context 2 (Lease Information):
        {lease_context}

        Question:
        {query}

        Please provide a concise and accurate response based on the provided contexts.
        """

        # Step 6: Send the prompt to the Google Gemini API
        gemini_response = self.send_to_gemini(prompt)

        # Step 7: Return the response
        return gemini_response
    
# Example usage
if __name__ == "__main__":
    chat_handler = ChatHandler()
    user_query = "What are the rental laws in Washington State?"
    response = chat_handler.process_query(user_query)
    print(response)
# This code is a simplified example and may require adjustments based on your actual implementation and requirements.