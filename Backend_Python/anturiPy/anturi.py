import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from google.cloud import firestore
from sklearn.cross_decomposition import PLSRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, mean_absolute_error
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller
import numpy as np

# Firestore alustaminen
service_account_key_path = 'C:\\Users\\melih\\Desktop\\anturiprojekti\\prj-mtp-jaak-leht-ufl-a50dabd764ca.json'
project_id = 'prj-mtp-jaak-leht-ufl'  # Google Cloud
db = firestore.Client.from_service_account_json(service_account_key_path, project=project_id)

# zonien määrittely
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

# Muutetaan timestamp datetime muotoon
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Järjestetään DataFrame aikalehden mukaan
df.sort_values('timestamp', inplace=True)

# Asetetaan timestamp indeksiksi
df.set_index('timestamp', inplace=True)

# Tarkistetaan, että data on oikein
print(df.head())
# Aikasarjan visualisointi kosteudesta ja lämpötilasta
plt.figure(figsize=(14, 6))
for zone in zones.keys():
    subset = df[df['zone'] == zone]
    plt.plot(subset.index, subset['humidity'], label=f'Kosteus {zone}')
    plt.plot(subset.index, subset['temperature'], label=f'Lämpötila {zone}')

plt.title('Kosteuden ja lämpötilan aikasarja-analyysi')
plt.xlabel('Aika')
plt.ylabel('Arvo')
plt.legend()
plt.show()
# Määritetään värit zoneille
# voi muuttaa värejä tästä halutessaan
zone_colors = {
    'zone1': 'blue',
    'zone2': 'green',
    'zone3': 'orange'
}

# Valmistellaan data klusterointia varten (käytetään kosteutta ja lämpötilaa)
X = df[['humidity', 'temperature']]

# Normalisoidaan data
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# K-Means-klusterointi (3 klusteria)
kmeans = KMeans(n_clusters=3, random_state=0)
df['cluster'] = kmeans.fit_predict(X_scaled)

# Klusterien selittävät nimet
cluster_labels = {
    0: 'Klusteri 1 (Matala kosteus, Korkea lämpötila)',
    1: 'Klusteri 2 (Keskikosteus, Keskilämpötila)',
    2: 'Klusteri 3 (Korkea kosteus, Matala lämpötila)'
}

# Korvataan numeeriset klusterit selittävillä nimillä
df['cluster_label'] = df['cluster'].map(cluster_labels)

# PCA (Principal Component Analysis) analyysi
pca = PCA(n_components=2)  # 2 pääkomponenttia
X_pca = pca.fit_transform(X_scaled)

# Lisätään PCA-komponentit DataFrameen
df['pca_comp1'] = X_pca[:, 0]
df['pca_comp2'] = X_pca[:, 1]

# Plotataan PCA-komponentit
plt.figure(figsize=(10, 6))
for zone, color in zone_colors.items():
    subset = df[df['zone'] == zone]
    plt.scatter(subset['pca_comp1'], subset['pca_comp2'], color=color, label=zone)

plt.title('PCA-komponentit (Principal Component Analysis)')
plt.xlabel('PCA-komponentti 1')
plt.ylabel('PCA-komponentti 2')
plt.legend(title='Zone')
plt.show()
# Lineaarinen regressiomalli (kosteus vs lämpötila)
X_reg = df[['humidity']]
y_reg = df['temperature']
reg_model = LinearRegression()
reg_model.fit(X_reg, y_reg)

# Ennusteet ja regressiotilastot
y_pred = reg_model.predict(X_reg)
r_squared = reg_model.score(X_reg, y_reg)
slope = reg_model.coef_[0]
intercept = reg_model.intercept_
# PLSRegression käytetään samaan tarkoitukseen (Multiblock Component Analysis)
pls = PLSRegression(n_components=2)
X_pls = df[['humidity', 'temperature']]
Y_pls = df[['humidity']]  # Placeholder, multiblock-malli tarvitsee yleensä useita riippuvia muuttujia
pls.fit(X_pls, Y_pls)

# Tulostetaan PLS-komponentit
df['pls_comp1'] = pls.x_scores_[:, 0]
df['pls_comp2'] = pls.x_scores_[:, 1]

# Plotataan PLS-komponentit
plt.figure(figsize=(10, 6))
for zone, color in zone_colors.items():
    subset = df[df['zone'] == zone]
    plt.scatter(subset['pls_comp1'], subset['pls_comp2'], color=color, label=zone)

plt.title('PLS-komponentit (Multiblock Component Analysis)')
plt.xlabel('PLS-komponentti 1')
plt.ylabel('PLS-komponentti 2')
plt.legend(title='Zone')
plt.show()
# Piirretään muut analyysit
fig, axs = plt.subplots(2, 2, figsize=(14, 14))  # Changed to 2x2 layout

