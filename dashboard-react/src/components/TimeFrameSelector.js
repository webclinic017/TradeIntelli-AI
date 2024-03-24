import React from 'react';

function TimeFrameSelector({ selectedTimeFrame, onSelectTimeFrame }) {
    return (
        <select value={selectedTimeFrame} onChange={e => onSelectTimeFrame(e.target.value)}>
            <option value="30M">30M</option>
            <option value="1H">1H</option>
            <option value="2H">2H</option>
            <option value="1D">1D</option>
        </select>
    );
}

export default TimeFrameSelector;
