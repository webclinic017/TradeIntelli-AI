import React from 'react';
import './TimeFrameSelector.css'; // Assuming your styles are here

function TimeFrameSelector({ selectedTimeFrame, onSelectTimeFrame }) {
    return (
        <select className="timeFrameSelector" value={selectedTimeFrame} onChange={e => onSelectTimeFrame(e.target.value)}>
            <option value="1H">1H</option>
            <option value="2H">2H</option>
            <option value="1D">1D</option>
        </select>
    );
}

export default TimeFrameSelector;
