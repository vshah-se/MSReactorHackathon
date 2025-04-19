import React, { useState } from 'react';
import axios from 'axios';

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState(''); 
  const [success, setSuccess] = useState(''); 

  const handleChange = (e) => {
    const selected = e.target.files[0]; 
    if (selected && selected.type === 'application/pdf') { // Check PDF type
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
    formData.append('file', file); 

    try {
      // Send the POST request to the backend
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Set the correct content type for file uploads
        },
      });

      setSuccess(`File uploaded successfully! Server says: ${response.data.message}`);
      setFile(null); // Reset file input
    } catch (err) {
      console.error(err);
      setError('Upload failed. Please try again.');
    }
  };

  return (
    <div>
      <h2>Upload a PDF File</h2>
      <form onSubmit={handleSubmit}>
        <input type="file" accept="application/pdf" onChange={handleChange} />
        <button type="submit">Upload</button>
      </form>

      {error && <p style={{ color: 'red' }}>{error}</p>} {/* Display error message */}
      {success && <p style={{ color: 'green' }}>{success}</p>} {/* Display success message */}
    </div>
  );
};

export default UploadPage;
