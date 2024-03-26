// src/components/CandlestickChart.js
import React, { useEffect } from 'react';
import * as echarts from 'echarts';
import './Chart.css';

function CandlestickChart({ data, id  }) {
    useEffect(() => {
        if (data) {
            const chartDom = document.getElementById(id);
            const myChart = echarts.init(chartDom);
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

                ]
            };
            myChart.setOption(option);
        }
    }, [data, id]);

    return <div id={id} className="chart"></div>;
}

export default CandlestickChart;
