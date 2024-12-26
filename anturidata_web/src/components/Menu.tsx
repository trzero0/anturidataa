import React, {useState, useEffect} from "react";
import Select, {SingleValue} from "react-select";
import MultiDatePicker, {DateObject} from "react-multi-date-picker";
import "react-multi-date-picker/styles/colors/teal.css";
import axios from "axios";
//import ArimaChart from "./ArimaChart.tsx";
import TimeSeriesChart from "./TimeSeriesChart.tsx";
import ArimaChart from "./ArimaChart.tsx";

const fetchSessionId = async () => {
    try {
        const response = await axios.get("http://localhost:3001/track-session", {
            withCredentials: true,
        });
        return (response.data as { sessionId: string }).sessionId; // Ensure the backend returns sessionId
    } catch (error) {
        console.error("Error fetching session ID:", error);
        return null;
    }
};

const fetchResultsBySession = async (sessionId: string) => {
    try {
        const response = await axios.get(`http://localhost:3001/results?sessionId=${sessionId}`, {
            withCredentials: true,
        });
        return response.data; // Return session-specific results
    } catch (error) {
        console.error("Error fetching results:", error);
        return [];
    }
};

const options = [
    {value: "Zone1", label: "Zone1", type: "zone"},
    {value: "Zone2", label: "Zone2", type: "zone"},
    {value: "Zone3", label: "Zone3", type: "zone"},
    {value: "Kosteus", label: "Kosteus", type: "variable"},
    {value: "Lampotila", label: "Lämpötila", type: "variable"},
    {value: "ARIMA", label: "ARIMA", type: "analysis"},
    {value: "TimeSeries", label: "TimeSeries", type: "analysis"}
];

interface SelectedOptions {
    zoneOne: SingleValue<{ value: string; label: string; type: string }> | null;
    variableOne: SingleValue<{ value: string; label: string; type: string }> | null;
    zoneTwo: SingleValue<{ value: string; label: string; type: string }> | null;
    variableTwo: SingleValue<{ value: string; label: string; type: string }> | null;
    analysisType: SingleValue<{ value: string; label: string; type: string }> | null;
}

