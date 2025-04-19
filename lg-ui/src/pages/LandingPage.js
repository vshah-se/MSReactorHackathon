import React from 'react';
import { Link } from 'react-router-dom';

function LandingPage() {
  return (
    <div style={styles.container}>
      <h1>Welcome to My App</h1>
      <p>This is the landing page.</p>
      <Link to="/upload" style={styles.link}>Go to PDF Upload</Link>
    </div>
  );
}

const styles = {
  container: {
    marginTop: '50px',
    textAlign: 'center',
    fontFamily: 'sans-serif'
  },
  link: {
    marginTop: '20px',
    display: 'inline-block',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    borderRadius: '8px',
    textDecoration: 'none'
  }
};

export default LandingPage;
