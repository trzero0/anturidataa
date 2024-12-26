## Sprint 1 Review
Ensimmäisessä sprintissä tavoitteena oli luoda projektiryhmälle github, discord ja trello. Tavoitteena oli myös valita sopiva työkalu datan analysointiin ja ryhmämme päätyi valitsemaan tähän KNIME analytics platformin. Tutustuimme KNIME:n toimintaan ja kartoitimme sen mahdollisuuksia projektimme tarkoituksiin.
Analysoimme "Knimellä" kahden muuttujan vaikutusta toisiinsa ja vertailtiin niitä. Analyysiin käytettiin relevanttia testidataa, koska oikeuksia varsinaiseen dataan ei vielä ollut.
Datasta ei ollut riittävästi informaatiota esimerkiksi siitä, mihin tarkoituksiin näitä aurinkopaneeleja käytetään ja mitkä ovat toivotut tulokset.

### Knimen analysointi rakenne
![image](https://github.com/user-attachments/assets/a59379f2-dbe4-4bff-8da6-6a498ac26eb3)

Tässä analysoitiin, kumpi puoli aurinkopaneelista on tehokkaampi ja kumpi tuottaa eniten sähköä. Koska testidatasta ei ollut paljon tietoja, oikeaa syytä tähän ei tiedetä.

![image](https://github.com/user-attachments/assets/f5640fd2-40b2-44c8-aeb1-65d99b3c8270)

Toisessa analyysissä tutkimme, vaikuttaako paneelin paikkatieto sähköntuottoon.
![alt text](Images/image.png)
Kuvassa x-akselilla on paneelin top-paikkatieto ja y-akselilla on sähköntuotto.
Tästä voimme pääetellä että, kun paikkatieto on 300 ja 550 välillä, sähköntuotto on tasaista ja tästä ylöspäin mentäessä sähköntuotto vaihtelee.


Seuraavaksi haettiin Python-koodilla dataa "Google Cloudista" Knimeen ja muunnettiin se JSON-muotoon.
Knimessä käytetään koodia "Python-nodeissa", ja tätä varten piti ladata Anaconda.
Anacondalla saatiin paketteja ja Python-ympäristö käyttöön Knimessä. Anacondan kautta pystyy lataamaan tarvittavia paketteja, joita tarvitaan "Google Cloudiin" yhdistämiseen.

### Knimen Anaconda Paketit -> Python koodi joka tuo dataa "Google CLoudista"
![image](https://github.com/user-attachments/assets/3e082db7-381c-4de8-835d-de340ac761b8)

## [Seuraava Sprint](SprintReview2.md)
## [Sprintit](SprintList.md)

