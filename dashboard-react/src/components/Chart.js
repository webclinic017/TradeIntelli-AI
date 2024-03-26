// src/App.js
import React, { useState, useEffect } from 'react';
import CandlestickChart from './CandlestickChart';
import StockSelector from './StockSelector';
import TimeFrameSelector from './TimeFrameSelector';
import StartDateSelector from './StartDateSelector';
import './Chart.css';

function Chart({ id }) {
    const [selectedStock, setSelectedStock] = useState('BTC');
    const [selectedTimeFrame, setSelectedTimeFrame] = useState('1H'); // Default to 1D
    const [selectedStartDate, setSelectedStartDate] = useState('30'); // Default to 1D
    const [data, setData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true); // Start loading
            try {
                const response = await fetch('http://127.0.0.1:8000/historical-data/?stock='
                 + selectedStock + '&time_frame=' + selectedTimeFrame+ '&start_date=' + selectedStartDate);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
               const jsonData = await response.json();
                setData(jsonData);
            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
            setIsLoading(false); // End loading
        };

        fetchData();
    }, [selectedStock, selectedTimeFrame, selectedStartDate]);

    return (
            <div className="App">
            <div className="toolbar" id={id+"x"}>
                <StockSelector onSelect={setSelectedStock} />
                <StartDateSelector selectedStartDate={selectedStartDate} onSelectStartDate={setSelectedStartDate} />
                <TimeFrameSelector selectedTimeFrame={selectedTimeFrame} onSelectTimeFrame={setSelectedTimeFrame} />
            </div>
                {isLoading ? <p>Loading...</p> : <CandlestickChart data={data} id={id}/>}
            </div>
        );
    }


export default Chart;

