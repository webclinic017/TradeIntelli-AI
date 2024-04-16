import React from 'react';
import { NavLink } from 'react-router-dom';
import logo from '../logo.png';
import './Navbar.css'; // Assuming the CSS is in Navbar.css

const Navbar = () => {

  return (
    <nav className="navbar">
      <img src={logo} alt="App Logo" className="navbar-logo" />
       <div className="navbar-links">
        <NavLink to="/chartarray" activeClassName="active">Chart</NavLink>
        <NavLink to="/positions" activeClassName="active">Portfolio</NavLink>
        <NavLink to="/marketnavigation" activeClassName="active">Most Traded</NavLink>
        <NavLink to="/stockmovers" activeClassName="active">Top Movers</NavLink>

      </div>

    </nav>
  );
};

export default Navbar;
