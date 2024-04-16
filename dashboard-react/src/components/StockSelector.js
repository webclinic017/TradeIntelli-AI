import React, { useState } from 'react';
import './TimeFrameSelector.css'; // Assuming your styles are here

const initialSymbols = {
    'BTC': 'BTC',
    'gold': 'gold',
    'nvidia': 'nvidia',
    'ndx100': 'ndx100',
    'spx500': 'spx500',
    'arm': 'arm'
};

function StockSelector({ onSelect }) {
    const [symbols, setSymbols] = useState(initialSymbols);
    const [inputValue, setInputValue] = useState('');
    const [selectedValue, setSelectedValue] = useState('');

    const handleInputChange = (event) => {
        setInputValue(event.target.value);
    };

    const handleKeyPress = (event) => {
        if (event.key === 'Enter' && inputValue && !Object.hasOwn(symbols, inputValue)) {
            const newSymbols = {
                ...symbols,
                [inputValue]: inputValue
            };
            setSymbols(newSymbols);
            setSelectedValue(inputValue);
            onSelect(inputValue);
            setInputValue('');
        }
    };

    const handleSelectionChange = (event) => {
        setSelectedValue(event.target.value);
        onSelect(event.target.value);
    };

    return (
        <div>
            <input
                type="text"
                value={inputValue}
                onChange={handleInputChange}
                onKeyPress={handleKeyPress}
                placeholder="Type new symbol and press Enter..."
            />
            <select className="timeFrameSelector" onChange={handleSelectionChange} value={selectedValue}>
                {Object.entries(symbols).map(([key, value]) => (
                    <option key={key} value={value}>
                        {key.charAt(0).toUpperCase() + key.slice(1)} ({value})
                    </option>
                ))}
            </select>
        </div>
    );
}

export default StockSelector;
