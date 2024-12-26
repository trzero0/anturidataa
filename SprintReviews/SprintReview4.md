## Sprint 4 Review

Sprintissä käytetty aika: 76 tuntia
Scrum master: Mikko Tanhola

Neljännessä sprintissä oli tavoitteena tehdä lisää analyysiä käyttämällä Time-Series analysis ,Predictive Modeling analysis, Statistical Hypothesis Testing analysis.

#### Time-Series 

Time-series analyysin KNIME nodet
![image](https://github.com/user-attachments/assets/46d5fcea-8623-4ba7-8346-50c9e6d64e20)

Analyysissä tarkistettiin Zone 1 ja Zone 3 ennusteita käyttämällä Multivariate Time-Series Forecasting modelis ja Time-Series ARIMA modelia.

##### Multivariate Time-Series Forecasting tulos

Tuloksista käy ilmi, että kosteustasojen ja lämpötilojen vaikutus viherkatossa ei ole niin suurta kuin normaali katossa, jossa kosteus vaikuttaa sähköntuottoon päivittäin enemmän.
Korkeilla lämpötiloilla kosteus on alhaisempaa. Tämän analyysin perusteella viherkatto tuottaa parempia tuloksia sähköntuotossa, mutta tätä ei voida vielä varmistaa, sillä on olemassa monia muita tekijöitä, joita ei ole otettu tai joita ei ole voitu ottaa huomioon tässä analyysissä.
![image](https://github.com/user-attachments/assets/4258dfc5-ca82-4a8a-81b4-fde39ea6ebe3)

#### Autoregressive Models (ARIMA) Time-series

Viherkatto ennustus
![image2](https://github.com/user-attachments/assets/4b9d30f5-f07b-441e-a884-a74b8bc2ad56)

Viherkaton ennustuksesta nähdään, että viherkaton datan 'log-likelihood' on korkea, mikä tarkoittaa, että data soveltuu hyvin ARIMA-analyysiin. Analyysistä käy ilmi, että on melko suuri todennäköisyys sähköntuotannon nousulle seuraavina päivinä elokuussa.
Jos tarkastellaan tulevaisuutta ja olosuhteet heinä- ja elokuussa ovat lähes samat, sähkön tuotanto voi olla suurempaa kuin tänä vuonna.

Normaalikatto ennustus
![image](https://github.com/user-attachments/assets/fb9e7f48-460f-4de3-8c45-59575435337a)

Normaalikaton ennustuksessa näkyy, että elokuussa tuotanto tulee olemaan suurempaa, mutta sitä seuraavat päivät tai kuukaudet todennäköisesti tuottavat vähemmän sähköä. Kuitenkin mahdollisuus tuottaa enemmän sähköä on edelleen hyvä. Datan 'log-likelihood' on alempi kuin viherkaton datassa; paras log-likelihood, joka voitiin saada analyysiin, on "75,499". Tämä tarkoittaa, että data sopii analyysiin, mutta se on huomattavasti vähemmän sopivaa kuin viherkaton data.

Molemmissa tuloksissa on ollut 95 %:n luottamusväli, joka tarkoittaa että analyysissä ollaan 95 % varmoja sähköntuoton laskusta. Ennusteen mukaan kuitenkin viherkatossa se nousee hyvin, kun taas normaalikatossa tuotanto todennäköisemmin laskee.

### Käyttöliitymä
Käyttöliittymään saatiin tuloksia POST- ja GET-pyynnöillä KNIME-sovelluksella. Kaikki tulokset KNIMEstä lähetettiin Python-nodella Express-palvelimelle, jossa POST-pyyntö vastaanotettiin. Mahdollisesti seuraavassa sprintissä analyysitulokset tallennetaan POST-pyynnön avulla tietokantaan. Tietokannasta tieto haetaan sitten GET-pyynnöllä.

[![Image from Gyazo](https://i.gyazo.com/8ab18f2a0adef78cf456b7a0400b8f52.gif)](https://gyazo.com/8ab18f2a0adef78cf456b7a0400b8f52)


### Time-Series Pythonilla

<img width="1045" alt="timeSeriesPy" src="https://github.com/user-attachments/assets/920ed23c-a5f5-456b-885b-c5484b4125ac">
-Aikasarjan visualisointi: Visualisoidaan lämpötilan ja kosteuden muutokset ajan suhteen jokaisessa zonessa, jotta kausivaihtelut tulisivat esille.

 
-Päivittäisten keskiarvojen laskenta: Laskettiin päivittäisiä keskiarvoja kosteudelle ja lämpötilalle eri zoneissa, mikä auttaa tunnistamaan pidemmän aikavälin muutoksia.

-Ennustaminen ARIMA-mallilla: Käytettiin ARIMA-mallia ennustamaan lämpötilan kehitystä valitulle zonelle seuraavien päivien ajalle. Tämä tarjoaa näkymän tulevaan lämpötilakehitykseen.

<img width="1042" alt="Screenshot 2024-11-03 194326" src="https://github.com/user-attachments/assets/9bc54fdc-60e8-4849-8923-da7a9e3b8d5f">


## [Seuraava Sprint](SprintReview5.md)
## [Sprintit](SprintList.md)
