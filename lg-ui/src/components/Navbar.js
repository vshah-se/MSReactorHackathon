import React from 'react';
import { NavLink } from 'react-router-dom';

const Navbar = () => {
  return (
    <nav style={styles.nav}>
      <h1 style={styles.logo}>📄 MyApp</h1>
      <div style={styles.links}>
        <NavLink to="/" style={styles.link} end>Home</NavLink>
        <NavLink to="/upload" style={styles.link}>Upload</NavLink>
        <NavLink to="/chat" style={styles.link}>Chat</NavLink>
      </div>
    </nav>
  );
};

const styles = {
  nav: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '10px 20px',
    backgroundColor: '#007bff',
    color: 'white',
    fontFamily: 'sans-serif',
  },
  logo: {
    margin: 0,
  },
  links: {
    display: 'flex',
    gap: '20px',
  },
  link: ({ isActive }) => ({
    color: isActive ? '#ffc107' : 'white',
    textDecoration: 'none',
    fontWeight: 'bold',
  }),
};

export default Navbar;
