import React from 'react';
import './TimeFrameSelector.css'; // Assuming your styles are here

function TimeFrameSelector({ selectedTimeFrame, onSelectTimeFrame }) {
    const timeFrames = ['1M', '5M', '10M', '30M', '1H', '4H', '1D'];

    return (
        <div className="timeFrameSelector">
            {timeFrames.map(timeFrame => (
                <button
                    key={timeFrame}
                    className={`timeFrameButton ${selectedTimeFrame === timeFrame ? 'selected' : ''}`}
                    onClick={() => onSelectTimeFrame(timeFrame)}
                >
                    {timeFrame}
                </button>
            ))}
        </div>
    );
}

export default TimeFrameSelector;
