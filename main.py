import random

class Pelaaja:
    def __init__(self, nimi: str) -> None:
        self.nimi = nimi
        

    def uusi_pelaaja(self):
        pass
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
