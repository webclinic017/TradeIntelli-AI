import React from 'react';
import './TimeFrameSelector.css'; // Assuming your styles are here

const symbol_map = {
    'BTC': 'BTC',
    'gold': 'gold',
    'nvidia': 'nvidia',
    'ndx100': 'ndx100',
    'spx500': 'spx500',
    'arm': 'arm'
};

function StockSelector({ onSelect }) {
    return (
        <select className="timeFrameSelector" onChange={(e) => onSelect(e.target.value)}>
            {Object.entries(symbol_map).map(([key, value]) => (
                <option key={key} value={value}>
                    {key.charAt(0).toUpperCase() + key.slice(1)} ({value})
                </option>
            ))}
        </select>
    );
}

export default StockSelector;
