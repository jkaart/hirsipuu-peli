import pygame
import random
 
pygame.init()
 
#asetukset
leveys = 800
korkeus = 600
naytto = pygame.display.set_mode((leveys, korkeus))
fontti = pygame.font.SysFont("Arial", 24)
taustakuva = pygame.image.load("tausta.jpg")
hirsipuu_kuvat = [pygame.image.load("Hangman-0.png"), pygame.image.load("Hangman-1.png"), pygame.image.load("Hangman-2.png"), pygame.image.load("Hangman-3.png"), pygame.image.load("Hangman-4.png"), pygame.image.load("Hangman-5.png"), pygame.image.load("Hangman-6.png")]
 
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
        self.vaikeus = 4
#        self.pelaa()
        self.__vaarat_kirjaimet = []
        self.uusi_peli()
    
    def __str__(self) -> str:
        return " ".join(self.arvattava_sana)

    def vaikeusaste(self, pituus: int):
        for sana in self.sanalista:
            if len(sana) == pituus:
                self.kaytettavat_sanat.append(sana)

    def uusi_peli(self):
        self.vaikeusaste(self.vaikeus)
        self.oikea_vastaus = self.uusi_sana()
        self.arvattava_sana = list("_" * len(self.oikea_vastaus))
    
    def lisaa_pelaaja(self):
        nimi = input("Anna pelaajan nimi: ")
        pelaaja = Pelaaja(nimi)
        self.pelaajat.append(pelaaja)

    def pelaa(self):
        while True:
            naytto.fill((0, 0, 0))
            naytto.blit(taustakuva, (0, 0))
        
            # Aloitusnäyttö
            teksti = fontti.render("HIRSIPUU", True, (255, 255, 255))
            naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 50))
            teksti2 = fontti.render("F1 - Uusi peli", True, (255, 255, 255))    # F1 - Uusi peli
            naytto.blit(teksti2, (leveys // 2 - teksti2.get_width() // 2, 100)) 
            teksti3 = fontti.render("F2 - Lisää pelaaja", True, (255, 255, 255)) # F2 - Lisää pelaaja
            naytto.blit(teksti3, (leveys // 2 - teksti3.get_width() // 2, 150))
            teksti4 = fontti.render("ESC - Lopeta", True, (255, 255, 255))       # ESC - Lopeta
            naytto.blit(teksti4, (leveys // 2 - teksti4.get_width() // 2, 200))
 
            pygame.display.flip()
            pygame.time.delay(10)
 
            for tapahtuma in pygame.event.get():
                if tapahtuma.type == pygame.KEYDOWN:
                    if tapahtuma.key == pygame.K_F1:
                        self.uusi_peli()
                    if tapahtuma.key == pygame.K_F2:
                        self.lisaa_pelaaja()
                    if tapahtuma.key == pygame.K_ESCAPE:
                        pygame.quit()
                    if tapahtuma.type == pygame.QUIT:
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
        return list(set(self.__vaarat_kirjaimet)) # Poistetaan mahdolliset duplikaatit ja palautetaan takaisin listana

hirsipuu = Hirsipuu()
hirsipuu.lisaa_pelaaja()
 
#hirsipuu.pelaajat[0].lisaa_piste()
#print(hirsipuu.pelaajat[0])

while True:
    for pelaaja in hirsipuu.pelaajat:
        print(pelaaja)
        print(hirsipuu)
        print(hirsipuu.vaarat_kirjaimet())
        arvaus = hirsipuu.arvaus()
        if arvaus:
            pelaaja.lisaa_piste()
