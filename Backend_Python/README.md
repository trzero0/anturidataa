# AnturiData Innovaatio Projekti

Jäsenet: Julia Köykkä, Atte Räisänen, Mikko Tanhola, Kaspar Tullus, Muhammed Özturk

# Kuvaus

Projektin tavoitteena on tutkia aurinkopaneelien eroja analysoimalla antureiden dataa KNIME-ohjelmistolla ja Python-ohjelmoinnilla. Lisäksi toteutetaan React-käyttöliittymä, jonka API yhdistyy Expressin avulla KNIME-palvelimeen. Käyttöliittymän avulla asiakas voi tarkastella dataa, esimerkiksi vertailemalla eri alueiden aurinkopaneelien kosteuden ja lämpötilan tasoja. Projektin aikataulutuksessa noudatetaan Agile-menetelmää ja hyödynnetään Trelloa.


# AnturiPy

### Ohje koodin käynnistämiseen
Lataa ensin AnturiPy tiedosto koneeseesi
## 1. Asennettavat kirjastot

Asenna seuraavat Python-kirjastot:

```bash
pip install pandas scikit-learn matplotlib google-cloud-firestore statsmodels numpy
```


## 2. Firestore-tunnukset

Koodissa käytetään Google Cloud Firestore -palvelua, joten sinun on määritettävä palvelutiliavain.

### Vaiheet:
1. Mene [Google Cloud Consoleen](https://console.cloud.google.com/).
2. Hae projekti ja siirry Firestore-osioon.
3. Lataa palvelutiliavain (JSON-muodossa).
4. Määritä `service_account_key_path`-muuttujaan polku ladattuun avaimeseen koodissasi:

```python
service_account_key_path = 'polku/tunnukseen.json'
```
## 3. Koodin käynnistäminen

Ennen koodin ajamista, on suositeltavaa luoda virtuaaliympäristö Pythonille. Tämä pitää projektin riippuvuudet erillään muista projekteista.

Luo ja aktivoi virtuaaliympäristö seuraavasti:

```bash
python -m venv venv
```
### Vaihe 4: Koodin suorittaminen

Kun kaikki riippuvuudet on asennettu ja Firestore-tunnus määritetty, voit suorittaa koodin seuraavalla komennolla:

1. Varmista, että olet virtuaaliympäristössä (jos käytät sellaista).
   
2. Suorita koodi komennolla:

   ```bash
   python analysis.py

## 5. Tulosten tarkastelu

Koodin suorituksen jälkeen voit tarkastella seuraavia tuloksia:

### Analyysit
- **Aikasarja-analyysi**: Kosteuden ja lämpötilan muutokset eri zoneissa ajan kuluessa.
- **PCA (Principal Component Analysis)**: Tulos, joka auttaa visualisoimaan dataa vähäisemmillä ulottuvuuksilla.
- **K-Means-klusterointi**: Klusterointi, joka ryhmittelee dataa perustuen kosteuden ja lämpötilan samankaltaisuuksiin.
- **Lineaarinen regressio**: Ennusteet ja malli kosteuden ja lämpötilan suhteelle.
- **PLS (Partial Least Squares)**: Multiblock-malli, joka analysoi useampia muuttujia samanaikaisesti.
- **ARIMA-malli**: Aikasarjan ennusteet, jotka perustuvat stationaarisiin aikasarjoihin. Malli testaa, onko data stationaarista ja luo ennusteita tuleville aikapisteille.
- **Hajontakaaviot ja histogrammit**: Visualisointeja, jotka auttavat ymmärtämään datan jakaumaa ja suhteita.

Voit tarkastella kaikki nämä tulokset suoraan koodin suorittamisen jälkeen näyttöön tulevissa graafeissa ja tulosteissa.




### [Sprintit](SprintReviews/SprintList.md)

### [Työajanseuranta](https://metropoliafi-my.sharepoint.com/:x:/g/personal/kaspart_metropolia_fi/EaOvk-hq3rlDtGvIea-mcjcByCtmNadYHdLlSF8qI84Jog?rtime=m9gjtOXa3Eg)
