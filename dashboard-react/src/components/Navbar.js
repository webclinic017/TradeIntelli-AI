import React from 'react';
import logo from '../logo.png';

const Navbar = () => {
  return (
    <nav className="navbar">
      <img src={logo} alt="App Logo" className="navbar-logo" />
      <div className="title">Chart </div>
    </nav>
  );
};

export default Navbar;
