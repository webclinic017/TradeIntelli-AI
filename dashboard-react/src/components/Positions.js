import React from 'react';

function Positions({ positions }) {
    if (!positions.length) {
        return <div>Loading positions or no positions found...</div>;
      }
  return (
    <div className="positions-container">
      <table>
        <thead>
          <tr>
            <th>Instrument</th>
            <th>createdDate</th>
            <th>Size</th>
            <th>Direction</th>
            <th>Level</th>
            <th>UPL</th>
            <th>leverage</th>
            <th>Market direction</th>
            <th>Market Status</th>
          </tr>
        </thead>
        <tbody>
          {positions.map((position, index) => (
            <tr key={index}>
              <td>{position.market.instrumentName}</td>
              <td>{position.position.createdDate}</td>
              <td>{position.position.size}</td>
              <td>{position.position.direction}</td>
              <td>{position.position.level}</td>
              <td style={{
                color: position.position.upl >= 0 ? 'green' : 'red'
              }}>
                {position.position.upl.toFixed(2)}
              </td>
              <td>{position.position.leverage}</td>
              <td>{position.position.direction}</td>
              <td>{position.market.marketStatus}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Positions;
