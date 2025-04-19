import React, { useState } from 'react';
import axios from 'axios';

const UploadPage = () => {
  const [file, setFile] = useState(null); // To store selected file
  const [error, setError] = useState(''); // To store error message
  const [success, setSuccess] = useState(''); // To store success message

  // Handle file selection
  const handleChange = (e) => {
    const selected = e.target.files[0]; // Get selected file
    if (selected && selected.type === 'application/pdf') { // Ensure it's a PDF
      setFile(selected); // Store the file in the state
      setError(''); // Clear any existing errors
    } else {
      setFile(null); // Reset file if it's not a PDF
      setError('Please select a PDF file'); // Show error message
    }
  };

  // Handle form submission
  const handleSubmit = async (e) => {
    e.preventDefault(); // Prevent default form behavior (page reload)

    // Check if a file is selected
    if (!file) {
      setError('Please choose a file first');
      return; // Exit if no file is selected
    }

    const formData = new FormData(); // Create a new FormData object
    formData.append('file', file); // Append the file to FormData with the 'file' key

    try {
      // Send the POST request to the backend
      const response = await axios.post('http://localhost:5000/upload', formData, {
        headers: {
          'Content-Type': 'multipart/form-data', // Set the correct content type for file uploads
        },
      });

      // On successful upload, handle the response
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
