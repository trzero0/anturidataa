## Sprint 3 Review

Sprintissä käytetty aika: 64 tuntia

Scrum master: Muhammed Özturk

Kolmannessa sprintissä oli tavoitteena jatkaa MOCA analyysia, PCA analyysia, selkeyttää viherkaton datan eroavaisuuksia, sekä aloittaa REACT sivun tekeminen aikaisempien suunnitelmien perusteella.

### KNIME analyysi

Yhdistettiin sähköntuottoa analyysiin mukaan. Sähköntuottodataa oli vain kahdelta kuukaudelta: heinä- ja elokuulta, joten analyysi ei ole hirveän kattava, eikä tuloksista näy esim. kausien vaikutusta sähköntuottoon. Yksittäisten paneelien sähköntuottoa ei ollut saatavilla, joten kattojen välisiä eroja analysoitaessa on käytetty keskiarvoa kaikkien paneelien tuotosta (tuotto/paneelien määrä). 
![sähköntuootto](Images/tuotto.png)
Kuvassa nähdään kattojen tuottoa. Voidaan havaita, että 22-25.5 tuotto on viherkatolla ollut parempaa, mutta muina aikoina tuotot ovat lähes samaa luokkaa.

![Pca-analyysi](Images/matrix.png)
Toteutettiin PCA-analyysiä KNIMEllä, joka sijoitteli annetut arvot klustereihin. Analyysituloksista voidaan havaita, ettei PCA-analyysillä tunnisteta suuria eroja zonejen välillä, koska zonet eivät ilmene analyysin klustereiksi.


### Käyttöliittymä

![Käyttöliittymä ver1](Images/käyttisver1.gif)

Tehtiin React-kirjastolla ja TypeScript ohjelmointikielellä ensimmäinen versio käyttöliittymästä. Käyttöliittymässä on kalenteri elementti, josta määritellään ajanjakson, jolta dataa haetaan.

Kalenteri elementti käyttää **React-date-range** -kirjastoa. Kalenteri näyttää kaksi kuukautta vierekkäin, jotta käyttäjä voi helposti valita ajanjakson laajalta aikaväliltä. Päivämäärät voi valita alusta ja lopusta, minkä jälkeen käyttöliittymä lähettää valitut päivämäärät muuhun logiikkaan kuvaajia varten. Kalenteri elementti ei vastaa vielä lopullista versiota.

Käyttöliittymässä on kaksi erillistä monivalintalaatikkoa, joissa käyttäjä voi valita zone-alueen ja sen muuttujat (esim. kosteus ja lämpötila). Monivalintalaatikko elementit käyttävät **React-select** -kirjastoa.

### Multiblock component analyysi pythonilla
 
<img width="737" alt="pla" src="https://github.com/user-attachments/assets/b749cf30-f35d-4335-9f9d-349e1f09a7a8">

tehtiin analyysi käyttämällä Partial Least Squares Regression (PLSRegression) -luokkaa, joka on osa scikit-learnin (sklearn.cross_decomposition) kirjastoa.

X on selittävien muuttujien matriisi (tässä tapauksessa kosteus ja lämpötila).

Y on riippuvien muuttujien matriisi (kosteutta placeholderina).

## [Seuraava Sprint](SprintReview4.md)
## [Sprintit](SprintList.md)
