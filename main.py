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
taustakuva2_polku = os.path.join("taustat", "tausta9.jpg")
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
        self.pisteet += 3

    def hae_pisteet(self):
        return self.pisteet

    def __str__(self) -> str:
        return f"{self.nimi} pisteet {self.pisteet}"

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
                        if syote == "":                         # Jos syötettä ei ole, ei tehdä mitään  
                            continue
                        if self.arvaus(syote):
                            syote = ""
                        else:
                            syote = ""
                            if self.pelitilanne < len(hirsipuu_kuvat)-1:
                                self.pelitilanne += 1
                        self.vuoronvaihto() # Vaihdetaan vuoroa
                    else:
                        pass    # Jos painetaan jotain muuta kuin kirjaimia, backspacea tai enteriä, ei tehdä mitään

            self.tausta2()
            self.piirra_hirsipuu()
            self.piira_arvattava_sana()
            self.piira_vaarat()
            self.piirra_vuoro()
            self.piirra_pisteet()
            teksti = fontti.render("Arvattava sana tai kirjain (Enter hyväksyy): " + syote, True, (204,196,188))
            naytto.blit(teksti, (100, korkeus - 180))
            
            pygame.display.flip()
            pygame.time.delay(10) 

            if "".join(self.arvattava_sana) == self.oikea_vastaus:
                self.lopetus_ruutu(True)
            if self.pelitilanne == len(hirsipuu_kuvat) -1:
                self.lopetus_ruutu(False)

    def vuoronvaihto(self):
        self.pelaajat.append(self.pelaajat.pop(0))      

    def piirra_vuoro(self):
        vuoro_teksti = fontti.render("Pelaaja: " + self.pelaajat[0].nimi, True, (235,117,25))
        naytto.blit(vuoro_teksti, (leveys // 2 - vuoro_teksti.get_width() // 2, korkeus - 230))

    def lopetus_ruutu(self, voitto: bool):
        hangman_kavely = hangmanAnimaatio("kavely")
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
            
            teksti = fontti.render("Peli päättyi!", True, (235,81,25))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 190))
            if voitto:
                hangman_kavely.paivita_kuva()
                naytto.blit(hangman_kavely.piirra_kuva(),(leveys //2 - hangman_kavely.leveys() // 2, 50))
                teksti = fontti.render("Voitit!", True, (25,255,90))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 150))
                teksti = fontti.render("Arvasit sanan joka oli: " + self.oikea_vastaus, True, (25,255,90))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 120))
            else:
                self.piirra_hirsipuu()
                teksti = fontti.render("Oikea sana oli: " + self.oikea_vastaus, True, (25,255,90))
                naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - 130))
            
            teksti = fontti.render("Enter = Uusi peli ESC = lopeta peli", True, (250,203,40))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, korkeus - teksti.get_height() - 20))

            self.piirra_pisteet()

            pygame.display.flip()
            kello.tick(60)

    def piirra_hirsipuu(self):
        kuva = hirsipuu_kuvat[self.pelitilanne]
        naytto.blit(kuva,(leveys //2 - kuva.get_width() // 2, 60))

    def piira_arvattava_sana(self):
        arvattava_sana = fontti2.render(" ".join(self.arvattava_sana), True, (25, 255, 0))
        naytto.blit(arvattava_sana, (leveys // 2 - arvattava_sana.get_width() // 2, korkeus - 155))

    def piira_vaarat(self):
        teksti = fontti.render("Väärät kirjaimet:", True, (204,196,188))
        naytto.blit(teksti, (100, korkeus - 80))
        vaarat = ",".join(sorted(self.__vaarat_kirjaimet))
        teksti = fontti.render(vaarat, True, (255, 0, 0))
        naytto.blit(teksti, (100, korkeus - 50))

    def piirra_pisteet(self):
        for pelaaja in self.pelaajat:   
            teksti = fontti3.render(str(pelaaja), True, (235,117,25))     
            naytto.blit(teksti, (10, 10 + 40 * self.pelaajat.index(pelaaja)))


    def lisaa_pelaaja(self):
        while True:
            nimi = self.tekstiboxi("Anna pelaajan nimi:")
            if nimi:                                                                 # Jos nimi on annettu, lisätään pelaaja
                pelaaja = Pelaaja(nimi)
                self.pelaajat.append(pelaaja)
            else:                                                                    # Jos nimeä ei ole annettu, ei tehdä mitään
                continue

            while True:
                lisaa_muita = self.tekstiboxi("Lisätäänkö toinen pelaaja? (k/e): ")  # Kysytään halutaanko lisätä muita pelaajia (k/e)   
                if lisaa_muita.lower() == "k":                                       # Jos vastaus on k, lisätään uusi pelaaja
                    nimi = self.tekstiboxi("Anna pelaajan nimi:")                    # Kysytään uuden pelaajan nimi
                    if not nimi:                                                     # Jos nimeä ei ole annettu, ei tehdä mitään
                        continue
                    else:  
                        pelaaja = Pelaaja(nimi)                                      # Jos toinenkin nimi on annettu, lisätään pelaaja
                        self.pelaajat.append(pelaaja)                                # Lisätään pelaaja listaan
                elif lisaa_muita.lower() == "e":                                     # Jos vastaus on e, ei lisätä muita pelaajia...
                    break                                                            # ...ja jatketaan peliin
                                
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
#           pygame.time.delay(10)

    def uusi_sana(self):
        return random.choice(self.kaytettavat_sanat)

    def arvaus(self, syote: str):
        loytyi = False
        if len(syote) == 1:                                                             # Jos annetaan yksi kirjain
            for i in range(len(self.oikea_vastaus)):                                    # Käydään läpi oikea vastaus
                if syote == self.arvattava_sana[i]:                                     # Jos syöte on jo arvattu
                    continue                                                            # Jatketaan seuraavaan
                if syote == self.oikea_vastaus[i]:                                      # Jos syöte on oikea kirjain
                    self.arvattava_sana[i] = syote                                      # Lisätään kirjain arvattavaan sanaan
                    loytyi = True
            if not loytyi:                                                              # Jos syöte ei ole oikea kirjain
                if syote not in self.__vaarat_kirjaimet:                                # ja jos syöte ei ole jo väärissä kirjaimissa
                    self.__vaarat_kirjaimet.append(syote)                               # Lisätään syöte väärin arvattuihin
                    if self.pelaajat[self.nykyinen_pelaaja].pisteet > 0:                # Jos pelaajalla on pisteitä...
                        self.pelaajat[self.nykyinen_pelaaja].pisteet -= 1               # voidaan vähentää pelaajan pisteitä vääristä arvauksista
            if loytyi:
                self.pelaajat[self.nykyinen_pelaaja].lisaa_piste()                      # Lisätään pelaajalle pisteitä 3 kpl jos vastaus on oikein
        elif syote == self.oikea_vastaus: 
            self.arvattava_sana = syote                                                 # Jos syöte on oikea sana  
            loytyi = True   
            self.pelaajat[self.nykyinen_pelaaja].pisteet += 10                          # Lisätään pelaajalle pisteitä 10 kpl jos vastaus on oikein
        else:
            if syote == self.oikea_vastaus and len(syote) == len(self.oikea_vastaus):   # Jos syöte on oikea sana ja pituus on sama kuin oikea sana 
                self.arvattava_sana = syote                                            
                loytyi = True
                self.pelaajat[self.nykyinen_pelaaja].pisteet += 10                      # Lisätään pelaajalle pisteitä 10 kpl jos vastaus on oikein

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
            with open(tiedostonimi, encoding="utf-8") as tiedosto:
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
    def __init__(self, kansio:str) -> None:
        polku = "animaatio/" + kansio
        self.kuva = None
        tnimet = sorted([os.path.join(polku, kuva) for kuva in os.listdir(polku) if kuva.endswith(".png")])
        self.kuvat = [pygame.image.load(kuva) for kuva in tnimet]
        
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

