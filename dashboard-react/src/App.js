import React from 'react';
import ChartArray from './components/ChartArray';
import Navbar from './components/Navbar'; // Adjust the path based on your file structure
import './App.css';

function App() {
  return (
    <div className="MainApp">
      <Navbar />
      <header className="App-header">
      </header>
      <ChartArray/>
    </div>
  );
}


export default App;
