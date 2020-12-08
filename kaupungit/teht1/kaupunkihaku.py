import sqlite3

# Tarkistin testaa tätä funktiota
def find_city_by_name(city_name, database):
    # Kirjoita ratkaisusi tähän funktioon.
    #
    # Avaa tietokanta 'database' ja etsi sieltä kaupunkia 'city_name'.
    # Palauta hakutuloksen kaupunki.
    # Jos haku palauttaa useamman kaupungin, palauta kaupunki, jossa on
    # suurin väkimäärä.
    return


# Tätä funktiota ei testata
# Voit lisätä tänne omia kokeiluja
def main():
    tietokanta = 'kaupungit.db'

    print("Ohjelma hakee kaupungin tietokannasta '{}'.".format(tietokanta))
    inputstring = input("Kaupungin nimi:")

    while inputstring != "":
        queryresult = find_city_by_name(inputstring, tietokanta)

        if queryresult:
            # Erotetaan queryresultin eri tietokentät
            dbid, city_name, region_name, country, population, lat, lon = queryresult

            print(city_name, ",", region_name, ",", country)
            print("Väkimäärä:", population)
            print("Koordinaatit: lat/lon", lat, "/", lon)

        else:
            print("Ei löytynyt")

        inputstring = input("Kaupungin nimi:")


# Tätä ei tarvitse muuttaa
if __name__ == "__main__":
    main()

# Tällaista ei tarvitse mihinkään
#main()
