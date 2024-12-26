import json
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from google.cloud import firestore
import os
import sys
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings("ignore", category=UserWarning, module='statsmodels')
warnings.filterwarnings("ignore", category=FutureWarning, module='statsmodels')

# Convert sys.argv inputs to lowercase (except for script name at index 0)
args = [arg.lower() for arg in sys.argv]

# Read inputs
dates = args[1]  # Date range as string, e.g., "2023-01-01 to 2023-12-31"
zoneOne = args[2]  # Zone identifier, e.g., 'zone2'
zoneTwo = args[3]  # Zone identifier, e.g., 'zone3'
variableOne = args[4]  # Variable, e.g., 'humidity'
variableTwo = args[5]  # Variable, e.g., 'temperature'
analysisType = args[6]
jsonData = args[7]  # Optional input JSON data (if required)

# Translate Finnish variables to English
translations = {
    'kosteus': 'humidity',
    'lämpötila': 'temperature',
    'lampotila': 'temperature'  # Added to ensure case matching
}

variableOne = translations.get(variableOne, variableOne)  # Default to original if no translation
variableTwo = translations.get(variableTwo, variableTwo)  # Default to original if no translation

# Initialize Firestore
service_account_key_path = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
project_id = 'prj-mtp-jaak-leht-ufl'  # Google Cloud project ID
db = firestore.Client.from_service_account_json(service_account_key_path, project=project_id)

# Load viherkatto.json data
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path_sahko = os.path.join(script_dir, 'viherkatto.json')
with open(file_path_sahko, 'r') as file:
    json_data_sahko = json.load(file)

# Process viherkatto.json data into a DataFrame
df_json = pd.DataFrame(json_data_sahko)
df_json['Time'] = pd.to_datetime(df_json['Time'], format='%d/%b/%Y %H:%M')
df_json.set_index('Time', inplace=True)
df_json.replace("--", pd.NA, inplace=True)

# Convert columns to numeric and handle non-numeric gracefully
df_json['Inverter 4 12kW Viherkatto/Total DC Power(kW)'] = pd.to_numeric(
    df_json['Inverter 4 12kW Viherkatto/Total DC Power(kW)'], errors='coerce')
df_json['Inverter 4 12kW Viherkatto/Total Active Power(kW)'] = pd.to_numeric(
    df_json['Inverter 4 12kW Viherkatto/Total Active Power(kW)'], errors='coerce')

# Drop rows with any NaN values
df_json.dropna(inplace=True)

# Load Firestore data
collection = 'kerabit'
zones = {
    'zone1': 'sensor_data_C631F5295273',
    'zone2': 'sensor_data_C4D912ED63C6',
    'zone3': 'sensor_data_C37E14567097'
}

all_data = []
for zone, sub_collection in zones.items():
    sub_collection_ref = db.collection(collection).document(zone).collection(sub_collection)
    docs = sub_collection_ref.stream()
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id
        doc_dict['zone'] = zone
        all_data.append(doc_dict)

# If no data, exit
if not all_data:
    exit()

# Process Firestore data into a DataFrame
df_firestore = pd.DataFrame([{
    'id': entry['id'],
    'zone': entry['zone'],
    'humidity': float(entry.get('humidity', 0)),  # Default to 0 if not present
    'temperature': float(entry.get('temperature', 0)),  # Default to 0 if not present
    'timestamp': entry['timestamp']
} for entry in all_data])

# Preprocess Firestore data
df_firestore['timestamp'] = pd.to_datetime(df_firestore['timestamp'], errors='coerce')  # Convert to datetime
df_firestore.dropna(subset=['timestamp'], inplace=True)  # Drop rows with invalid timestamps
df_firestore.set_index('timestamp', inplace=True)

# Remove timezone info
df_firestore.index = df_firestore.index.tz_localize(None)
df_json.index = df_json.index.tz_localize(None)

# Sort and aggregate data
df_firestore.sort_index(inplace=True)
df_firestore = df_firestore.groupby([df_firestore.index]).agg({
    'id': 'first',
    'zone': 'first',
    'humidity': 'mean',
    'temperature': 'mean'
})
df_firestore = df_firestore.asfreq('D', method='pad')

# Combine viherkatto.json and Firestore data
df_combined = pd.concat([df_firestore, df_json], axis=1).sort_index()

# Handle date range parsing from sys.argv
if 'to' in dates:
    date_range = dates.split(" to ")
else:
    date_range = dates.split(",")

# Ensure there are exactly two date parts after split
if len(date_range) == 2:
    start_date = pd.to_datetime(date_range[0].strip())  # Parse start date
    end_date = pd.to_datetime(date_range[1].strip())    # Parse end date
else:
    raise ValueError("Invalid date range format. Please provide dates in 'YYYY-MM-DD to YYYY-MM-DD' format.")

# Filter data based on the date range
df_combined = df_combined[(df_combined.index >= start_date) & (df_combined.index <= end_date)]

# Filter data based on zoneOne and zoneTwo
df_combined = df_combined[df_combined['zone'].isin([zoneOne, zoneTwo])]

# Define ARIMA Analysis Function (this will work for both humidity and temperature separately)
def perform_arima_analysis(data, zone, variable, forecast_steps=10):
    # Test for stationarity (Augmented Dickey-Fuller test)
    adf_test = adfuller(data.dropna())
    if adf_test[1] > 0.05:  # If data is non-stationary, difference the data
        data = data.diff().dropna()

    # Fit ARIMA model
    model = ARIMA(data, order=(1, 1, 1))
    model_fit = model.fit()

    # Forecast future values
    forecast = model_fit.forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start=data.index[-1], periods=forecast_steps + 1, freq='D')[1:]

    return {
        "zone": zone,
        "variable": variable,
        "forecast": list(zip(forecast_index.strftime('%Y-%m-%d').tolist(), forecast.tolist()))
    }

# Run ARIMA analysis for selected zones (separate humidity and temperature for each zone)
arima_results = []

# Iterate over both zones
for zone in [zoneOne, zoneTwo]:
    # Initialize a dictionary to store combined results for the zone
    combined_forecast = {'zone': zone, 'forecast': []}

    # Initialize variables to store individual forecasts
    zone_temperature_forecast = []
    zone_humidity_forecast = []

    # Perform ARIMA analysis for both humidity and temperature separately
    for variable in ['humidity', 'temperature']:
        zone_data = df_combined[df_combined['zone'] == zone][variable]  # Select each variable
        if len(zone_data.dropna()) >= 10:  # Ensure sufficient data points
            # Perform ARIMA analysis for each variable separately
            result = perform_arima_analysis(zone_data, zone, variable)

            # Depending on the variable, store the forecast
            if variable == 'humidity':
                zone_humidity_forecast = result['forecast']  # Assuming result contains 'forecast' key
            elif variable == 'temperature':
                zone_temperature_forecast = result['forecast']  # Assuming result contains 'forecast' key

    # Combine temperature and humidity forecasts for the zone
    # Here, we assume that both forecasts are time-aligned and can be added together
    combined_forecast['forecast'] = [
        temp + hum for temp, hum in zip(zone_temperature_forecast, zone_humidity_forecast)
    ]

    # Append the combined result for the zone to the arima_results list
    arima_results.append(combined_forecast)


# Package the results with only forecast data
data = {
    "dates": dates,
    "zones": [zoneOne,zoneTwo],
    "variables": [variableOne, variableTwo],
    "analysisType":[analysisType],
    "jsonData": arima_results,
}


# Output ARIMA results as JSON
print(json.dumps(data, indent=4))