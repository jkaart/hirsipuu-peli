import pygame
import random
import sys
import os

pygame.init()

# Asetukset
leveys = 800
korkeus = 600
naytto = pygame.display.set_mode((leveys, korkeus))

# Fontit
fontti = pygame.font.Font("creepster.ttf", 30)
fontti2 = pygame.font.Font("creepster.ttf", 70)
fontti3 = pygame.font.Font("creepster.ttf", 20)

# Taustakuvat
taustakuva_polku = os.path.join("taustat", "tausta3.jpg")
taustakuva2_polku = os.path.join("taustat", "tausta2.jpg")
taustakuva = pygame.image.load(taustakuva_polku)
taustakuva2 = pygame.image.load(taustakuva2_polku)

# skaalataan taustakuva koko ruudun kokoiseksi
taustakuva = pygame.transform.scale(taustakuva, (leveys, korkeus))
taustakuva2 = pygame.transform.scale(taustakuva2, (leveys, korkeus))

# Kuvat
hirsipuu_kuvat = []
for i in range(1, 8):
    kuva_polku = os.path.join("hangman_kuvat", f"hangman{i}bg.png") 
    hirsipuu_kuvat.append(pygame.image.load(kuva_polku))

pygame.display.set_caption("Hirsipuu")

kello = pygame.time.Clock()
class Pelaaja:
    def __init__(self, nimi: str) -> None:
        self.nimi = nimi
        self.pisteet = 0

    def lisaa_piste(self):
        self.pisteet += 1

    def hae_pisteet(self):
        return self.pisteet

    def __str__(self) -> str:
        return f"Pelaajan {self.nimi} pisteet {self.pisteet}"

