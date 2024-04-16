import React from 'react';
import ChartArray from './components/ChartArray';
import Navbar from './components/Navbar';
import StockMovers from './components/StockMovers';
import PositionsContainer from './components/PositionsContainer';
import './App.css';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import MarketNavigation from './components/MarketNavigation';
function App() {
  return (
    <Router>
      <div className="MainApp">
        <Navbar />
        <header className="App-header">
        </header>
        <Routes>
          <Route path="/" element={<MarketNavigation />} />
          <Route path="/chartarray" element={<ChartArray />} />
          <Route path="/positions" element={<PositionsContainer />} />
          <Route path="/marketnavigation" element={<MarketNavigation />} />
          <Route path="/stockmovers" element={<StockMovers />} />

        </Routes>
      </div>
    </Router>
  );
}


export default App;