const Menu = () => {
    const [jsonData, setJsonData] = useState<any>(null);
    const [dates, setDates] = useState<DateObject[]>([]);
    const [selectedOptions, setSelectedOptions] = useState<SelectedOptions>({
        zoneOne: null,
        variableOne: null,
        zoneTwo: null,
        variableTwo: null,
        analysisType: null,
    });
    const [data, setData] = useState<any>(null);
    const [dateError, setDateError] = useState<string | null>(null);
    const [dataToSend, setDataToSend] = useState<any>(null);
    const [isLoading, setIsLoading] = useState(false); // Track loading state

    const [sessionId, setSessionId] = useState<string | null>(null);
    const [sessionData, setSessionData] = useState<any[]>([]);
    const [selectedData, setSelectedData] = useState<any>(null);

    useEffect(() => {
        const initializeSession = async () => {
            const id = await fetchSessionId();
            setSessionId(id);

            if (id) {
                const results = await fetchResultsBySession(id);
                setSessionData(results);
            }
        };

        initializeSession();
    }, []);

    const handleDataSelection = (item: any) => {
		console.log("Selected Data:", item);
        setSelectedData(item);
    };

    // Update `dataToSend` dynamically when dependencies change
    useEffect(() => {
        if (!dateError && dates.length >= 2 && selectedOptions.zoneOne && selectedOptions.variableOne && selectedOptions.analysisType) {
            setDataToSend({
                dates: dates.map((d) => d.format("YYYY-MM-DD")),
                zoneOne: selectedOptions.zoneOne?.value,
                zoneTwo: selectedOptions.zoneTwo?.value,
                variableOne: selectedOptions.variableOne?.value,
                variableTwo: selectedOptions.variableTwo?.value,
                analysisType: selectedOptions.analysisType?.value,
                jsonData: jsonData || [],
            });
        } else {
            setDataToSend(null); // Clear when inputs are invalid
        }
    }, [dates, selectedOptions, jsonData, dateError]);
    useEffect(() => {
        if (data) {
            setSelectedData(data);  // Set selectedData to data whenever data changes
        }
    }, [data]);
    // Handle POST request
    const sendPostRequest = async () => {
        if (!dataToSend) return;
        setIsLoading(true);
        setData(null); // Clear previous data
        try {
            const response = await axios.post("http://localhost:3001/results", dataToSend, {
                withCredentials: true,
            });
            setData(response.data);
            console.log("Fetched Data:", response.data);
        } catch (error) {
            console.error("Error sending POST request:", error);
        } finally {
            setIsLoading(false);
        }
    };

    const handleDateChange = (date: DateObject[]) => {
        setDates(date);

        if (date.length >= 2) {
            const firstDate = date[0].toDate(); // Convert to JS Date
            const secondDate = date[1].toDate(); // Convert to JS Date

            if (firstDate >= secondDate) {
                setDateError("Date 1 must be before Date 2.");
            } else setDateError(null);
        } else setDateError(null);
    };

    const handleSelectChange = (
        selected: SingleValue<{ value: string; label: string; type: string }> | null,
        name: keyof SelectedOptions
    ) => {
        setSelectedOptions((prev) => {
            const updated = {...prev, [name]: selected};

            if (name === "zoneTwo" && selected?.value === prev.zoneOne?.value) {
                return {...updated, zoneTwo: null};
            }
            return updated;
        });
    };

    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const file = event.target.files?.[0];
        if (file) {
            const reader = new FileReader();
            reader.onload = (e) => {
                try {
                    const json = JSON.parse(e.target?.result as string);
                    setJsonData(json);
                    console.log("Uploaded JSON Data:", json);
                } catch (error) {
                    console.error("Error parsing JSON:", error);
                }
            };
            reader.readAsText(file);
        }
    };

    const zoneTwoOptions = options.filter(
        (opt) => opt.type === "zone" && opt.value !== selectedOptions.zoneOne?.value
    );

    // Filter session data to only include results for the current sessionId
    const filteredSessionData = sessionData.filter((item) => item.sessionId === sessionId);

    return (
        <div className="container">
            <div className="sidebar">
                <div className="headerpanel">
                    <h1>Anturidata</h1>
                </div>
                <br/>
                <div className="json-upload">
                    <label htmlFor="json-upload" className="json-label">
                        <h3>Käytä JSON tiedostoa:</h3>
                    </label>
                    <input type="file" id="json-upload" accept=".json" onChange={handleFileUpload}/>
                </div>
                <br/>
                <h3>Hae dataa aikaväliltä:</h3>
                <MultiDatePicker value={dates} onChange={handleDateChange} range/>
                {dateError && <p className="error-message">{dateError}</p>}
                <br/>
                <br/>
                <h3>Valitse alueet ja muuttujat</h3>
                <div className="field">
                    <p>Ensimmäinen vertailtava alue:</p>
                    <Select
                        options={options.filter((opt) => opt.type === "zone")}
                        value={selectedOptions.zoneOne}
                        onChange={(selected) => handleSelectChange(selected, "zoneOne")}
                        placeholder="Valitse alue"
                    />
                </div>
                <div className="field">
                    <p>Toinen vertailtava alue:</p>
                    <Select
                        options={zoneTwoOptions}
                        value={selectedOptions.zoneTwo}
                        onChange={(selected) => handleSelectChange(selected, "zoneTwo")}
                        placeholder="Valitse alue"
                    />
                </div>
                <div className="field">
                    <p>Ensimmäinen vertailtava muuttuja:</p>
                    <Select
                        options={options.filter((opt) => opt.type === "variable")}
                        value={selectedOptions.variableOne}
                        onChange={(selected) => handleSelectChange(selected, "variableOne")}
                        placeholder="Valitse muuttuja"
                    />
                </div>
                <div className="field">
                    <p>Toinen vertailtava muuttuja:</p>
                    <Select
                        options={options.filter((opt) => opt.type === "variable")}
                        value={selectedOptions.variableTwo}
                        onChange={(selected) => handleSelectChange(selected, "variableTwo")}
                        placeholder="Valitse muuttuja"
                    />
                </div>
                <h3>Valitse Analyysin tyypi</h3>
                <div className="field">
                    <p>Tyypi:</p>
                    <Select
                        options={options.filter((opt) => opt.type === "analysis")}
                        value={selectedOptions.analysisType}
                        onChange={(selected) => handleSelectChange(selected, "analysisType")}
                        placeholder="Valitse alue"
                    />
                </div>
                <br/>
                <button className="submit-button" onClick={sendPostRequest} disabled={!dataToSend || isLoading}>
                    {isLoading ? "Lähetetään..." : "Lähetä valinnat"}
                </button>
            </div>
            <div className="content">
                <h3>Kuvaajanäkymä</h3>
                {/* Scrollable container for buttons */}
                <div className="historyData" style={{maxHeight: "300px", overflowY: "scroll"}}>
                    {filteredSessionData.map((item, index) => (
                        <button
                            key={index}
                            className="historyDataButton"
                            onClick={() => handleDataSelection(item)}
                        >
                            Data {index + 1} {/* Use item-specific info if available */}
                        </button>
                    ))}
                </div>
                {(selectedData || data) ? (
                    ((selectedData?.data?.[0]?.analysisType?.[0] || data?.data?.[0]?.analysisType?.[0]) === "arima") ? (
                        <ArimaChart
                            jsonData={{
                                data: {
                                    jsonData: selectedData ? [selectedData] : [data], // Use selectedData if available; fallback to data
                                },
                            }}
                        />
                    ) : (
                        <TimeSeriesChart
                            jsonData={{
                                data: {
                                    jsonData: selectedData ? [selectedData] : [data], // Same logic here
                                },
                            }}
                        />
                    )
                ) : (
                    <div>No data available to display</div>
                )}


                <p>Kuvaajasi tulee näkyviin tähän</p>
            </div>
        </div>
    );
};

export default Menu;
