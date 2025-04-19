import chromadb
from chromadb.config import Settings
import requests
from rag import RAG
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from google.generativeai import configure, GenerativeModel
import os
import json

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
        self.gemini_api_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash"
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")  # Replace with your actual API key
        self.embedding_model = SentenceTransformer("all-MiniLM-L6-v2")  # Example embedding model
        configure(api_key=self.gemini_api_key)
        self.gemini = GenerativeModel("gemini-2.0-flash")
        self.rag = RAG()

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
         # Step 1: Create a prompt for intent determination
        intent_prompt = f"""
        You are an AI assistant. Your task is to determine the intent of the user's query. 
        The query will be related to real estate, specifically rental laws or lease agreements.

        Here are the possible intents:
        - rental_laws: The query is about rental laws and regulations.
        - lease_agreements: The query is about lease agreements, contracts, and related terms.
        - unknown: The query is not related to rental laws or lease agreements, or the intent is unclear.

        Based on the information below, determine the intent of the query.
        Query:
        {query}

        Return the intent as one of the following strings: "rental_laws", "lease_agreements", or "unknown".
        """

        # Step 2: Get the intent from the Gemini API
        try:
            intent_response = self.gemini.generate_content(intent_prompt)
            intent = intent_response.text.strip()
            print(f"Intent detected: {intent}")  # Debugging
        except Exception as e:
            print(f"Error determining intent: {e}")
            intent = "unknown"  # Default to unknown in case of error

        # Step 3: Define the function call based on the intent
        if intent == "rental_laws":
            function_call = {
                "name": "get_rental_law_information",
                "description": "This function retrieves information about rental laws based on the user's query.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's query about rental laws."
                         }
                    },
                    "required": ["query"]
                }
            }
        elif intent == "lease_agreements":
            function_call = {
                "name": "get_lease_agreement_information",
                 "description": "This function retrieves information about lease agreements based on the user's query.",
                "parameters": {
                    "type": "OBJECT",
                    "properties": {
                        "query": {
                            "type": "string",
                            "description": "The user's query about lease agreements."
                         }
                    },
                    "required": ["query"]
                }
            }
        else:
            return "I'm sorry, I couldn't understand the intent of your query.  Please try again."

        # Step 4: Create a prompt for the Gemini API, including the function call
        prompt = f"""
        You are an AI assistant. The user has a question about real estate. You have access to the following function:

        {json.dumps(function_call, indent=4)}

        Use this function to answer the user's question: {query}
        """

        # Step 5: Send the prompt and function call to the Gemini API
        try:
            response = self.gemini.generate_content(
                contents=prompt,
                tools=[{"function_declarations": [function_call]}]
            )

            # Check if the response contains a function call
            if response.parts and response.parts[0].function_call:
                function_name = response.parts[0].function_call.name
                arguments = response.parts[0].function_call.args

                # Call the function based on the function name
                if function_name == "get_rental_law_information":
                    return self.get_rental_law_information(arguments)  # Call the function
                elif function_name == "get_lease_agreement_information":
                    return self.get_lease_agreement_information(arguments)
                else:
                    return f"Unknown function: {function_name}"
            else:
                return response.text  # Return the response text if no function call
        except Exception as e:
            return f"Error communicating with Gemini API: {e}"

    def get_rental_law_information(self, arguments):
        """
        This function is called when the Gemini API determines that the get_rental_law_information
        function should be called.
        """
        query = arguments.get("query")
        context = self.rag.get_law_context(query)

        prompt = f"""
        You are an AI assistant. Your task is to answer questions about user query based on the context provided.
        Based on the information below use context to answer the user's question.
        Query:{query}
        context:{context}
        """
        response = self.gemini.generate_content(prompt)
        return response.text

    def get_lease_agreement_information(self, arguments):
        """
        This function is called when the Gemini API determines that the get_lease_agreement_information
        function should be called.
        """
        
        query = arguments.get("query")
        context = self.rag.get_lease_context(query)

        prompt = f"""
        You are an AI assistant. Your task is to answer questions about user query based on the context provided.
        Based on the information below use context to answer the user's question.
        Query:{query}
        context:{context}
        """
        response = self.gemini.generate_content(prompt)
        return response.text

    
# Example usage
if __name__ == "__main__":
    chat_handler = ChatHandler()
    user_query = "What are the rental laws in Washington State?"
    response = chat_handler.process_query(user_query)
    print(response)
# This code is a simplified example and may require adjustments based on your actual implementation and requirements.