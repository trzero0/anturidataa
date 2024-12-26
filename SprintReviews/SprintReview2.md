## Sprint 2 Review

Sprintissä käyttety aika: 66 tuntia
Scrum master: Kaspar Tullus

Trello Board Kuva, Sprint 2. 
![image](https://github.com/user-attachments/assets/c2b596e2-13da-41ac-a4f7-a710ce17b364)

Toisen sprintin tavoitteena oli analysoida antureista saatua dataa ja aloittaa käyttöliittymän suunnittelu. Saatiin tehtyä yksinkertaista analyysiä, vaikkakin sähköntuotanto jäi vielä analysoimatta.

![image](Images/averages.png)
Kuvasta nähdään zonejen väliset keskiarvot lämpötilalle ja kosteudelle.

![image](Images/temp_curve.png)
![image](Images/hum_curve.png)
Kuvissa näkyvät lämpötilan ja kosteuden keski-arvot päivittäin

![Density Plot](https://github.com/user-attachments/assets/9440ac9a-f96b-45c9-8cb5-bb97341607e4)
![Density Plot temp](https://github.com/user-attachments/assets/8ab40016-cce4-4957-a425-a1f120ee19be)
Kuvissa näkyy lämpötilan ja kosteuden arvojen jakauma.

![image](Images/linear_reg.png)
![image](Images/dec_tree.png)

Edettiin soveltamaan dataan koneoppimismalleja. Linear regression -mallia sovellettiin kosteusarvojen ennustamiseen kohtalaisin tuloksin, mallin osoittaessa lievää korrelaatiota. Decision tree -mallia tutkittiin puolestaan zonejen ennustamiseen. Malli ei ollut tutkimusiimin mielestä hyödyllinen, sillä 60 % accuracy -arvolla virheellisesti luokiteltuja oli edelleen turhan paljon.

### Käyttöliittymän yhteys KNIME palvelimelle

[Anaconda-ecosysteemi](https://www.anaconda.com/) ladattiin, jotta KNIME-palvelinta voitiin testata käyttöliittymän kanssa. Se mahdollistaa erilaisten pakettien lataamisen KNIMEen, joita voi hyödyntää muunmuassa Python-koodinoodeissa.
KNIMEssä tiedot saatiin käyttöliittymään hakemalla dataa Google Cloud Firestoresta Python-noodia käyttäen. Python-noodissa data muunnettiin "Kino"-outputiksi, joka voitiin puolestaan lähettää analyysinoodeihin. Analyysinoodien käsittelyn jälkeen kaikki tulokset lähetettiin uudelle Python-noodille, joka lähetti POST-kutsulla tiedon ("Tulokset") Express-palvelimelle.
![image](https://github.com/user-attachments/assets/7dca5373-7e99-4408-94a6-8cdc337431c7)

Express-palvelin vastaanotti kutsun, myöhemmässä versiossa koitetaan purkaa tieto kutsusta ja tulostaa se käyttöliitymään. Tässä versiossa testattiin vain, että kutsu saapui perille Knimen sisältä "LocalHost"-palvelimelle.

Tiimi tutki, paljonko KNIME-palvelimen ylläpito maksaisi. Tultiin päätelmään, että jos ohjelmaa tarvitaan suurelle määrälle käyttäjiä, 35000 euroa/vuosi maksava "Knime Business Hub" -paketti olisi kannattavin. Mikäli käyttäjiä on vähän, 100 euroa kuukaudessa maksava "Team-plan" olisi sopivampi. Analyysin käynnistäminen "Team-plan" -sopimuksella maksaisi 0.10 euroa/minuutti, ja Workflow pyörii hitaammin, mitä enemmän dataa se hakee. Datan ollessa paljon, workflown hinta voi olla mittava.
![image](https://github.com/user-attachments/assets/cb3c9b25-7e39-49c4-b030-08c9b80aee4c)

Knimen suunnitelmien hinnat näkyvät sivustolla: https://www.knime.com/knime-hub-pricing

### Käyttöliittymän suunnittelu

Kolmannessa sprintissä valittiin käyttöliittymän ohjelmointikielet ja hahmoteltiin käyttöliittymän toiminnallisuuksia, jotta seuraavassa sprintissä käyttöliittymän rakentaminen voidaan aloittaa.

![sekvenssikaavio](https://github.com/user-attachments/assets/a9c0e12d-5498-4e01-aaa3-ba6def6d308d)
[Kaavio Google Drivessä](https://drive.google.com/file/d/1e3WuuvXdpVepUh0KZqurkI0zXcseGpl1/view?usp=sharing)

Kuvassa on esitetty sekvenssikaavio.

Sekvenssikaaviosta nähdään tyypillisiä käyttötapauksia:

- Sivu avautuu valikkoon, josta valitaan kuvaajalle visalisoitava data.
- Kuvaajasivulla datan ja kuvaajan tyypin voi vaihtaa.
- Nuolilla voi siirtää kuvaajan ajanjaksoa.
- Kuvaajan datan voi hakea uudelleen.

Perustoiminnallisuuksia on myös hahmoteltu [Figmassa](https://www.figma.com/design/ErpZ9BRxzQFRhu7QXLLNyz/InnovaatioProju?node-id=0-1&t=mHdW0f2nfrnkuPJs-1).
Lisäksi on alustavasti mietitty lisätoiminnallisuuksia, kuten tulosten tallentaminen (PDF/CSV-muotoon) ja interaktiivinen datan tutkinta.

### Analyysi Pythonilla

Tavoitteena tarkistaa tuleeko samat tulokset Pythonilla
![python](https://github.com/user-attachments/assets/1be370b4-49f7-46cf-b5ec-dbd79037e440)
Kaikki kaaviot sisältävät reaaliaikaisesti zone 1, 2 ja 3.

Kuvissa näkyy:

- **Kosteuden ja lämpötilan hajontakaavio**
- **Kosteuden ja lämpötilan histogrammi**
- **Klusterointikaavio**
- **Lineaarinen regressio: Kosteus vs Lämpötila**  
  Regressiosuoran R²-arvo: `0.67`, kun Knimellä saavutettiin `0.7`.

Käytettiin seuraavia Python-kirjastoja:

- **pandas**: Datan käsittelyyn ja esikäsittelyyn
- **numpy**: Matemaattisiin laskutoimituksiin
- **matplotlib** ja **seaborn**: Visualisointien, kuten hajontakaavioiden ja histogrammien, piirtämiseen
- **sklearn (scikit-learn)**: Klusterointiin ja lineaariseen regressioon
  - **KMeans**: Klusterointiin
  - **LinearRegression**: Lineaariseen regressioon

Tulokset olivat lähellä KNIME:llä saatuja, mutta eroavaisuudet olivat helposti havaittavissa. Esimerkiksi pisteet eivät olleet täysin samoilla kohdilla.

## [Seuraava Sprint](SprintReview3.md)
## [Sprintit](SprintList.md)
