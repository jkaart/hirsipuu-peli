import pygame
import random

pygame.init()

#asetukset
leveys = 800
korkeus = 600
naytto = pygame.display.set_mode((leveys, korkeus))
pygame.display.set_caption("Hirsipuu")
fontti = pygame.font.SysFont("Arial", 24)

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
        self.oikea_vastaus = ""
        self.arvattava_sana = ""
        self.uusi_peli()

    def __str__(self) -> str:
        return " ".join(self.arvattava_sana)

    def uusi_peli(self):
        pass
        self.oikea_vastaus = self.uusi_sana()
        self.arvattava_sana = list("_" * len(self.oikea_vastaus))

    def lisaa_pelaaja(self):
        nimi = input("Anna pelaajan nimi: ")
        pelaaja = Pelaaja(nimi)
        #pelaaja.uusi_pelaaja()
        self.pelaajat.append(pelaaja)

    def uusi_sana(self):
        return random.choice(self.sanalista)

    def arvaus(self):
        try:
            syote = input("Kirjain tai sana: ")
            if len(syote) == 1:
                i = self.oikea_vastaus.index(syote)

                self.arvattava_sana[i] = syote
                if syote in self.arvattava_sana:
                    return True
                else:
                    if syote == self.oikea_vastaus:
                        print("löytyi koko sana!")
                    print("Ei löytynyt")
        except ValueError:
            print("ei löytynyt")


naytto.fill((50, 50, 50))

teksti = fontti.render("HIRSIPUU", True, (255, 255, 255))
naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 50))

pygame.display.flip()


def pelaa():
    while True:
        for tapahtuma in pygame.event.get():
            if tapahtuma.type == pygame.KEYDOWN:
                if tapahtuma.key == pygame.K_F1:
                    hirsipuu.uusi_peli()
                if tapahtuma.key == pygame.K_F2:
                    hirsipuu.lisaa_pelaaja()
                if tapahtuma.type == pygame.QUIT:
                    return

        pygame.display.flip()

        #Päivitetään näyttö
        naytto.fill((50, 50, 50))
        teksti = fontti.render("HIRSIPUU", True, (255, 255, 255))
        naytto.blit(teksti, (leveys // 2 - teksti.get_width() // 2, 50))
        pygame.display.flip()
        pygame.time.delay(10)

hirsipuu = Hirsipuu()
hirsipuu.lisaa_pelaaja()

hirsipuu.pelaajat[0].lisaa_piste()
print(hirsipuu.pelaajat[0])
while True:
    for pelaaja in hirsipuu.pelaajat:
        print(pelaaja)
        print(hirsipuu)
        arvaus = hirsipuu.arvaus()
        if arvaus:
            pelaaja.lisaa_piste()