import React, { useState, useEffect, useRef } from 'react';
import CanvasDraw from "react-canvas-draw";
import CandlestickChart from './CandlestickChart';
import StockSelector from './StockSelector';
import TimeFrameSelector from './TimeFrameSelector';
import StartDateSelector from './StartDateSelector';
import './Chart.css';

function Chart({ id }) {
    const [selectedStock, setSelectedStock] = useState('BTC');
    const [selectedTimeFrame, setSelectedTimeFrame] = useState('5M');
    const [selectedStartDate, setSelectedStartDate] = useState('60');
    const [data, setData] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const [isDrawingEnabled, setIsDrawingEnabled] = useState(false);
    const drawingCanvasRef = useRef(null);


    const clearDrawing = () => {
        drawingCanvasRef.current.clear();
    };
    useEffect(() => {
        const fetchData = async () => {
            setIsLoading(true);
            try {
                const response = await fetch(`http://127.0.0.1:8000/historical-data/?stock=${selectedStock}&time_frame=${selectedTimeFrame}&start_date=${selectedStartDate}`);
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const jsonData = await response.json();
                setData(jsonData);
            } catch (error) {
                console.error('Failed to fetch data:', error);
            }
            setIsLoading(false);
        };

        fetchData();
    }, [selectedStock, selectedTimeFrame, selectedStartDate]);

    const toggleDrawing = () => setIsDrawingEnabled(!isDrawingEnabled);

    return (
        <div className="App">
            <div className="toolbar" id={`${id}x`}>
                <StockSelector onSelect={setSelectedStock} />
                <StartDateSelector selectedStartDate={selectedStartDate} onSelectStartDate={setSelectedStartDate} />
                <TimeFrameSelector selectedTimeFrame={selectedTimeFrame} onSelectTimeFrame={setSelectedTimeFrame} />
                <button onClick={toggleDrawing}>{isDrawingEnabled ? 'Stop Drawing' : 'Start Drawing'}</button>
                <button onClick={clearDrawing}>Clear Drawing</button>
            </div>
            {isLoading ? <p>Loading...</p> : (
                <div className="chartWithDrawing">
                    <CandlestickChart data={data} id={id}/>
                    <CanvasDraw
                        ref={drawingCanvasRef}
                        disabled={!isDrawingEnabled}
                        style={{
                            position: 'absolute',
                            top: 0,
                            left: 0,
                            zIndex: 10,
                            pointerEvents: isDrawingEnabled ? 'all' : 'none',
                            // Temporary background color for visibility when drawing is enabled
                            backgroundColor: isDrawingEnabled ? 'rgba(255,255,255,0.3)' : 'transparent',
                        }}
                        canvasWidth={1600}
                        canvasHeight={800}
                        hideGrid={true}
                        brushRadius={4}
                    />
                </div>
            )}
        </div>
    );
}

export default Chart;
