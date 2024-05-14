import random

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

    def uusi_peli(self):
        pass
    
    def lisaa_pelaaja(self):
        nimi = input("Anna pelaajan nimi: ")
        pelaaja = Pelaaja(nimi)

        #pelaaja.uusi_pelaaja()
        self.pelaajat.append(pelaaja)

hirsipuu = Hirsipuu()
hirsipuu.lisaa_pelaaja()

hirsipuu.pelaajat[0].lisaa_piste()
print(hirsipuu.pelaajat[0])
