import json
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import os
import sys
import warnings
from google.cloud import firestore
import pytz  # For timezone handling

# Suppress warnings from statsmodels
warnings.filterwarnings("ignore", category=UserWarning, module="statsmodels")
warnings.filterwarnings("ignore", category=FutureWarning, module="statsmodels")

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

# Define collection and zones
collection = 'kerabit'
zones = {
    'zone1': 'sensor_data_C631F5295273',
    'zone2': 'sensor_data_C4D912ED63C6',
    'zone3': 'sensor_data_C37E14567097'
}

# Gather data for each zone
all_data = []
for zone, sub_collection in zones.items():
    sub_collection_ref = db.collection(collection).document(zone).collection(sub_collection)
    docs = sub_collection_ref.stream()
    
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id
        doc_dict['zone'] = zone
        all_data.append(doc_dict)

# Exit if no data found
if not all_data:
    print(json.dumps({"error": "No data found in Firestore"}))
    exit()

# Convert data to pandas DataFrame
df = pd.DataFrame([{
    'id': entry['id'],
    'zone': entry['zone'],
    'humidity': float(entry['humidity']),
    'temperature': float(entry['temperature']),
    'timestamp': entry['timestamp']
} for entry in all_data])

# Preprocess Data
df['timestamp'] = pd.to_datetime(df['timestamp'])
df.sort_values('timestamp', inplace=True)

# Process dates string to separate start and end dates
start_date_str, end_date_str = dates.split(",")  # Split at the comma
start_date_str = start_date_str.strip()  # Remove any extra spaces
end_date_str = end_date_str.strip()  # Remove any extra spaces

# Convert the string dates into datetime objects
start_date = pd.to_datetime(start_date_str)
end_date = pd.to_datetime(end_date_str)

# Ensure that start_date and end_date are timezone-aware (UTC)
start_date = start_date.replace(tzinfo=pytz.UTC)
end_date = end_date.replace(tzinfo=pytz.UTC)

# Filter the data to only include rows within the date range
df = df[(df['timestamp'] >= start_date) & (df['timestamp'] <= end_date)]

# Ensure the data is properly indexed and has a frequency
df.set_index('timestamp', inplace=True)

# Handle duplicates: Aggregating by taking the mean for each timestamp
df = df.groupby([df.index, 'zone']).agg({
    'id': 'first',  # Use the first ID for each group
    'humidity': 'mean',  # Average the humidity for duplicates
    'temperature': 'mean'  # Average the temperature for duplicates
}).reset_index()

# Filter data to include only the selected zones
df = df[df['zone'].isin([zoneOne, zoneTwo])]

# Pivot to have separate columns for each zone's data
df_pivoted = df.pivot(index='timestamp', columns='zone', values=['humidity', 'temperature'])

# Define ARIMA Analysis Function
def perform_arima_analysis(data, variable, zone, forecast_steps=10):
    # Test for stationarity (Augmented Dickey-Fuller test)
    adf_test = adfuller(data.dropna())  # Drop NA values for stationarity test
    if adf_test[1] > 0.05:  # If data is non-stationary, difference the data
        data = data.diff().dropna()

    # Fit ARIMA model
    model = ARIMA(data, order=(1, 1, 1))  # Adjust (p, d, q) as needed
    model_fit = model.fit()

    # Forecast future values
    forecast = model_fit.forecast(steps=forecast_steps)
    forecast_index = pd.date_range(start=data.index[-1], periods=forecast_steps + 1, freq='D')[1:]

    return {
        "zone": zone,
        "forecast": list(zip(forecast_index.strftime('%Y-%m-%d').tolist(), forecast.tolist()))
    }

# Run ARIMA analysis for each selected zone on the chosen variable
arima_results = []
for zone in [zoneOne, zoneTwo]:
    if zone in zones:
        zone_data = df_pivoted[variableOne][zone].dropna()  # Select the chosen variable for ARIMA
        if len(zone_data) < 10:  # Ensure enough data points
            continue
        result = perform_arima_analysis(zone_data, variableOne, zone)
        arima_results.append(result)

# Combine ARIMA results with metadata
data = {
    "dates": dates,
    "zones": [zoneOne, zoneTwo],
    "variables": [variableOne, variableTwo],
    "analysisType": [analysisType],
    "jsonData": arima_results,
}

# Output ARIMA results as JSON
print(json.dumps(data, indent=4))
