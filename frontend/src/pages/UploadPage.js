import React, { useState } from 'react';
import axios from 'axios';
import './UploadPage.css'; // 👈 Create this file for styling

const UploadPage = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

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
    formData.append('file', file);

    try {
      const response = await axios.post('http://localhost:5000/upload-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      setSuccess(`File uploaded successfully! Server says: ${response.data.message}`);
      setFile(null);
    } catch (err) {
      console.error(err);
      setError('Upload failed. Please try again.');
    }
  };

  return (
    <div className="upload-wrapper">
      <div className="upload-box">
        <h2>📄 Upload a PDF File</h2>
        <form onSubmit={handleSubmit}>
          <input type="file" accept="application/pdf" onChange={handleChange} />
          <button type="submit">Upload</button>
        </form>
        {error && <p className="error">{error}</p>}
        {success && <p className="success">{success}</p>}
      </div>
    </div>
  );
};

export default UploadPage;
