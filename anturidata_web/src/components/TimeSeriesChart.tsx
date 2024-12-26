import React, { useState } from 'react';
// @ts-ignore
import CanvasJSReact from '@canvasjs/react-charts';

const { CanvasJSChart } = CanvasJSReact;

const ChartTimeSeries: React.FC<{ jsonData: any }> = ({ jsonData }) => {
    const [chartType, setChartType] = useState('line'); // State to manage chart type

    // Log the raw jsonData to inspect its structure
    console.log('Raw jsonData:', jsonData);

    const zoneData = jsonData?.data?.jsonData?.[0]?.data?.[0];
    if (!zoneData) {
        return <div>No data available to display</div>;
    }
    console.log('Zone Data:', zoneData); // Log the zoneData for debugging

    const { jsonData: zones } = zoneData;

    if (!zones || zones.length === 0) {
        return <div>No zone data available to display</div>;
    }

    // Transform data into the format CanvasJS expects
    const transformedData = zones.map((zoneData: any) => {
        const { timestamps, humidity, temperature, zone } = zoneData;

        if (!timestamps || !humidity || !temperature || timestamps.length !== humidity.length || timestamps.length !== temperature.length) {
            console.warn(`Invalid data found for zone: ${zone}`);
            return [];
        }

        return [
            {
                type: chartType,  // Dynamically change the chart type based on the state
                name: `${zone} - Humidity`,
                showInLegend: true,
                dataPoints: timestamps.map((timestamp: string, index: number) => {
                    const parsedDate = new Date(timestamp);
                    return {
                        x: parsedDate,
                        y: humidity[index],
                    };
                }),
            },
            {
                type: chartType,  // Dynamically change the chart type based on the state
                name: `${zone} - Temperature`,
                showInLegend: true,
                dataPoints: timestamps.map((timestamp: string, index: number) => {
                    const parsedDate = new Date(timestamp);
                    return {
                        x: parsedDate.getTime(),
                        y: temperature[index],
                    };
                }),
            },
        ];
    }).flat();

    console.log('Transformed Data:', transformedData);

    // Set chart options
    const options = {
        animationEnabled: true,
        animationDuration: 2000,
        exportFileName: "TimeSeries Chart",
        exportEnabled: true,
        zoomEnabled: true,
        title: {
            text: 'TimeSeries Chart',
        },
        axisX: {
            title: 'Date',
            valueFormatString: 'YYYY-MM-DD',
        },
        axisY: {
            title: 'Value',
        },
        data: transformedData,
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

export default ChartTimeSeries;
