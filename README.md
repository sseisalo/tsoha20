# keskustelusovellus
Projekti on Redditin/Jodelin kaltainen keskustelusovellus. Kommentoitavat keskustelualoitukset luodaan tietylle "feedille", jotka näkyvät käyttäjälle tämän selatessa kyseistä feediä tai kaikki aloitukset sisältävää etusivua. Käyttäjä voi olla joko peruskäyttäjä, joka voi kommentoida, tehdä aloituksia, sekä tilata haluamiaan feedejä, tai moderaattori, joka voi peruskäyttäjän toimintojen lisäksi poistaa asiattomia viestejä/käyttäjiä ja estää tietyille feedeille kirjoittamisen.

# Muita keskeisiä toimintoja
* Jokainen käyttäjä voi arvostella keskustelunaloituksia ja kommentteja antamalla niille joka ylä- tai alapeukun. Aloituksen tai kommentin suosio lasketaan pisteillä, jonka kaava on (yläpeukut - alapeukut).
* Aloituksia voidaan etsiä merkkijonohaulla, ja tulokset voidaan järjestää julkaisuajankohdan tai aloituksen suosion perusteella.
* Viestejä voidaan luonnollisesti muokata ja poistaa jälkikäteen, mutta aloituksen voi vain poistaa (jolloin aloituksen alla olevat kommentit poistuvat samalla).

# Sovelluksen nykytilanne
* Sovellus löytyy [täältä.](https://zzlo-keskustelusovellus.herokuapp.com/)
* Sovelluksessa on perustoiminnallisuus rekisteröitymiselle ja kirjautumiselle, kanaville/syötteille, uusille aloituksille, sekä kommennoinnille.
* ~~Kanaville ei ole vielä luotu hakutoimintoa, kanaville pääsee tällä hetkellä vain joko olemassaolevan aloituksen kautta tai syöttämällä urliin /ch/\<kanava>, kun \<kanava> on haluttu kanava.~~ Hakutoiminto on luotu. Toiminnon käytettävyys mobiililla on noin 0%, mutta sivulliset uhrit ovat välttämättömiä.
* CSS on pitkälti valmis
* Sovelluksessa on testikäyttäjä, tunnus:salasana: testi:testi123.


Sovellus ei ole aivan valmis, mutta tulevien ominaisuuksien lisäämisessä ei tule kestämään kauan. Lisättäviä ominaisuuksia on moderaattorikäyttäjät, aloituksien äänestys, sekä viestien kommentointi/poistaminen.
