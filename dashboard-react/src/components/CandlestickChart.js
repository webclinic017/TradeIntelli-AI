// src/components/CandlestickChart.js
import React, { useEffect } from 'react';
import * as echarts from 'echarts';
import './Chart.css';
import upArrowUrl from '../upArrow.png';
import downArrowUrl from '../downArrow.png';

function CandlestickChart({ data, id  }) {
    useEffect(() => {
        if (data && data.length > 0) {
            const chartDom = document.getElementById(id);
            const myChart = echarts.init(chartDom);
            const marketDirection = data[data.length - 1].market_direction || "Uncertain";
            const ema_market_direction = data[data.length - 1].ema_market_direction || "Uncertain";
            const macd_market_direction = data[data.length - 1].macd_market_direction || "Uncertain";

            const option = {
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {
                        type: 'cross'
                    }
                },
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
                        symbol: 'none'
                    },
                    {
                        name: 'EMA100',
                        type: 'line',
                        data: data.map(item => item.EMA100),  // EMA 100 values
                        smooth: true,
                        color: 'red',
                        symbol: 'none' // Fuchsia
                    },
                    {
                        name: 'EMA50',
                        type: 'line',
                        data: data.map(item => item.EMA50),  // EMA 50 values
                        smooth: true,
                        color: 'green',
                        symbol: 'none'
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
                                formatter: 'Resistance: {c}',
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
                                formatter: 'Support: {c}',
                                color: 'green' // Match the line color
                            },
                        }]
                    }
                    }

                ],
                graphic: [
                    {
                        type: 'text',
                        left: 'center',
                        top: 20, // Adjusted for better visualization with the arrow
                        style: {
                            text: `Support and Resistance Market Direction: ${marketDirection}`, // Dynamic label
                            fill: marketDirection === "Bullish" ? 'green' : marketDirection === "Bearish" ? 'red' : 'grey',
                            fontSize: 15
                        }
                    },
                    {
                        type: 'text',
                        left: 'center',
                        top: 40, // Adjusted for better visualization with the arrow
                        style: {
                            text: `MACD Market Direction: ${macd_market_direction}`, // Dynamic label
                            fill: macd_market_direction === "Bullish" ? 'green' : macd_market_direction === "Bearish" ? 'red' : 'grey',
                            fontSize: 15
                        }
                    },
                    {
                        type: 'text',
                        left: 'center',
                        top: 60, // Adjusted for better visualization with the arrow
                        style: {
                            text: `EMA Market Direction: ${ema_market_direction}`, // Dynamic label
                            fill: ema_market_direction === "Bullish" ? 'green' : ema_market_direction === "Bearish" ? 'red' : 'grey',
                            fontSize: 15
                        }
                    },

                    {
                        type: 'image',
                        left: 'center',
                        top: 80, // Adjust based on the exact positioning you want
                        style: {
                            image: marketDirection === "Bullish" ? upArrowUrl : marketDirection === "Bearish" ? downArrowUrl : '',
                            width: 20,
                            height: 20
                        },
                        z: 100 // Ensure the image is displayed above other chart elements
                    }
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
                        params.forEach(param => {
                            if (param.seriesName === 'Candlestick') {
                                res += `
                                    Open: ${param.data[1]}<br/>
                                    Close: ${param.data[2]}<br/>
                                    Low: ${param.data[3]}<br/>
                                    High: ${param.data[4]}<br/>
                                `;

                                res += `Market direction: ${additionalData.market_direction}<br/>`;
                                res += `EMA Market direction: ${additionalData.ema_market_direction}<br/>`;
                                res += `MACD Market direction: ${additionalData.macd_market_direction}<br/>`;

                            } else {
                                res += `${param.seriesName}: ${param.value}<br/>`;
                            }


                        });
                        return res;
                    }
}


            };
            myChart.setOption(option);
        }
    }, [data, id]);

    return <div id={id} className="chart"></div>;
}

export default CandlestickChart;
