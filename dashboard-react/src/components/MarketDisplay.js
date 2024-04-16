import React from 'react';

const MarketDisplay = ({ data }) => {
    return (
        <div style={{ display: 'flex', flexWrap: 'wrap' }}>
            {data.map((item, index) => (
                <div key={index} style={{ margin: '10px',
            padding: '20px',
            border: '1px solid #ccc',
            borderRadius: '8px',
            boxShadow: '0 2px 6px rgba(0,0,0,0.1)',
            maxWidth: '300px',
            textAlign: 'left' }}>
                    <h3>{item.instrumentName}</h3>
                    <p>Symbol: {item.symbol}</p>
                    <p>Epic: {item.epic}</p>
                    <p> Change:
                    <span style={{ color: item.percentageChange > 0 ? 'green' : 'red' }}>
                       %{item.percentageChange.toFixed(2)}
                    </span> </p>
                    <p> Net Change:
                    <span style={{ color: item.netChange > 0 ? 'green' : 'red' }}>
                          {item.netChange.toFixed(2)}
                    </span> </p>
                    <p>Bid: {item.bid}</p>
                    <p>marketStatus: {item.marketStatus}</p>
                </div>
            ))}
        </div>
    );
}

export default MarketDisplay;
