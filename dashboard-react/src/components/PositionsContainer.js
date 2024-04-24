import React, { useState, useEffect } from 'react';
import Positions from './Positions';

function PositionsContainer() {
  const [positions, setPositions] = useState([]);
  const [accountInfo, setAccountInfo] = useState(null);

  useEffect(() => {
    // Fetch positions
    fetch('http://localhost:8000/capital-open-position')
      .then(response => response.json())
      .then(data => setPositions(data.positions))
      .catch(error => console.error('Error fetching positions:', error));

    // Fetch account information
    fetch('http://localhost:8000/capital-account_info')
      .then(response => response.json())
      .then(data => setAccountInfo(data.accounts[0]))  // Assuming we're interested in the first account
      .catch(error => console.error('Error fetching account information:', error));
  }, []);  // The empty array ensures these effects run only once after the component mounts.

  if (!accountInfo || positions.length === 0) {
    return <div>Loading data...</div>;
  }
    const profitLossStyle = {
        color: accountInfo.balance.profitLoss >= 0 ? 'green' : 'red'
      };
  return (
    <>
      <div>
        <h3>Account Information</h3>
        <p>Account Name: {accountInfo.accountName}</p>
        <p>Account Type: {accountInfo.accountType}</p>
        <p>Balance: {accountInfo.balance.balance} {accountInfo.symbol}</p>
        <p>Available Funds: {accountInfo.balance.available} {accountInfo.symbol}</p>
        <p style={profitLossStyle}>Profit/Loss: {accountInfo.balance.profitLoss.toFixed(2)} {accountInfo.symbol}</p>

      </div>
      <Positions positions={positions} />
    </>
  );
}

export default PositionsContainer;
