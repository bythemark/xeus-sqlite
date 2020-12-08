import sqlite3
import math


# Tarkistin testaa tätä funktiota
# 1. Toteuta funktio matka
def matka(lat1, lon1, lat2, lon2):
    # Maapallon säde kilometreissä
    R = 6371.0
    # Laske ja palauta etäisyys pisteiden (lat1, lon1) ja (lat2, lon2) välillä
    return


# Tarkistin testaa tätä funktiota
# 2. Toteuta funktio hae_kaupunki
def hae_kaupunki(nimi, tietokanta):
    # Hae tietokannasta 'tietokanta' kaupunkia nimeltä 'nimi' ja palauta löytynyt tietokannan rivi
    return


# Tätä funktiota ei testata
# Voit lisätä tänne omia kokeiluja
def main():
    tietokanta = 'kaupungit.db'

    print("Ohjelma hakee tietokannasta '{}' kaksi kaupunkia ja laskee niiden etäisyyden.\n".format(tietokanta))

    inputstring1 = input("Ensimmäisen kaupungin nimi:")
    inputstring2 = input("Toisen kaupungin nimi:")

    queryresult1 = hae_kaupunki(inputstring1, tietokanta)
    queryresult2 = hae_kaupunki(inputstring2, tietokanta)

    if queryresult1 and queryresult2:
        _, nimi1, _, _, _, lat1, lon1 = queryresult1
        _, nimi2, _, _, _, lat2, lon2 = queryresult2

        matkan_pituus = matka(lat1, lon1, lat2, lon2)
        print(nimi1, lat1, lon1)
        print(nimi2, lat2, lon2)
        print("Etäisyys", nimi1, "ja", nimi2, "välillä on", matkan_pituus, "km.")

    else:
        print("Ei löytynyt")


# Tätä ei tarvitse muuttaa
if __name__ == "__main__":
    main()

# Tällaista ei tarvitse mihinkään
#main()
