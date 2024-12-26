import React, { useState } from 'react';
// @ts-ignore
import CanvasJSReact from '@canvasjs/react-charts';

const { CanvasJSChart } = CanvasJSReact;

const ArimaChart: React.FC<{ jsonData: any }> = ({ jsonData }) => {
    const [chartType, setChartType] = useState('line'); // State to manage chart type

    // Log the raw jsonData to inspect its structure
    console.log('Raw jsonData:', jsonData);

    // Ensure the required data exists
    if (!jsonData?.data?.jsonData?.length || !jsonData.data.jsonData[0].data[0].jsonData) {
        return <div>No data available to display</div>;
    }

    // Extract and transform the data for the chart
    const transformedData = jsonData.data.jsonData[0].data[0].jsonData.map((zoneData: any) => ({
        type: chartType,  // Dynamically change the chart type based on the state
        name: zoneData.zone,
        showInLegend: true,
        dataPoints: zoneData.forecast.map(([date, value]: [string, number]) => {
            const parsedDate = new Date(date);
            return {
                x: parsedDate.getTime() ? parsedDate : new Date(),
                y: value,
            };
        }),
    }));

    console.log('Transformed Data:', transformedData);

    if (!transformedData || transformedData.length === 0) {
        return <div>No valid forecast data available to display</div>;
    }

    // Set chart options
    const options = {
        animationEnabled: true,
        animationDuration: 2000,
        exportFileName: "Arima Chart",
        exportEnabled: true,
        zoomEnabled: true,
        title: {
            text: 'Dynamic Multi-Zone Forecast Chart',
        },
        axisX: {
            title: 'Date',
            valueFormatString: 'YYYY-MM-DD', // Format for displaying date
        },
        axisY: {
            title: 'Value',
        },
        data: transformedData, // Use the transformed data
    };

    // Function to handle the type change
    const handleTypeChange = (event: React.ChangeEvent<HTMLSelectElement>) => {
        setChartType(event.target.value);  // Update the chart type based on user selection
    };

    return (
        <div className={"chartDiv"}>
            <h2>Chart Example</h2>

            {/* Dropdown to select chart type */}
            <select onChange={handleTypeChange} value={chartType}>
                <option value="line">Line</option>
                <option value="column">Column</option>
                <option value="area">Area</option>
                <option value="spline">Spline</option>
                <option value="scatter">Scatter</option>
            </select>

            <CanvasJSChart options={options} />
        </div>
    );
};

export default ArimaChart;
