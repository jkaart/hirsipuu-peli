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
        self.sanalista = ["auto","pallo"]
        self.oikea_vastaus = ""
        self.arvattava_sana = ""
        self.uusi_peli()
    
    def __str__(self) -> str:
        return " ".join(self.arvattava_sana)

    def uusi_peli(self):
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

hirsipuu = Hirsipuu()
hirsipuu.lisaa_pelaaja()

while True:
    for pelaaja in hirsipuu.pelaajat:
        print(pelaaja)
        print(hirsipuu)
        arvaus = hirsipuu.arvaus()
        if arvaus:
            pelaaja.lisaa_piste()
