import React, { useState } from 'react';
import axios from 'axios';
import { Link } from 'react-router-dom';

function UploadPage() {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    const selected = e.target.files[0];
    if (selected && selected.type === 'application/pdf') {
      setFile(selected);
      setError('');
    } else {
      setFile(null);
      setError('Please select a PDF file');
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please choose a file first');
      return;
    }

    const formData = new FormData();
    formData.append('file', file); // append the selected PDF file to the FormData

    try {
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data' // Tell the server that we're sending form data (not JSON)
        }
      });

      // Handle successful response from the backend
      alert(`File uploaded successfully! Server says: ${response.data.message}`);
      setFile(null); // reset file after upload
    } catch (err) {
      console.error(err);
      setError('Upload failed. Please try again.');
    }
  };

  return (
    <div style={{ textAlign: 'center', marginTop: '50px' }}>
      <h2>Upload PDF File</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="application/pdf" onChange={handleChange} />
        <br />
        {error && <p style={{ color: 'red' }}>{error}</p>}
        {file && <p>Selected File: {file.name}</p>}
        <button type="submit">Upload</button>
      </form>
      <Link to="/" style={{ display: 'block', marginTop: '20px' }}>← Back to Home</Link>
    </div>
  );
}

export default UploadPage;
