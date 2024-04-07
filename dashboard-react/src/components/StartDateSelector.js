import React from 'react';
import './StartDateSelector.css'; // Assuming your styles are here

function StartDateSelector({ selectedStartDate, onSelectStartDate }) {
    return (
        <select className="StartDateSelector" value={selectedStartDate} onChange={e => onSelectStartDate(e.target.value)}>
            <option value="0">Auto</option>
            <option value="30">30M</option>
            <option value="60">1H</option>
            <option value={`${60*5}`}>5H</option>
            <option value={`${60*24}`}>1D</option>
            <option value={`${60*24*7}`}>7D</option>
        </select>
    );
}

export default StartDateSelector;
