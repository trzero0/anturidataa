import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
from sklearn.cross_decomposition import PLSRegression
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
from google.cloud import firestore
import numpy as np
import json
import os

# Firestore alustaminen
service_account_key_path = 'C:\\Users\\melih\\Desktop\\anturiprojekti\\prj-mtp-jaak-leht-ufl-a50dabd764ca.json'
project_id = 'prj-mtp-jaak-leht-ufl'  # Google Cloud
db = firestore.Client.from_service_account_json(service_account_key_path, project=project_id)

# Zonien määrittely
collection = 'kerabit'
zones = {
    'zone1': 'sensor_data_C631F5295273',
    'zone2': 'sensor_data_C4D912ED63C6',
    'zone3': 'sensor_data_C37E14567097'
}

# Muuttuja yhdistämään kaikki zonien data yhdeksi DataFrameksi
all_data = []

# Haetaan data Firestoresta jokaiselle zonelle
for zone, sub_collection in zones.items():
    sub_collection_ref = db.collection(collection).document(zone).collection(sub_collection)
    docs = sub_collection_ref.stream()
    
    for doc in docs:
        doc_dict = doc.to_dict()
        doc_dict['id'] = doc.id
        doc_dict['zone'] = zone
        all_data.append(doc_dict)

# Tarkistetaan, että dataa löytyi
if not all_data:
    print("Ei dataa löytynyt Firestoresta.")
    exit()

# Muutetaan data pandas DataFrameksi
df = pd.DataFrame([{
    'id': entry['id'],
    'zone': entry['zone'],
    'humidity': float(entry['humidity']),
    'temperature': float(entry['temperature']),
    'timestamp': entry['timestamp']
} for entry in all_data])

# Muutetaan timestamp datetime-muotoon
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Järjestetään DataFrame aikalehden mukaan
df.sort_values('timestamp', inplace=True)

# Asetetaan timestamp indeksiksi
df.set_index('timestamp', inplace=True)

# Normalisoidaan data
scaler = StandardScaler()
X = df[['humidity', 'temperature']]
X_scaled = scaler.fit_transform(X)

# K-Means-klusterointi
kmeans = KMeans(n_clusters=3, random_state=0)
df['cluster'] = kmeans.fit_predict(X_scaled)

# PCA-analyysi
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df['pca_comp1'] = X_pca[:, 0]
df['pca_comp2'] = X_pca[:, 1]

# PLS-analyysi
pls = PLSRegression(n_components=2)
X_pls = df[['humidity', 'temperature']]
Y_pls = df[['humidity']]  # Placeholder, voisi käyttää toista muuttujaa
pls.fit(X_pls, Y_pls)
df['pls_comp1'] = pls.x_scores_[:, 0]
df['pls_comp2'] = pls.x_scores_[:, 1]

# Lineaarinen regressio
X_reg = df[['humidity']]
y_reg = df['temperature']
reg_model = LinearRegression()
reg_model.fit(X_reg, y_reg)
y_pred = reg_model.predict(X_reg)
r_squared = reg_model.score(X_reg, y_reg)

# ARIMA-malli jokaiselle zonelle
arima_results = {}
for zone in zones.keys():
    example_data = df[df['zone'] == zone]['temperature']
    if adfuller(example_data)[1] > 0.05:
        example_data_diff = example_data.diff().dropna()
    else:
        example_data_diff = example_data
    model = ARIMA(example_data_diff, order=(1, 1, 1))
    model_fit = model.fit()
    forecast = model_fit.forecast(steps=5)
    arima_results[zone] = {
        'forecast': forecast.tolist(),
        'aic': model_fit.aic,
        'bic': model_fit.bic
    }

# Kuukausittainen sähkötuotanto
json_files = {
    'flex': 'flex.json',
    'flat': 'flat.json',
    'viherkatto': 'viherkatto.json',
    'seina': 'seina.json'
}

column_mappings = {
    'flex': {"Inverter 2 50kW Flex/Total Active Power(kW)": "Active Power (kW)"},
    'flat': {"Inverter 3 50kW Flatfix/Total Active Power(kW)": "Active Power (kW)"},
    'viherkatto': {"Inverter 4 12kW Viherkatto/Total Active Power(kW)": "Active Power (kW)"},
    'seina': {"Inverter 15kW Seinä/Total Active Power(kW)": "Active Power (kW)"}
}

def load_and_process_json(file_path, column_mapping):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df['Time'] = pd.to_datetime(df['Time'], format="%d/%b/%Y %H:%M")
    df.rename(columns=column_mapping, inplace=True)
    return df

dataframes = []

for source, file_path in json_files.items():
    if os.path.exists(file_path):
        df_energy = load_and_process_json(file_path, column_mappings[source])
        df_energy['Source'] = source
        dataframes.append(df_energy)
    else:
        print(f"Tiedostoa {file_path} ei löytynyt.")

all_energy_data = pd.concat(dataframes, ignore_index=True)
all_energy_data['Active Power (kW)'] = pd.to_numeric(all_energy_data['Active Power (kW)'], errors='coerce')
all_energy_data['Month'] = all_energy_data['Time'].dt.to_period('M')
monthly_production = all_energy_data.groupby('Month')['Active Power (kW)'].sum()

# Kaikki analyysit JSON-muodossa
results = {
    'kmeans': {
        'clusters': df['cluster'].value_counts().to_dict(),
    },
    'pca': {
        'explained_variance': pca.explained_variance_ratio_.tolist(),
        'components': X_pca.tolist()
    },
    'pls': {
        'x_scores': pls.x_scores_.tolist(),
        'y_scores': pls.y_scores_.tolist()
    },
    'regression': {
        'r_squared': r_squared,
        'slope': reg_model.coef_[0],
        'intercept': reg_model.intercept_
    },
    'arima': arima_results,
    'monthly_production': monthly_production.to_dict()
}

# Muunna kaikki avaimet string-muotoon JSON-tallennusta varten
def convert_keys_to_strings(d):
    if isinstance(d, dict):
        return {str(k): convert_keys_to_strings(v) for k, v in d.items()}
    elif isinstance(d, list):
        return [convert_keys_to_strings(i) for i in d]
    else:
        return d

results_json_ready = convert_keys_to_strings(results)

# Tallennetaan tulokset tiedostoon
output_path = 'Tulokset.json'
with open(output_path, 'w') as f:
    json.dump(results_json_ready, f, indent=4)
