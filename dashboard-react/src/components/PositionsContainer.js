import React, { useState, useEffect } from 'react';
import Positions from './Positions';

function PositionsContainer() {
  const [positions, setPositions] = useState([]);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/capital-open-position')
      .then(response => response.json())
      .then(data => setPositions(data.positions))
      .catch(error => console.error('Error fetching positions:', error));
  }, []); // The empty array ensures this effect runs only once after the component mounts.

  return <Positions positions={positions} />;
}

export default PositionsContainer;
