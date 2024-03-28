import React from 'react';
import logo from '../logo.png';

const Navbar = () => {
  return (
    <nav className="navbar">
      <img src={logo} alt="App Logo" className="navbar-logo" />
      {/* Add other navbar links or elements here */}
    </nav>
  );
};

export default Navbar;
