
# Hirsipuu-peli

Tämä hirsipuu-peli on perinteisesti kynällä ja paperilla pelattavavasta hirsipuu pelistä poikkeava tietokoneella pelattava versio.

Pelissä tietokone arpoo sanalistoista sanan ja pelaaajat yrittävät arvata koko sanan tai siinä olevan kirjaimen.
Peli on ohjelmoitu python kielellä käyttössä on myös Pygame kirjasto

> [!WARNING]
> Peli saattaa sisältää hieman kyseenalaisia sanoja koska sen sisältämät sanat ovat peräisin [kotus.fi nykysuomen sanalistasta](https://www.kotus.fi/aineistot/sana-aineistot/nykysuomen_sanalista) ja ovat sanaluokaltaan substantiivejä.

## Pelin suorittaminen ja vaatimukset

### Vaatimukset

#### Windows
- Python tulkki https://www.python.org/downloads/windows/
- Pygame kirjasto Windowsin komentokehotteessa `pip3 install pygame`

***

#### Linux
Debian pohjaisissa jakeluissa (Ubuntu, mint ja yms.)
- Python tulkki `sudo apt install python3` komennolla terminaalissa
- Pygame kirjasto joko `pip3 install pygame` tai `sudo apt python3-pygame` komennolla terminaalissa

***

### Suorittaminen
Komentokehotteessa tai terminaalissa hirsipuu-peli kansiossa ajettuna `python3 main.py` komento käynistää pelin
