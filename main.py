import pygame
import random
import sys

pygame.init()

# Asetukset
leveys = 800
korkeus = 600
naytto = pygame.display.set_mode((leveys, korkeus))
fontti = pygame.font.SysFont("Arial", 24)
fontti2 = pygame.font.SysFont("Arial", 40, bold=True)
taustakuva = pygame.image.load("tausta.jpg")    
taustakuva = pygame.transform.scale(taustakuva, (leveys, korkeus))

hirsipuu_kuvat = [pygame.image.load("hangman-0.png"), pygame.image.load("hangman-1.png"),
                  pygame.image.load("hangman-2.png"), pygame.image.load("hangman-3.png"),
                  pygame.image.load("hangman-4.png"), pygame.image.load("hangman-5.png"),
                  pygame.image.load("hangman-6.png")]

pygame.display.set_caption("Hirsipuu")

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
        self.vaikeus = [4,5,6]
        self.__vaarat_kirjaimet = []
        self.pelitilanne = 0
        self.nykyinen_pelaaja = 0

    def __str__(self) -> str:
        return " ".join(self.arvattava_sana)

    def vaikeusaste(self, pituus: int):
        if pituus == 4:
            self.kaytettavat_sanat = self.sanalistat.nelja_kirjainta
        if pituus == 5:
            self.kaytettavat_sanat = self.sanalistat.viisi_kirjainta
        if pituus == 6:
            self.kaytettavat_sanat = self.sanalistat.kuusi_kirjainta
    
    def vaikeus_valinta(self, vaikeus: int):
        self.vaikeusaste(self.vaikeus[vaikeus])
        self.oikea_vastaus = self.uusi_sana()
        self.arvattava_sana = list("_" * len(self.oikea_vastaus))

    def uusi_peli(self):
        while True:
            self.tausta()
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
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 50))
            teksti = fontti.render("1 = Helppo", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 100))
            teksti = fontti.render("2 = Keskivaikea", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 150))
            teksti = fontti.render("3 = Vaikea", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 200))

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
                        #self.arvaa(syote)
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
                        
            self.tausta()
            self.piirra_hirsipuu()
            self.piira_arvattava_sana()
            self.piira_vaarat()
            self.piirra_vuoro()
            teksti = fontti.render("Arvattava sana tai kirjain (Enter hyväksyy): " + syote, True, (0,0,0))
            naytto.blit(teksti, (100, korkeus - 150))
            
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
        while True:
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                    pygame.quit()
            
            self.tausta()
            self.piirra_hirsipuu()
            
            teksti = fontti.render("Peli päättyi!", True, (0,0,0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 250))
            if voitto:
                teksti = fontti.render("Voitit!", True, (0,0,0))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 200))
                teksti = fontti.render("Arvasit sanan joka oli: " + self.oikea_vastaus, True, (0,0,0))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 175))
            else:
                teksti = fontti.render("Hävisit!", True, (0,0,0))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 200))
                teksti = fontti.render("Oikea sana oli: " + self.oikea_vastaus, True, (0,0,0))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 175))
                
            pygame.display.flip()

    def arvaa(self, syote):
        if self.arvaus(syote):
            self.piira_arvattava_sana()
        else:
            self.piira_vaarat()

    def piirra_hirsipuu(self):
        kuva = hirsipuu_kuvat[self.pelitilanne]
        naytto.blit(kuva,(leveys //2 - kuva.get_width() // 2, 10))

    def piira_arvattava_sana(self):
        arvattava_sana = fontti2.render(" ".join(self.arvattava_sana), True, (0,0,0))
        naytto.blit(arvattava_sana, (leveys // 2 - arvattava_sana.get_width() // 2, korkeus - 200))

    def piira_vaarat(self):
        teksti = fontti.render("Väärät kirjaimet:", True, (0,0,0))
        naytto.blit(teksti, (100, korkeus - 115))
        vaarat = ",".join(sorted(self.__vaarat_kirjaimet))
        teksti = fontti.render(vaarat, True, (0,0,0))
        naytto.blit(teksti, (100, korkeus - 90))


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

            self.tausta()
            syote_alue = fontti.render(viesti + teksti, True, (0, 0, 0))
            naytto.blit(syote_alue, (leveys // 2 - syote_alue.get_width() // 2, korkeus // 2))

            pygame.display.flip()
        return teksti
           
    def tausta(self):
        naytto.fill((0, 0, 0))
        naytto.blit(taustakuva, (0, 0))
        
    def pelaa(self):
        while True:
            self.tausta()

            # Aloitusnäyttö
            teksti = fontti2.render("HIRSIPUU", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 80 + teksti.get_height()// 2))
            teksti2 = fontti.render("F1 - Uusi peli", True, (0, 0, 0))  # F1 - Uusi peli
            naytto.blit(teksti2, (leveys // 2 - teksti2.get_width() // 2, 150 + teksti.get_height()// 2))
            teksti3 = fontti.render("F2 - Lisää pelaaja", True, (0, 0, 0))  # F2 - Lisää pelaaja
            naytto.blit(teksti3, (leveys // 2 - teksti3.get_width() // 2, 200 + teksti.get_height()// 2))
            teksti4 = fontti.render("ESC - Lopeta", True, (0, 0, 0))  # ESC - Lopeta
            naytto.blit(teksti4, (leveys // 2 - teksti4.get_width() // 2, 250 + teksti.get_height()// 2))

            pygame.display.flip()
            pygame.time.delay(10)

            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_F1:
                        self.uusi_peli()
                    if tapahtuma.key == pygame.K_F2:
                        self.lisaa_pelaaja()
                    if tapahtuma.key == pygame.K_ESCAPE:
                        pygame.quit()
                        
            pygame.display.flip()

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

if __name__ == "__main__":
    hirsipuu = Hirsipuu()
    hirsipuu.pelaa()

    pygame.quit()
