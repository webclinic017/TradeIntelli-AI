import React from 'react';

const MarketDisplay = ({ data }) => {
    return (
        <div style={{ display: 'flex', flexWrap: 'wrap' }}>
            {data.map((item, index) => (
                <div key={index} style={{ margin: 10, padding: 10, border: '1px solid #ccc' }}>
                    <h3>{item.symbol}</h3>
                    <p>Percentage Change: % {item.percentageChange}</p>
                    <p>Bid: {item.bid}</p>
                    <p>marketStatus: {item.marketStatus}</p>
                </div>
            ))}
        </div>
    );
}

export default MarketDisplay;