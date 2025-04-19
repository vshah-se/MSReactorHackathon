from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from chat_handler import ChatHandler

app = Flask(__name__)
CORS(app)

# Directory to save uploaded files
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/upload-pdf', methods=['POST'])
def upload_pdf():
    """
    Endpoint to upload a PDF file.
    """
    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file and file.filename.endswith('.pdf'):
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)
        return jsonify({'message': 'File uploaded successfully', 'file_path': file_path}), 200
    else:
        return jsonify({'error': 'Invalid file type. Only PDF files are allowed.'}), 400

@app.route('/chat', methods=['POST'])
def chat():
    """
    Endpoint to handle chat queries and return responses.
    """
    data = request.json
    if not data or 'query' not in data:
        return jsonify({'error': 'No query provided'}), 400

    query = data['query']
    chat_handler = ChatHandler()
    response = chat_handler.process_query(query)
    # Mock response for now
    return jsonify({'query': query, 'response': response}), 200

if __name__ == '__main__':
    app.run(debug=True)