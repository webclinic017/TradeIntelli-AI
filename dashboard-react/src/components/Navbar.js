import React, { useState } from 'react';
import { NavLink } from 'react-router-dom';
import logo from '../logo.png';
import './Navbar.css'; // Assuming the CSS is in Navbar.css

const Navbar = () => {
  const [isNavExpanded, setIsNavExpanded] = useState(false);

  return (
    <nav className="navbar">
      <img src={logo} alt="App Logo" className="navbar-logo" />
       <div className={`navbar-links ${isNavExpanded ? "expanded" : ""}`}>
        <NavLink to="/stockmovers" activeClassName="active">Top Movers</NavLink>
        <NavLink to="/chartarray" activeClassName="active">Chart</NavLink>
      </div>

    </nav>
  );
};

export default Navbar;
