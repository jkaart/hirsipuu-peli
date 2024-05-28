nelja_kirjainta = []
viisi_kirjainta = []
kuusi_kirjainta = []

def tarkista(sana: str):
    loytyi = False
    for kirjain in sana:
        if kirjain in "abcdefghijklmnopqrstuvwxyzåäö":
            loytyi = True
        else:
            loytyi = False
            break
    return loytyi

sanalista = "nykysuomensanalista2024.csv" # Löytyy osoitteesta https://www.kotus.fi/aineistot/sana-aineistot/nykysuomen_sanalista

with open(sanalista, encoding="utf-8") as tiedosto:
    for rivi in tiedosto:
        if "substantiivi" in rivi and not "substantiivi," in rivi:
            rivi = rivi.split('\t')
            rivi = rivi[0].replace(" ","")
            rivi = rivi.replace("\n","")
            
            if tarkista(rivi):
                print(rivi)
                if len(rivi) == 4:
                    nelja_kirjainta.append(rivi)
                if len(rivi) == 5:
                    viisi_kirjainta.append(rivi)
                if len(rivi) == 6:
                    kuusi_kirjainta.append(rivi)

nelja_kirjainta = set(nelja_kirjainta)
viisi_kirjainta = set(viisi_kirjainta)
kuusi_kirjainta = set(kuusi_kirjainta)

print("Nykysuomensanalista luettu")

with open("nelja_kirjainta.txt", "w", encoding="utf-8") as tiedosto:
    for sana in nelja_kirjainta:
        tiedosto.write(sana+"\n")

print("Tiedosto nelja_kirjainta.txt luotu")

with open("viisi_kirjainta.txt", "w", encoding="utf-8") as tiedosto:
    for sana in viisi_kirjainta:
        tiedosto.write(sana+"\n")

print("Tiedosto viisi_kirjainta.txt luotu")

with open("kuusi_kirjainta.txt", "w", encoding="utf-8") as tiedosto:
    for sana in kuusi_kirjainta:
        tiedosto.write(sana+"\n")

print("Tiedosto kuusi_kirjainta.txt luotu")
