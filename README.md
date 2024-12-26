# AnturiData Innovaatio Projekti

Jäsenet: Julia Köykkä, Atte Räisänen, Mikko Tanhola, Kaspar Tullus, Muhammed Özturk

# Sisällysluettelo <a name="sisäl"></a>
1. [Johdanto](#joh)
2. [Projektivaatimukset](#vaat)
3. [Kehitysmenetelmät](#kehmen)\
&nbsp;&nbsp;&nbsp;&nbsp;3.1 [Sprintti 1](#s1)\
&nbsp;&nbsp;&nbsp;&nbsp;3.2 [Sprintti 2](#s2)\
&nbsp;&nbsp;&nbsp;&nbsp;3.3 [Sprintti 3](#s3)\
&nbsp;&nbsp;&nbsp;&nbsp;3.4 [Sprintti 4](#s4)\
&nbsp;&nbsp;&nbsp;&nbsp;3.5 [Sprintti 5](#s5)\
&nbsp;&nbsp;&nbsp;&nbsp;3.6 [Sprintti 6](#s6)\
&nbsp;&nbsp;&nbsp;&nbsp;3.7 [Sprintti 7](#s7)
4. [Projektin suunnittelu](#suun)\
    4.1 [Data-analyysi](#analy)\
    4.2 [Sovellusarkkitehtuuri](#sov)
5. [Data-analyysi syventävästi](tulk)
6. [Sovelluksen käyttöönotto](otto)\
    6.1 [Edellytykset](#edel)\
    6.2 [Asennus](#asen)\
    6.3 [Käyttöohje](#käyt)
7. [Testaus](#test)
8. [Yhteenveto](#yht)

## Johdanto <a name="joh"></a>
Projektin tavoitteena on tutkia aurinkopaneelien eroja analysoimalla antureiden dataa KNIME-ohjelmistolla ja Python-ohjelmoinnilla. Lisäksi pyritään toteuttamaan React-käyttöliittymä, jonka API yhdistyy Expressin avulla KNIME-palvelimeen. Käyttöliittymän avulla asiakas voi tarkastella dataa, esimerkiksi vertailemalla eri alueiden aurinkopaneelien kosteuden ja lämpötilan tasoja. Projektin aikataulutuksessa noudatetaan ketterää menetelmää ja hyödynnetään Trelloa.

## Projektivaatimukset <a name="vaat"></a>

Pääasiallisena asiakasvaatimuksena oli toteuttaa data-analyysi asiakkaan palvelimelle tallennetulle datalle. Asiakasta kiinnosti erityisesti, kuinka kastellun viherkaton sähköntuoton anturidata poikkeaa valkopohjaisen ja mustapohjaisen katon anturidatasta. Opettajan suosituksesta vaatimuksena oli käyttää Pythonin lisäksi data-analysointiin erikoistunutta ohjelmistoa, jonka avulla data-analyysiä voidaan hahmottaa helpommin.

Ohjelmistotuotannon opiskelijoina ryhmän projektivaatimuksena oli myös kehittää web-sovellus, jonka avulla data-analyysiä voidaan tarkastella. Sovellukselle ei kuitenkaan saatu tarkempia asiakasvaatimuksia.

Sovelluksen edetessä budjetointiin, se erikoistui Python-pohjaiseen data-analyysiin, sillä KNIME-palvelimen analysointi osoittautui liian resursseja kuluttavaksi.

## Kehitysmenetelmät <a name="kehmen"></a>

Projektihallinnassa käytettiin ketterää Scrum-menetelmää. Aikaraja jaettiin kahden viikon jaksoihin, jotka määriteltiin sprintteinä. Kaikissa paitsi ensimmäisessä sprintissä oli Scrum-mestari, jonka tehtävänä on ylläpitää tehtävienhallintaa Trellossa. 

(lisää sen sujuvuudesta, haasteellista sairastuessa ja epäselvyyksien myötä jnejne)

Ketterään työskentelyyn kuuluu Scrum-palaverien aikatauluttaminen. Projektissa pidettiin palavereja tarpeen mukaan, pyrkien pitämään niitä vähintään sprinttien alussa ja lopussa. 

Trello linkki

Projektin versiohallintatyökaluna käytettiin GitHub -etätietovarasto.

[Linkki työajanseurantaan](https://metropoliafi-my.sharepoint.com/:x:/g/personal/kaspart_metropolia_fi/EaOvk-hq3rlDtGvIea-mcjcByCtmNadYHdLlSF8qI84Jog?rtime=m9gjtOXa3Eg)

### Sprintti 1 <a name="s1"></a>
Aikataulu: 28.8 - 11.9

Ensimmäisessä sprintissä päätavoitteina oli perustaa projektinhallinnan työkalut ryhmälle, sekä valita sopiva väline datan analysointiin. Projektinhallintaa varten luotiin GitHub, Discord ja Trello, ja analysointityökaluksi valittiin KNIME Analytics Platform. Aluksi tutustuttiin KNIMEn toimintaan ja arvioitiin sen soveltuvuutta projektin tarpeisiin. KNIMEn avulla voitiin analysoida kahden muuttujan välisiä vaikutuksia. Alustavat analyysit tehtiin testidatalla, koska varsinaiseen dataan ei ollut vielä saatu käyttöoikeuksia. Testidatasta ei myöskään löytynyt riittävästi taustatietoa esimerkiksi aurinkopaneelien käyttötarkoituksista tai odotetuista tuloksista.

Ensimmäisessä analyysissa tutkittiin, kumpi aurinkopaneelin puolista tuotti enemmän sähköä. Testidatan rajoitusten vuoksi ilmiön taustasyitä ei voitu tarkasti määrittää. Toisessa analyysissä tarkasteltiin, vaikuttiko paneelin paikkatieto sähköntuottoon. Tulokset osoittivat, että paikkatiedon ollessa välillä 300–550 sähköntuotto pysyi tasaisena, mutta suuremmilla paikkatiedon arvoilla tuotanto alkoi vaihdella.

Analysointiprosessia varten data haettiin Google Cloudista Python-koodilla ja muunnettiin JSON-muotoon KNIMEä varten. Python-koodia käytettiin KNIMEn Python -noodeissa, minkä mahdollistamiseksi asennettiin Anaconda. Anacondan avulla otettiin käyttöön tarvittavat Python-ympäristöt ja ladattiin tarvittavia paketteja Google Cloud -yhteyden muodostamiseksi.

### Sprintti 2 <a name="s2"></a>
Aikataulu: 12.9 - 26.9&nbsp;&nbsp;&nbsp;&nbsp; Scrum-mestari: Kaspar Tullus

Toisessa sprintissä keskityttiin anturidatan analysointiin ja käyttöliittymän suunnittelun aloittamiseen. Sprintissä saatiin tehtyä yksinkertaista analyysiä, mutta sähköntuotannon analyysi jäi vielä kesken. Analysoinnissa tarkasteltiin zonejen lämpötilan ja kosteuden keskiarvoja sekä näiden arvojen jakaumaa. Lisäksi tutkittiin koneoppimismalleja, kuten lineaarista regressiota kosteuden ennustamiseen ja Decision tree -mallia zonejen ennustamiseen. Lineaarisen regression tulokset osoittivat lievää korrelaatiota, mutta Decision tree -malli osoittautui epätarkaksi, sillä 60 % tarkkuus ei ollut riittävä.

KNIME-palvelimen ja käyttöliittymän välistä yhteyttä testattiin. Data haettiin Google Cloud Firestoresta ja käsiteltiin Python -noodien avulla. Tämän jälkeen analyysitulokset lähetettiin Express-palvelimelle POST-kutsuna, ja testattiin, että yhteys toimii. Lisäksi tutkittiin KNIME-palvelimen kustannuksia eri käyttäjämäärillä. Jos käyttäjiä olisi paljon, "Knime Business Hub" -paketti olisi taloudellisin vaihtoehto, mutta pienemmille käyttäjämäärille sopisi paremmin "Team-plan" -sopimus.

Pythonilla tehtiin analyysi, jossa tarkistettiin, saadaanko samoja tuloksia kuin KNIME:llä. Käytössä olivat muun muassa kirjastot pandas, numpy, matplotlib, seaborn ja scikit-learn. Pythonilla saavutetut tulokset olivat samankaltaisia KNIME:llä saatuihin nähden, mutta pieniä eroavaisuuksia havaittiin. Esimerkiksi regressiosuoran R²-arvo oli Pythonilla 0.67, kun KNIME:llä se oli 0.7.

Käyttöliittymän suunnittelussa valittiin ohjelmointikielet ja hahmoteltiin perustoiminnallisuuksia, kuten datan valinta, kuvaajan tyypin vaihtaminen ja datan ajanjakson muokkaaminen. Lisäksi suunniteltiin lisäominaisuuksia, kuten tulosten tallentaminen eri tiedostomuodoissa ja interaktiivinen datan tutkinta. Perustoiminnallisuuksia ja käyttöliittymän yleisilmettä hahmoteltiin Figmassa, ja sekvenssikaaviolla kuvattiin tyypillisiä käyttötapauksia.

### Sprintti 3 <a name="s3"></a>
Aikataulu: 26.9 - 11.10&nbsp;&nbsp;&nbsp;&nbsp; Scrum-mestari: Muhammed Özturk

Kolmannessa sprintissä keskityttiin MOCA- ja PCA-analyysien jatkamiseen, viherkaton datan eroavaisuuksien selkeyttämiseen sekä React-pohjaisen käyttöliittymän kehittämisen aloittamiseen aiemmin tehtyjen suunnitelmien perusteella.

KNIME:llä yhdistettiin sähköntuottodataa osaksi analyysiä. Datan rajoitukset, kuten lyhyt ajanjakso (heinä- ja elokuu) ja yksittäisten paneelien tietojen puuttuminen, heikensivät analyysin kattavuutta. Kattojen sähköntuotosta tarkasteltiin keskiarvoja. Tulokset osoittivat, että viherkatolla oli jonain päivinä parempi tuotto, mutta yleisesti ottaen kattojen tuotot olivat samankaltaisia. PCA-analyysissä klusteroitiin zonejen tietoja, mutta selkeitä eroja ei havaittu, sillä zonet eivät muodostaneet omia klustereitaan.

Pythonilla toteutettiin multiblock component -analyysi käyttäen Partial Least Squares Regression (PLSRegression) -menetelmää, joka kuuluu scikit-learnin (sklearn.cross_decomposition) kirjastoihin. Analyysissä käytettiin selittävinä muuttujina kosteuden ja lämpötilan arvoja (X) ja riippuvana muuttujana kosteutta placeholderina (Y). Tämä analyysi tuki sprintin päätavoitetta syventää ymmärrystä muuttujien välisistä yhteyksistä.

Käyttöliittymän kehittämisessä luotiin ensimmäinen versio React-kirjastolla ja TypeScript-ohjelmointikielellä. Käyttöliittymässä toteutettiin kalenterielementti, joka käyttää React-date-range -kirjastoa. Kalenterin avulla käyttäjä voi valita ajanjakson, jolta dataa haetaan, mutta se on vielä alustava ratkaisu. Lisäksi lisättiin monivalintalaatikoita, joiden avulla käyttäjä voi valita zone-alueen ja sen muuttujat, kuten kosteuden ja lämpötilan. Monivalintalaatikot toteutettiin React-select -kirjastolla, ja niitä kehitettiin seuraavassa sprintissä.

### Sprintti 4 <a name="s4"></a>
Aikataulu: 21.10 - 4.11&nbsp;&nbsp;&nbsp;&nbsp; Scrum-mestari: Mikko Tanhola

Neljännessä sprintissä keskityttiin analyysien syventämiseen käyttämällä aikasarja-analyysiä (Time-Series), ennakoivaa mallinnusta (Predictive Modeling) ja tilastollisten hypoteesien testausta (Statistical Hypothesis Testing). Lisäksi käyttöliittymään tehtiin edistysaskelia tiedon haun ja lähetyksen osalta.

KNIME:llä toteutettiin aikasarja-analyysiä hyödyntämällä Multivariate Time-Series Forecasting -mallia ja ARIMA-mallia. Ennusteissa tarkasteltiin kosteuden ja lämpötilan vaikutuksia viherkattoon ja normaalikattoon.

Multivariate Time-Series Forecasting -analyysin perusteella viherkaton kosteustasoilla ja lämpötiloilla oli vähemmän vaikutusta sähköntuottoon kuin normaalikaton vastaavilla muuttujilla. Viherkatto näytti olevan tehokkaampi sähköntuotossa, mutta tulosta ei voitu pitää lopullisena monien huomioon ottamatta jääneiden tekijöiden vuoksi. ARIMA-mallilla tehty ennustus viherkaton osalta osoitti korkeaa log-likelihood-arvoa, mikä viittasi mallin sopivuuteen. Ennuste antoi suurta todennäköisyyttä sähköntuoton nousulle seuraavien päivien aikana. Normaalikaton ennusteessa näkyi niin ikään tuotannon nousua elokuussa, mutta sen jälkeen todennäköisemmin laskua. Molemmissa tapauksissa ennusteet tehtiin 95 %:n luottamusvälillä.

Pythonilla aikasarja-analyysiä syvennettiin seuraavasti:
- Visualisoitiin lämpötilan ja kosteuden muutoksia ajan suhteen eri zoneissa kausivaihtelujen havainnollistamiseksi.
- Laskettiin päivittäisiä keskiarvoja kosteudelle ja lämpötilalle, mikä toi esille pidemmän aikavälin muutoksia.
- Ennustettiin lämpötilan kehitystä ARIMA-mallilla valituille zoneille, tarjoten näkymää tuleviin lämpötilatrendeihin.

Käyttöliittymässä saavutettiin edistystä POST- ja GET-pyyntöjen avulla. KNIMEstä lähetettiin tuloksia Python-noden kautta Express-palvelimelle, jossa POST-pyynnöt vastaanotettiin. Tiedot aiotaan tulevissa sprinteissä tallentaa tietokantaan, jotta ne voidaan hakea GET-pyynnöillä. Käyttöliittymän ulkoasulle kehitettiin responsiivisempi CSS.

Sprintti antoi merkittävää lisätietoa kattojen välisistä eroista ja valmisteli käyttöliittymää tulevia toiminnallisuuksia varten.

### Sprintti 5 <a name="s5"></a>
Aikataulu: 1.11 - 15.11&nbsp;&nbsp;&nbsp;&nbsp; Scrum-mestari: Atte Räisänen

Sprintin 5 keskeinen tavoite oli käyttöliittymän kehittäminen ja sen integrointi backend-toiminnallisuuksiin sekä analyysitulosten käsittelyyn. Sprintin aikana selvitettiin sopivat grafiikat analyysien visualisointiin, datan vastaanottaminen ja lähettäminen käyttöliittymän kautta, sekä kehitettiin tietokantaintegraatiota.

Pythonilla suoritetut analyysit järjestivät sensoridatan aikajärjestykseen ja sovittivat siihen monipuolisia analyysimalleja. Esimerkiksi ARIMA-mallilla ennustettiin lämpötilan kehitystä, kun taas PCA-analyysi tunnisti tärkeimmät pääkomponentit datassa. Tulokset tallennettiin JSON-muotoon sekä tietokantaan, mikä mahdollistaa niiden tehokkaan jatkokäsittelyn ja visualisoinnin käyttöliittymässä.

Käyttäjän valitsemat parametrit saatiin toimivasti lähetettyä käyttöliittymästä POST-pyynnöllä Pythonille, joka suorittaa tarvittavat analyysit, kuten ARIMA-mallinnuksen, PCA:n ja K-Means-klusteroinnin. Tulokset palautetaan käyttöliittymään ja tallennetaan MongoDB-tietokantaan, josta niitä voidaan hakea GET-pyynnöillä myöhempää tarkastelua varten. SessionID-järjestelmän avulla varmistettiin, että käyttäjäkohtaiset analyysit pysyvät yksityisinä ja helposti saatavilla.

### Sprintti 6 <a name="s6"></a>
Aikataulu: 18.11 - 29.11&nbsp;&nbsp;&nbsp;&nbsp; Scrum-mestari: Julia Köykkä

tiivistelmä sprint 6

### Sprintti 7 <a name="s7"></a>
Aikataulu: &nbsp;&nbsp;&nbsp;&nbsp; Scrum-mestari: 
tiivistelmä sprint 7

[Linkki erillisiin sprintti katsauksiin](SprintReviews/SprintList.md)

## Projektin suunnittelu <a name="suun"></a>
### Data-analyysi <a name="analy"></a>
Ei yksityiskohtia, vasta miten aloittaa

### Sovellusarkkitehtuuri <a name="sov"></a>
Kaaviot rakenteesta ja selitys

## Data-analyysi syventävästi <a name="tulk"></a>
Loput, jaa osiin

## Sovelluksen käyttöönotto <a name="otto"></a>
### Edellytykset <a name="edel"></a>
Mitä tarvitsee että toimii (puuttuvat tiedostot jne)
### Asennus <a name="asen"></a>
Miten asennetaan
### Käyttöohje <a name="käyt"></a>
Miten käytetään

## Testaus <a name="test"></a>
Onko meillä

## Projektin yhteenveto <a name="yht"></a>
t