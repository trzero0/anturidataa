from google.cloud import firestore

# Palvelutilin avaimen polku
service_account_key_path = 'prj-mtp-jaak-leht-ufl-a50dabd764ca.json'

# Yhdistetään Firestore-tietokantaan
db = firestore.Client.from_service_account_json(service_account_key_path, project='prj-mtp-jaak-leht-ufl')

# Kokoelma, joka sisältää zone-dokumentit
collection = 'kerabit'

# Haetaan kaikki zone-dokumentit
zones = db.collection(collection).stream()



for zone in zones:
    print(f"Haetaan dataa zonelle: {zone.id}")
    
    # Hakee kaikki sub-kokoelmat (sensorit) kyseisessä zonessa
    sensor_collections = db.collection(collection).document(zone.id).collections()
    
    # Käydään läpi kaikki sensoridatan alikokoelmat (esim. sensor_data_C631F5295273)
    for sensor_collection in sensor_collections:
        print(f"  Haetaan dataa sensorikokoelmasta: {sensor_collection.id}")
        
        # Haetaan enintään kolme dokumenttia sensorikokoelmasta
        sensor_docs = sensor_collection.stream()
        doc_count = 0  # Counter to track the number of documents fetched
        
        for doc in sensor_docs:
            print(f"    {doc.id} => {doc.to_dict()}")
            doc_count += 1
            if doc_count >= 3:
                break

# # Käydään läpi kaikki zone-dokumentit ja haetaan kunkin sensoridata
# for zone in zones:
#     print(f"Haetaan dataa zonelle: {zone.id}")
    
#     # Hakee kaikki sub-kokoelmat (sensorit) kyseisessä zonessa
#     sensor_collections = db.collection(collection).document(zone.id).collections()
    
#     # Käydään läpi kaikki sensoridatan alikokoelmat (esim. sensor_data_C631F5295273)
#     for sensor_collection in sensor_collections:
#         print(f"  Haetaan dataa sensorikokoelmasta: {sensor_collection.id}")
        
#         # Haetaan kaikki dokumentit sensorikokoelmasta
#         sensor_docs = sensor_collection.stream()
        
#         # Tulostetaan jokaisen sensoridatan dokumentti
#         for doc in sensor_docs:
#             print(f"    {doc.id} => {doc.to_dict()}")