# Kosteus vs Lämpötila hajontakaavio (K-Means-klusterit)
for zone, color in zone_colors.items():
    subset = df[df['zone'] == zone]
    axs[0, 0].scatter(subset['humidity'], subset['temperature'], c=color, label=zone)

axs[0, 0].set_xlabel('Kosteus')
axs[0, 0].set_ylabel('Lämpötila')
axs[0, 0].set_title('Kosteuden ja lämpötilan hajontakaavio (Zonet)')
axs[0, 0].legend(title='Zone')

# Histogrammi kosteudesta ja lämpötilasta zonittain
for zone, color in zone_colors.items():
    subset = df[df['zone'] == zone]
    axs[0, 1].hist(subset['humidity'], bins=20, alpha=0.5, label=f'Kosteus ({zone})', color=color)
    axs[0, 1].hist(subset['temperature'], bins=20, alpha=0.5, label=f'Lämpötila ({zone})', color=color, histtype='step')

axs[0, 1].set_xlabel('Arvo')
axs[0, 1].set_ylabel('Frekvenssi')
axs[0, 1].set_title('Kosteuden ja lämpötilan histogrammi (Zonet)')
axs[0, 1].legend()

# Klusterien jakauma (piakkakaavio)
cluster_counts = df['cluster_label'].value_counts()
axs[1, 0].pie(cluster_counts, labels=cluster_counts.index, autopct='%1.1f%%', colors=plt.get_cmap('viridis')(range(len(cluster_counts))))
axs[1, 0].set_title('Klusterien jakauma')

# Lineaarinen regressio: Kosteus vs Lämpötila
axs[1, 1].scatter(X_reg, y_reg, color='blue', label='Data')
axs[1, 1].plot(X_reg, y_pred, color='red', label='Regressiolinja')
axs[1, 1].set_title(f'Lineaarinen regressio (R²={r_squared:.2f})')
axs[1, 1].set_xlabel('Kosteus')
axs[1, 1].set_ylabel('Lämpötila')
axs[1, 1].legend()
plt.grid()
plt.tight_layout()  # Adjust layout to prevent overlap
plt.show()

# ARIMA-mallin sovittaminen
# Testataan stationaarisuutta
def test_stationarity(timeseries):
    result = adfuller(timeseries)
    print('ADF Statistic:', result[0])
    print('p-value:', result[1])

# Esimerkkiaikasarja (voit valita haluamasi zone)
example_zone = 'zone1'
example_data = df[df['zone'] == example_zone]['humidity']

# Testataan stationaarisuutta
test_stationarity(example_data)

# Jos data ei ole stationaarinen, otetaan ensimmäinen differenssi
if adfuller(example_data)[1] > 0.05:
    example_data_diff = example_data.diff().dropna()
else:
    example_data_diff = example_data

# ARIMA-mallin sovittaminen jokaiselle zonelle
arima_results = {}

plt.figure(figsize=(14, 8))

for zone in zones.keys():
    # Valitaan esimerkkiaikasarja
    example_data = df[df['zone'] == zone]['temperature']  # Voit muuttaa 'temperature' -> 'humidity' tarpeen mukaan

    # Testataan stationaarisuutta
    adf_test = adfuller(example_data)
    print(f'Testataan stationaarisuutta zonessa: {zone}')
    print('ADF Statistic:', adf_test[0])
    print('p-value:', adf_test[1])

    # Jos data ei ole stationaarinen, otetaan ensimmäinen differenssi
    if adf_test[1] > 0.05:
        example_data_diff = example_data.diff().dropna()
    else:
        example_data_diff = example_data

    # ARIMA-mallin sovittaminen
    model = ARIMA(example_data_diff, order=(1, 1, 1))  # (p, d, q)
    model_fit = model.fit()

    # Ennusteet
    forecast_steps = 5  # Ennustettavien aikapisteiden määrä
    forecast = model_fit.forecast(steps=forecast_steps)

    # Visualisoidaan ennusteet samassa ikkunassa
    plt.plot(example_data.index, example_data, label=f'Todellinen data ({zone})')
    forecast_index = pd.date_range(start=example_data.index[-1], periods=forecast_steps + 1, freq='D')[1:]
    plt.plot(forecast_index, forecast, label=f'Ennuste ({zone})', linestyle='--')

# Yhteenveto grafiikasta
plt.title('ARIMA-ennusteet kaikille zonille')
plt.xlabel('Aika')
plt.ylabel('Lämpötila')  # Muuta 'Lämpötila' 'Kosteus' mukaan
plt.legend()
plt.grid()
plt.show()