import sqlite3

#Tata funktiota ei testata
def paivita_tiedot(tiedostonimi, tietokanta):
    # Yhdistetaan tietokantaan
    conn = sqlite3.connect(tietokanta)
    # Text factory korjaa mahdollisia merkistokoodausongelmia, ei tarvitse valittaa
    conn.text_factory = str
    # Tehdaan tietokantakursori
    c = conn.cursor()

    # Avataan tiedosto, josta luetaan uusia kaupunkeja
    with open(tiedostonimi, encoding="utf-8") as f_in:

        # Luetaan otsakkeen yli
        f_in.readline()

        try:
            # Luetaan rivit yksi kerrallaan
            for line in f_in.readlines():
                #Paivita tiedot
                pass
            # Tallennetaan tehdyt muutokset tietokantaan
            conn.commit()

        finally:
            conn.close()

#Tata funktiota ei testata
#Voit lisata omia kokeiluja
def main():
    tiedostonimi = "suomen_suurimpien_kuntien_asukasluvut.txt"
    tietokanta = 'kaupungit.db'
    print("Kokeillaan paivittaa tiedostosta '{}' asukasluvut tietokantaan '{}':".format(tiedostonimi, tietokanta))
    paivita_tiedot(tiedostonimi, tietokanta)



# Tata ei tarvitse muuttaa
if __name__ == "__main__":
    main()
