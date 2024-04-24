import React, { useState, useEffect } from 'react';
import MarketDisplay from './MarketDisplay';  // This will be your new display component

const MarketNavigation = () => {
    const [data, setData] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
    console.log(process.env.REACT_APP_API_BASE_URL)
        fetch(process.env.REACT_APP_API_BASE_URL + '/marketnavigation?category_id=hierarchy_v1.commons.most_traded')
            .then(response => response.json())
            .then(data => {
                setData(data); // Assuming 'data' is the object containing 'markets'
                setIsLoading(false);
            })
            .catch(error => {
                setError(error.message);
                setIsLoading(false);
            });
    }, []);

    if (isLoading) return <div>Loading...</div>;
    if (error) return <div>Error: {error}</div>;
    if (!data) return <div>No data available</div>;

    // Pass the data to the display component
    return <MarketDisplay data={data.markets} />;
}

export default MarketNavigation;