class Hirsipuu:
    def __init__(self) -> None:
        self.sanalistat = Sanalistat()
        self.pelaajat = []
        self.kaytettavat_sanat = []
        self.oikea_vastaus = ""
        self.arvattava_sana = ""
        self.__vaarat_kirjaimet = []
        self.pelitilanne = 0
        self.nykyinen_pelaaja = 0

    def __str__(self) -> str:
        return " ".join(self.arvattava_sana)

    def vaikeusaste(self, vaikeus: int):
        if vaikeus == 0:
            self.kaytettavat_sanat = self.sanalistat.nelja_kirjainta
        elif vaikeus == 1:
            self.kaytettavat_sanat = self.sanalistat.viisi_kirjainta
        elif vaikeus == 2:
            self.kaytettavat_sanat = self.sanalistat.kuusi_kirjainta
    
    def vaikeus_valinta(self, vaikeus: int):
        self.vaikeusaste(vaikeus)
        self.oikea_vastaus = self.uusi_sana()
        self.arvattava_sana = list("_" * len(self.oikea_vastaus))

    def uusi_peli(self):
        while True:
            self.tausta2()
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                        pygame.quit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if tapahtuma.key == pygame.K_1:
                        self.helppo()
                    if tapahtuma.key == pygame.K_2:
                        self.keskivaikea()
                    if tapahtuma.key == pygame.K_3:
                        self.vaikea()

            teksti = fontti.render("Vaikeusaste", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 150))
            
            teksti = fontti.render("1 = Helppo", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 200))
            teksti = fontti.render("2 = Keskivaikea", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 250))
            teksti = fontti.render("3 = Vaikea", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 300))

            pygame.display.flip()
        
    def helppo(self):
        self.peliruutu(0)

    def keskivaikea(self):
        self.peliruutu(1)

    def vaikea(self):
        self.peliruutu(2)

    def peliruutu(self, vaikeusaste: int):
        self.vaikeus_valinta(vaikeusaste)
        syote = ""

        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    pygame.quit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.unicode in "abcdefghijklmnopqrstuvwxyzåäö":
                        syote += tapahtuma.unicode
                    elif tapahtuma.key == pygame.K_BACKSPACE:
                        syote = syote[:-1]
                    
                    elif tapahtuma.key == pygame.K_RETURN:
                        if self.arvaus(syote):
                            syote = ""
                        else:
                            syote = ""
                            if self.pelitilanne < len(hirsipuu_kuvat)-1:
                                self.pelitilanne += 1
                        self.vuoronvaihto() # Vaihdetaan vuoroa

            self.tausta2()
            self.piirra_hirsipuu()
            self.piira_arvattava_sana()
            self.piira_vaarat()
            self.piirra_vuoro()
            teksti = fontti.render("Arvattava sana tai kirjain (Enter hyväksyy): " + syote, True, (0,0,0))
            naytto.blit(teksti, (100, korkeus - 200))
            
            pygame.display.flip()

            if "".join(self.arvattava_sana) == self.oikea_vastaus:
                self.lopetus_ruutu(True)
            if self.pelitilanne == len(hirsipuu_kuvat) -1:
                self.lopetus_ruutu(False)

    def vuoronvaihto(self):
        self.pelaajat.append(self.pelaajat.pop(0))      

    def piirra_vuoro(self):
        vuoro_teksti = fontti.render("Pelaaja: " + self.pelaajat[0].nimi, True, (0, 0, 0))
        naytto.blit(vuoro_teksti, (leveys // 2 - vuoro_teksti.get_width() // 2, korkeus - 250))


    def lopetus_ruutu(self, voitto: bool):
        hangman = hangmanAnimaatio()
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    pygame.quit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_RETURN:
                        self.__vaarat_kirjaimet = []
                        self.pelitilanne = 0
                        self.uusi_peli()
                    if tapahtuma.key == pygame.K_ESCAPE:
                        pygame.quit()
            
            self.tausta2()
            
            teksti = fontti.render("Peli päättyi!", True, (0,0,0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 250))
            if voitto:
                hangman.paivita_kuva()
                naytto.blit(hangman.piirra_kuva(),(leveys //2 - hangman.leveys() // 2, 50))
                teksti = fontti.render("Voitit!", True, (0,0,0))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 200))
                teksti = fontti.render("Arvasit sanan joka oli: " + self.oikea_vastaus, True, (0,0,0))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 150))
            else:
                self.piirra_hirsipuu()
                teksti = fontti.render("Hävisit!", True, (0,0,0))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 200))
                teksti = fontti.render("Oikea sana oli: " + self.oikea_vastaus, True, (0,0,0))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 175))
            
            teksti = fontti.render("Enter = Uusi peli ESC = lopeta peli", True, (0,0,0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - teksti.get_height() - 20))

            pygame.display.flip()
            kello.tick(60)

    def piirra_hirsipuu(self):
        kuva = hirsipuu_kuvat[self.pelitilanne]
        naytto.blit(kuva,(leveys //2 - kuva.get_width() // 2, 50))

    def piira_arvattava_sana(self):
        arvattava_sana = fontti2.render(" ".join(self.arvattava_sana), True, (0,0,0))
        naytto.blit(arvattava_sana, (leveys // 2 - arvattava_sana.get_width() // 2, korkeus - 175))

    def piira_vaarat(self):
        teksti = fontti.render("Väärät kirjaimet:", True, (0,0,0))
        naytto.blit(teksti, (100, korkeus - 100))
        vaarat = ",".join(sorted(self.__vaarat_kirjaimet))
        teksti = fontti.render(vaarat, True, (0,0,0))
        naytto.blit(teksti, (100, korkeus - 70))

    def lisaa_pelaaja(self):
        nimi = self.tekstiboxi("Anna pelaajan nimi:")
        pelaaja = Pelaaja(nimi)
        self.pelaajat.append(pelaaja)

        while True:
            lisaa_muita = self.tekstiboxi("Lisätäänkö toinen pelaaja? (k/e): ") 
            if lisaa_muita.lower() == "k":
                nimi = self.tekstiboxi("Anna pelaajan nimi:")
                pelaaja = Pelaaja(nimi)
                self.pelaajat.append(pelaaja)
            else:
                break

        self.uusi_peli()

    # Tekstiboxi johon voi kirjoittaa
    def tekstiboxi(self, viesti: str) -> str:
        teksti = ""                             
        aktiivinen = True
        while aktiivinen:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    pygame.quit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_RETURN:
                        aktiivinen = False
                    elif tapahtuma.key == pygame.K_BACKSPACE:
                        teksti = teksti[:-1]
                    else:
                        teksti += tapahtuma.unicode

            self.tausta2()
            syote_alue = fontti.render(viesti + teksti, True, (0, 0, 0))
            naytto.blit(syote_alue, (leveys // 2 - syote_alue.get_width() // 2, korkeus // 2))

            pygame.display.flip()
        return teksti
           
    def tausta(self):
        naytto.fill((0, 0, 0))
        naytto.blit(taustakuva, (0, 0))

    def tausta2(self):
        naytto.fill((0, 0, 0))
        naytto.blit(taustakuva2, (0, 0)) 
        
    def pelaa(self):
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_RETURN:
                        self.lisaa_pelaaja()
                    if tapahtuma.key == pygame.K_ESCAPE:
                        pygame.quit()
            
            self.tausta()

            # Aloitusnäyttö
            teksti = fontti2.render("HIRSIPUU", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 112 + teksti.get_height()// 2))
            teksti = fontti3.render("Enter - Uusi peli", True, (169, 169, 169))  # Enter - Uusi peli
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 300 + teksti.get_height()))
            teksti = fontti3.render("ESC - Lopeta", True, (169, 169, 169))  # ESC - Lopeta
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 350 + teksti.get_height()))

            pygame.display.flip()
#            pygame.time.delay(10)

    def uusi_sana(self):
        return random.choice(self.kaytettavat_sanat)

    def arvaus(self, syote: str):
        loytyi = False
        if len(syote) == 1: # Jos annetaan yksi kirjain
            for i in range(len(self.oikea_vastaus)):
                if syote == self.arvattava_sana[i]:
                    continue
                if syote == self.oikea_vastaus[i]:
                    self.arvattava_sana[i] = syote
                    loytyi = True
            if not loytyi:
                if syote not in self.__vaarat_kirjaimet:
                    self.__vaarat_kirjaimet.append(syote)
        elif syote == self.oikea_vastaus: # Jos annettu enemmän kuin yksi kirjain ja vastaus on oikein
            self.arvattava_sana = syote
            loytyi = True

        return loytyi

    def vaarat_kirjaimet(self):
        return list(set(self.__vaarat_kirjaimet)) # Poistetaan mahdolliset duplikaatit ja palautetaan takaisin listana

class Sanalistat:
    def __init__(self) -> None:
        self.__nelja_kirjainta = []
        self.__viisi_kirjainta = []
        self.__kuusi_kirjainta = []
        self.lue_tiedostot()

    def lue_tiedosto(self, tiedostonimi: str, sanojen_pituus: int):
            with open(tiedostonimi) as tiedosto:
                for rivi in tiedosto:
                    if rivi.startswith("#"):
                        continue
                    if rivi == "":
                        continue
                    rivi = rivi.replace("\n","")
                    if sanojen_pituus == 4:
                        self.__nelja_kirjainta.append(rivi)
                    elif sanojen_pituus == 5:
                        self.__viisi_kirjainta.append(rivi)
                    elif sanojen_pituus == 6:
                        self.__kuusi_kirjainta.append(rivi)

    def lue_tiedostot(self):
        self.lue_tiedosto("sana_listat/nelja_kirjainta.txt", 4)
        self.lue_tiedosto("sana_listat/viisi_kirjainta.txt", 5)
        self.lue_tiedosto("sana_listat/kuusi_kirjainta.txt", 6)

    @property
    def nelja_kirjainta(self):
        return self.__nelja_kirjainta
    
    @property
    def viisi_kirjainta(self):
        return self.__viisi_kirjainta
    
    @property
    def kuusi_kirjainta(self):
        return self.__kuusi_kirjainta

class hangmanAnimaatio:
    def __init__(self) -> None:
        kansio = "hangman_animaatio/"
        self.kuva = None
        self.kuvat = [pygame.image.load(kansio+"hangman8bg.png"),pygame.image.load(kansio+"hangman9bg.png"),
                        pygame.image.load(kansio+"hangman10bg.png"),pygame.image.load(kansio+"hangman11bg.png"),
                        pygame.image.load(kansio+"hangman12bg.png"),pygame.image.load(kansio+"hangman13bg.png"),
                        pygame.image.load(kansio+"hangman14bg.png"),pygame.image.load(kansio+"hangman15bg.png"),
                        pygame.image.load(kansio+"hangman16bg.png"),pygame.image.load(kansio+"hangman17bg.png"),
                        pygame.image.load(kansio+"hangman18bg.png"),pygame.image.load(kansio+"hangman19bg.png"),
                        pygame.image.load(kansio+"hangman20bg.png"),pygame.image.load(kansio+"hangman21bg.png"),
                        pygame.image.load(kansio+"hangman22bg.png"),pygame.image.load(kansio+"hangman23bg.png")]
        self.laskuri = 0
        self.indeksi = 0
        self.nopeus = 10

    def paivita_kuva(self):
            self.laskuri += 1
            if self.indeksi == len(self.kuvat):
                    # self.indeksi = 0 # jos halutaan looppaamaan
                    return
            self.kuva = self.kuvat[self.indeksi]
            if self.laskuri > self.nopeus:
                    self.indeksi += 1
                    self.laskuri = 0

    def piirra_kuva(self):
          return self.kuva
    
    def leveys(self):
        return self.kuva.get_width()
    
    def korkeus(self):
        return self.kuva.get_height()

if __name__ == "__main__":
    hirsipuu = Hirsipuu()
    hirsipuu.pelaa()

