// ChartArray.js

import React, { useState } from 'react';
import Chart from './Chart'; // Ensure this path matches where your Chart component is located

const ChartArray = () => {
    const [charts, setCharts] = useState([{ id: `chart${Date.now()}` }]);

    const addChart = () => {
        setCharts(charts.concat({ id: `chart${Date.now()}` }));
    };

    const removeChart = idToRemove => {
        setCharts(charts.filter(chart => chart.id !== idToRemove));
    };

    return (
        <div>
            {charts.map(({ id }) => (
                <div key={id}>
                    <Chart id={id} />
                    <button onClick={() => removeChart(id)}>Remove this chart</button>
                </div>
            ))}
            <button onClick={addChart}>Add another chart</button>
        </div>
    );
};

export default ChartArray;
