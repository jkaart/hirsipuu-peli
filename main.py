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
        self.__vaarat_kirjaimet = []
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

while True:
    for pelaaja in hirsipuu.pelaajat:
        print(pelaaja)
        print(hirsipuu)
        print(hirsipuu.vaarat_kirjaimet())
        arvaus = hirsipuu.arvaus()
        if arvaus:
            pelaaja.lisaa_piste()
