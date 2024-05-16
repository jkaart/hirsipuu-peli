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
        self.pelaajat = []
        self.sanalista = ["auto","pallo"]
        self.kaytettavat_sanat = []
        self.oikea_vastaus = ""
        self.arvattava_sana = ""
        self.vaikeus = [4,5,6]
        self.__vaarat_kirjaimet = []
        self.pelaa()
#       self.uusi_peli()

    def __str__(self) -> str:
        return " ".join(self.arvattava_sana)

    def vaikeusaste(self, pituus: int):
        for sana in self.sanalista:
            if len(sana) == pituus:
                self.kaytettavat_sanat.append(sana)

    def vaikeus_valinta(self, vaikeus: int):
        self.vaikeusaste(self.vaikeus[vaikeus])
        self.oikea_vastaus = self.uusi_sana()
        self.arvattava_sana = list("_" * len(self.oikea_vastaus))

    def uusi_peli(self):
        while True:
            naytto.fill((0, 0, 0))
            naytto.blit(taustakuva, (0, 0))
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.QUIT:
                        pygame.quit()
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if tapahtuma.type == pygame.K_1:
                        self.vaikeus_valinta[0]
                    if tapahtuma.type == pygame.K_2:
                        self.vaikeus_valinta[1]
                    if tapahtuma.type == pygame.K_3:
                        self.vaikeus_valinta[2]
            teksti = fontti.render("Vaikeusaste", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 80))
            teksti = fontti.render("1 = Helppo", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 150))
            teksti = fontti.render("2 = Keskivaikea", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 200))
            teksti = fontti.render("3 = Vaikea", True, (0, 0, 0))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 250))

            pygame.display.flip()


    def lisaa_pelaaja(self):
        nimi = self.tekstiboxi("Anna pelaajan nimi:")
        pelaaja = Pelaaja(nimi)
        self.pelaajat.append(pelaaja)

        # Kysytään lisätäänkö pelaajia
        while True:
            lisaa_muita = self.tekstiboxi("Lisätäänkö toinen pelaaja? (k/e): ") 
            if lisaa_muita.lower() == "k":                                      
                self.pelaajat.append                                            
                nimi = self.tekstiboxi("Anna pelaajan nimi:")                   
            else:
                self.pelaa()                                                    


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

            naytto.blit(taustakuva, (0, 0))  
            syote_alue = fontti.render(viesti + teksti, True, (0, 0, 0))                            # Syötealue johon teksti tulee
            naytto.blit(syote_alue, (leveys // 2 - syote_alue.get_width() // 2, korkeus // 2))      # Syötealueen sijainti

            pygame.display.flip()
        
        return teksti

    def pelaa(self):
        while True:
            naytto.fill((0, 0, 0))
            naytto.blit(taustakuva, (0, 0))

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

    def arvaus(self):
        loytyi = False
        syote = input("Kirjain tai sana: ")
        if len(syote) == 1: # Jos annetaan yksi kirjain
            for i in range(len(self.oikea_vastaus)):
                if syote == self.arvattava_sana[i]:
                    continue
                if syote == self.oikea_vastaus[i]:
                    self.arvattava_sana[i] = syote
                    loytyi = True
            if loytyi == False:
                self.__vaarat_kirjaimet.append(syote)
        elif syote == self.oikea_vastaus: # Jos annettu enemmän kuin yksi kirjain ja vastaus on oikein
            loytyi = True

        return loytyi

    def vaarat_kirjaimet(self):
        return list(set(self.__vaarat_kirjaimet))  # Poistetaan mahdolliset duplikaatit ja palautetaan takaisin listana

hirsipuu = Hirsipuu()
hirsipuu.lisaa_pelaaja()

hirsipuu.pelaajat[0].lisaa_piste()
print(hirsipuu.pelaajat[0])

while True:
    for pelaaja in hirsipuu.pelaajat:
        print(pelaaja)
        print(hirsipuu)
        print(hirsipuu.vaarat_kirjaimet())
        arvaus = hirsipuu.arvaus()
        if arvaus:
            pelaaja.lisaa_piste()
