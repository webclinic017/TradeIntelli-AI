import React from 'react';
import { Link } from 'react-router-dom';
import logo from '../logo.png';

const Navbar = () => {
  return (
    <nav className="navbar">
      <img src={logo} alt="App Logo" className="navbar-logo" />
      <div className="title">Chart </div>
      <ul className="navbar-links">
        <li><Link to="/stockmovers">Stock Movers</Link></li>
        <li><Link to="/chartarray">Chart Array</Link></li>
      </ul>
    </nav>
  );
};

export default Navbar;
