import React from 'react';
import { Link } from 'react-router-dom';

function LandingPage() {
  return (
    <div style={styles.container}>
      <h1>LeaseGuard</h1>
      <p>Have questions about your lease?
        Upload it here and we'll answer your questions!
      </p>
      <Link to="/upload" style={styles.link}>Upload Your Lease</Link>
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
    backgroundColor: '#606c38',
    color: 'white',
    borderRadius: '8px',
    textDecoration: 'none'
  }
};

export default LandingPage;
