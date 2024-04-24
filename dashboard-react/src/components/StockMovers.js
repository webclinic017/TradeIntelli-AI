import React, { useEffect, useState } from 'react';

const StockMovers = () => {
  const [data, setData] = useState({ gainers: [], losers: [], last_updated: '', market_type: '' });
  const [images, setImages] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://16.171.39.64:8000/stocks-movers');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const data = await response.json();
        setData(data);
//      fetchCompanyImages([...data.gainers, ...data.losers]); // Fetch images for both gainers and losers
      } catch (error) {
        console.error('There was a problem with your fetch operation:', error);
      }
    };

    fetchData();
  }, []);

  const fetchCompanyImages = async (stocks) => {
    const imageUrls = {};
    for (const stock of stocks) {
      try {
      const response = await fetch("https://financialmodelingprep.com/api/v3/profile/" + stock.symbol + "?apikey=n4E9vmgHW1EyBnbkl9Bq5y0mOGOZjI1r");
        if (!response.ok) {
          throw new Error('Failed to fetch company profile');
        }
        const [profile] = await response.json();
        console.log("profile:" + profile)

        imageUrls[stock.symbol] = profile.image; // Store the image URL using the stock symbol as the key
      } catch (error) {
        console.error(`There was a problem fetching the company image for ${stock.symbol}:`, error);
      }
    }
    setImages(imageUrls);
  };


  return (
    <div>
      <h2>Stock Movers - {data.market_type.charAt(0).toUpperCase() + data.market_type.slice(1)}</h2>
      <h3>Last Updated: {new Date(data.last_updated).toLocaleString()}</h3>
      <div style={{ display: 'flex', justifyContent: 'space-around', flexWrap: 'wrap' }}>
        <div>
          <h4>Gainers</h4>
          {data.gainers.map((stock, index) => (
            <div key={index} style={{ border: '1px solid green', padding: '10px', marginBottom: '10px' }}>
             <p>Symbol: {stock.symbol}</p>
              <p>Price: ${stock.price}</p>
              <p>Change: ${stock.change} ({stock.percent_change}%)</p>
            </div>
          ))}
        </div>
        <div>
          <h4>Losers</h4>
          {data.losers.map((stock, index) => (
            <div key={index} style={{ border: '1px solid red', padding: '10px', marginBottom: '10px' }}>
             <p>Symbol: {stock.symbol}</p>
              <p>Price: ${stock.price}</p>
              <p>Change: ${stock.change} ({stock.percent_change}%)</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default StockMovers;
