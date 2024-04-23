// src/components/CandlestickChart.js
import React, { useEffect, useState } from 'react';
import * as echarts from 'echarts';
import './Chart.css';
import upArrowUrl from '../upArrow.png';
import downArrowUrl from '../downArrow.png';

function CandlestickChart({ data, id  }) {

    const [theme, setTheme] = useState('light');
    useEffect(() => {
        if (data && data.length > 0) {
            const chartDom = document.getElementById(id);
            const myChart = echarts.init(chartDom, theme);
            const marketDirection = data[data.length - 1].market_direction || "Uncertain";
            const ema_market_direction = data[data.length - 1].ema_market_direction || "Uncertain";
            const macd_market_direction = data[data.length - 1].macd_market_direction || "Uncertain";

            const startZoom = (data.length > 100) ? ((data.length - 100) / data.length * 100) : 0;
            const ZoomWindowSize = 100;
            const option = {
                xAxis: {
                    type: 'category',
                    data: data.map(item => item.date)  // Dates
                },
                yAxis: {
                    scale: true
                },
                series: [
                    {
                        name: 'Candlestick',
                        type: 'candlestick',
                        data: data.map(item => [item.open, item.close, item.low, item.high]),  // OHLC
                        itemStyle: {
                            color: '#00ff00',
                            color0: '#ff0000',
                            borderColor: null,
                            borderColor0: null
                        }
                    },

                    {
                        name: 'EMA200',
                        type: 'line',
                        data: data.map(item => item.EMA200),  // EMA 200 values
                        smooth: true,
                        color: 'black',
                        symbol: 'none',
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    symbolSize: 0,  // Adjust the size of the mark point symbol if necessary
                                    label: {
                                        show: true,
                                        position: 'right',  // Label will be on the right; adjust as needed
                                        formatter: function (params) {
                                            return params.value.toFixed(2);  // Displays the value of the mark point
                                        },
                                        color: 'black'
                                    },
                                },
                                {
                                    type: 'min',
                                    symbolSize: 0,  // Adjust the size of the mark point symbol if necessary
                                    label: {
                                        show: true,
                                        position: 'right',  // Label will be on the right; adjust as needed
                                        formatter: function (params) {
                                            return params.value.toFixed(2);  // Displays the value of the mark point
                                        },
                                        color: 'black'
                                    },
                                },
                            ]
                        }
                    },
                    {
                        name: 'EMA100',
                        type: 'line',
                        data: data.map(item => item.EMA100),  // EMA 100 values
                        smooth: true,
                        color: 'red',
                        symbol: 'none',
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    symbolSize: 0,  // Adjust the size of the mark point symbol if necessary
                                    label: {
                                        show: true,
                                        position: 'right',  // Label will be on the right; adjust as needed
                                        formatter: function (params) {
                                            return params.value.toFixed(2);  // Displays the value of the mark point
                                        },
                                        color: 'red'
                                    },
                                },
                                {
                                    type: 'min',
                                    symbolSize: 0,  // Adjust the size of the mark point symbol if necessary
                                    label: {
                                        show: true,
                                        position: 'right',  // Label will be on the right; adjust as needed
                                        formatter: function (params) {
                                            return params.value.toFixed(2);  // Displays the value of the mark point
                                        },
                                        color: 'red'
                                    },
                                },
                            ]
                        }
                    },
                    {
                        name: 'EMA50',
                        type: 'line',
                        data: data.map(item => item.EMA50),  // EMA 50 values
                        smooth: true,
                        color: 'green',
                        symbol: 'none',
                        markPoint: {
                            data: [
                                {
                                    type: 'max',
                                    symbolSize: 0,  // Adjust the size of the mark point symbol if necessary
                                    label: {
                                        show: true,
                                        position: 'right',  // Label will be on the right; adjust as needed
                                        formatter: function (params) {

                                            return params.value.toFixed(2);  // Displays the value of the mark point
                                        },
                                        color: 'green'
                                    },
                                },
                                {
                                    type: 'min',
                                    symbolSize: 0,  // Adjust the size of the mark point symbol if necessary
                                    label: {
                                        show: true,
                                        position: 'right',  // Label will be on the right; adjust as needed
                                        formatter: function (params) {
                                            return params.value.toFixed(2);  // Displays the value of the mark point
                                        },
                                        color: 'green'
                                    },
                                },
                            ]
                        }
                    },
                    {
                        name: 'Resistance',
                        type: 'line',
                        data: data.map(item => item.resistance),
                        smooth: true,
                        color: 'red',
                        symbol: 'none'
                        ,
                        markLine: {
                        silent: true, // Makes the markLine non-interactive
                        data: [{
                            yAxis: Math.max(...data.map(item => item.resistance)), // The constant support value you want to display
                            label: {
                                show: true, // Show the label
                                position: 'end', // Position it at the end of the line
                                formatter: '{c} Resistance',
                                color: 'red' // Match the line color
                            },
                        }]
                    }
                    } ,
                    {
                        name: 'Support',
                        type: 'line',
                        data: data.map(item => item.support),
                        smooth: true,
                        color: 'green',
                        symbol: 'none'
                        ,
                        markLine: {
                        silent: true,
                        data: [{
                            yAxis: Math.max(...data.map(item => item.support)), // The constant support value you want to display
                            label: {
                                show: true, // Show the label
                                position: 'end', // Position it at the end of the line
                                formatter: '{c} Support',
                                color: 'green' // Match the line color
                            },
                        }]
                    }
                    }

                ],
                graphic: [
                    {
                        type: 'text',
                        left: 100,
                        top: 20, // Adjusted for better visualization with the arrow
                        style: {
                            text: `S&R: ${marketDirection}`, // Dynamic label
                            fill: marketDirection === "Bullish" ? 'green' : marketDirection === "Bearish" ? 'red' : 'grey',
                            fontSize: 15
                        }
                    },
                    {
                        type: 'image',
                        left: 200,
                        top: 20, // Adjust based on the exact positioning you want
                        style: {
                            image: marketDirection === "Bullish" ? upArrowUrl : marketDirection === "Bearish" ? downArrowUrl : '',
                            width: 20,
                            height: 20
                        },
                        z: 100 // Ensure the image is displayed above other chart elements
                    },
                    {
                        type: 'text',
                        left: 300,
                        top: 20, // Adjusted for better visualization with the arrow
                        style: {
                            text: `MACD: ${macd_market_direction}`, // Dynamic label
                            fill: macd_market_direction === "Bullish" ? 'green' : macd_market_direction === "Bearish" ? 'red' : 'grey',
                            fontSize: 15
                        }
                    },
                    {
                        type: 'text',
                        left: 500,
                        top: 20, // Adjusted for better visualization with the arrow
                        style: {
                            text: `EMA: ${ema_market_direction}`, // Dynamic label
                            fill: ema_market_direction === "Bullish" ? 'green' : ema_market_direction === "Bearish" ? 'red' : 'grey',
                            fontSize: 15
                        }
                    },


                ],
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    },
                    formatter: function (params) {
                        const dataIndex = params[0].dataIndex; // Assuming all series have the same dataIndex
                        const additionalData = data[dataIndex];
                        let res = `${params[0].name}<br/>`; // Starting with the name (usually the date)
                        let leverage = 100;
                        let amount_invested = 100;

                        const getDirectionHtml = (direction) => {
                            let color = 'grey'; // Default color
                            let arrow = '➖'; // Default arrow for 'Uncertain'
                            if (direction === 'Bullish') {
                                color = 'green';
                                arrow = '🔼'; // Up arrow for 'Bullish'
                            } else if (direction === 'Bearish') {
                                color = 'red';
                                arrow = '🔽'; // Down arrow for 'Bearish'
                            }
                            return `<span style="color: ${color};">${arrow} ${direction}</span>`;
                        };
                        params.forEach(param => {
                                if (param.seriesName === 'Candlestick') {
                                     res += `
                                            <div style="text-align: left;">  <!-- Align text to the left -->
                                                <strong>Price:</strong><br/>
                                                Open: ${Number(param.data[1]).toFixed(3)}<br/>
                                                Close: ${Number(param.data[2]).toFixed(3)}<br/>
                                                Low: ${Number(param.data[3]).toFixed(3)}<br/>
                                                High: ${Number(param.data[4]).toFixed(3)}<br/>

                                                <strong>Market direction:</strong><br/>
                                                S&R: ${getDirectionHtml(additionalData.market_direction)}<br/>
                                                EMA : ${getDirectionHtml(additionalData.ema_market_direction)}<br/>
                                                MACD: ${getDirectionHtml(additionalData.macd_market_direction)}<br/>

                                                <strong>Indicators Performance $ ${amount_invested}, leverage 1:${leverage}:</strong><br/>
                                                todo: use start price to callable profit in dollar <br/>
                                                ema_profit: ${additionalData.ema_profit.toFixed(2)} pip,
                                                 $ ${(additionalData.ema_profit/param.data[1]*amount_invested*leverage).toFixed(2)}<br/>

                                                macd_profit: ${additionalData.macd_profit.toFixed(2)} pip,
                                                 $ ${(additionalData.macd_profit/param.data[1]*amount_invested*leverage).toFixed(2)}<br/>

                                                s_r_profit: ${additionalData.s_r_profit.toFixed(2)} pip,
                                                 $ ${(additionalData.s_r_profit/param.data[1]*amount_invested*leverage).toFixed(2)}<br/>

                                                <strong>Indicators:</strong><br/>
                                                macd_histogram: ${additionalData.macd_histogram.toFixed(2)}<br/>

                                            </div>
                                            `;

                                } else {
                                    res += `<div style="text-align: left;">${param.seriesName}: ${Number(param.value).toFixed(3)}</div>`;
                                }


                        });
                        return res;
                    }
                },
                dataZoom: [
                        {
                            type: 'inside', // This enables a slider at the bottom of the chart for horizontal scrolling
                            xAxisIndex: [0], // This targets the first (and only in this case) xAxis defined by the chart configuration
                            start: startZoom, // This sets the starting zoom range to 0%
                            end: ZoomWindowSize  // This can be set to a smaller value if you want to start with a zoomed in view
                        },
                        {
                            type: 'slider', // This enables a slider at the bottom of the chart for horizontal scrolling
                            xAxisIndex: [0], // This targets the first (and only in this case) xAxis defined by the chart configuration
                            start: startZoom, // This sets the starting zoom range to 0%
                            end: ZoomWindowSize  // This can be set to a smaller value if you want to start with a zoomed in view
                        }
                    ],
                grid: {
                    left: '3%',
                    right: '4%',
                    bottom: '3%',
                    containLabel: true
                },
                toolbox: {
                        show: true,
                       feature: {
            saveAsImage: {
                show: true,
                title: 'Save'
            },

            restore: {
                show: true,
                title: 'Restore'
            },

        },
                    right: 20  // Position the toolbox to the right for better accessibility
                },

            };
            myChart.setOption(option);
            return () => {
        myChart.dispose();  // Cleanup: make sure to dispose on component unmount
    };
        }
    }, [data, id, theme]);

        const toggleTheme = () => {

                setTheme(currentTheme => currentTheme === 'dark' ? 'light' : 'dark');
            };

    return (
            <div style={{ textAlign: 'left'}}> {/* Container styled to align contents to the right */}
            <button
                onClick={toggleTheme}
                style={{
                    cursor: 'pointer',
                    padding: '5px 10px',
                    fontSize: '16px',
                    border: 'none',
                    borderRadius: '20px',
                    backgroundColor: theme === 'dark' ? '#555' : '#DDD',
                    color: theme === 'dark' ? '#FFF' : '#333',
                    outline: 'none',
                    transition: 'all 0.3s ease'
                }}
                     >
                {theme === 'light' ? 'Dark Mode' : 'Light Mode'}
            </button>
                <div id={id} className="chart"></div>

            </div>
        );
}

export default CandlestickChart;
