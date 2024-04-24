import React, { useState, useEffect } from 'react';
import './TimeFrameSelector.css'; // Assuming your styles are here

function StockSelector({ onSelect }) {
    const [symbols, setSymbols] = useState({});
    const [inputValue, setInputValue] = useState('');
    const [selectedValue, setSelectedValue] = useState('');

    useEffect(() => {
        fetch("http://16.171.39.64:8000/marketnavigation?category_id=hierarchy_v1.commons.most_traded&limit=30")
            .then(response => response.json())
            .then(data => {
                const fetchedSymbols = data.markets.reduce((acc, market) => {
                    acc[market.instrumentName] = market.epic;
                    return acc;
                }, {});
                setSymbols(fetchedSymbols);
                if (data.markets.length > 0) {
                    const firstSymbol = data.markets[0].epic;
                    setSelectedValue(firstSymbol);
                    onSelect(firstSymbol);
                }
            })
            .catch(error => console.error('Error fetching symbols:', error));
    }, [onSelect]);

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
        <div className="tool-group">
            <input
            className="timeFrameSelector"
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
