# -*- coding: utf-8 -*-
import os.path
import sys
import unittest

from matka import matka, hae_kaupunki


DB_NAME = "kaupungit.db"
# ../kaupungit.db
DB_PATH = os.path.join(os.path.pardir, DB_NAME)


class TestMatka(unittest.TestCase):

    def setUp(self):
        # Testdata with precalculated distances.
        self.data = [
            (('Acultzingo', 'Veracruz-Llave', 'MEXICO', 5801, 18.716667, -97.316667),
             ('Clonakilty', 'Cork', 'IRELAND', 4065, 51.6230556, -8.8705556),
             8282.27029484201),

            (('Amsterdam', 'Noord-Holland', 'NETHERLANDS', 745811, 52.35, 4.916667),
             ('Teplyk', "Vinnyts'ka Oblast'", 'UKRAINE', 6604, 48.665658, 29.745035),
             1793.3351423353665),

            (('Safotu', None, 'SAMOA', 1207, -13.45, -172.4),
             ('Oxford', 'Oxfordshire', 'UNITED KINGDOM', 154567, 51.75, -1.25),
             15683.163263741253)
        ]

    def test1_matka_returns_float(self):
        """Funktio matka palauttaa etäisyyden liukulukuna."""
        returned_distance = matka(0.0, 0.0, 1.0, 1.0)
        self.assertIsInstance(
            returned_distance,
            float,
            "Funktion matka palauttama etäisyys pitäisi olla tyyppiä {}, ei {}.".format(float, type(returned_distance)))

    def test2_distance_between_two_cities(self):
        """Funktio matka laskee kahden kaupungin etäisyyden oikein."""
        accuracy = 3
        for city1, city2, distance in self.data:
            returned_distance = matka(city1[4], city1[5], city2[4], city2[5])
            self.assertAlmostEqual(
                returned_distance,
                distance,
                accuracy,
                "Etäisyys alla olevien kaupunkien välillä pitäisi olla {} desimaalin tarkkuudella {:.4f}, mutta funktiosi palautti {:.4f}."
                .format(accuracy, distance, returned_distance) + "\n\n"
                + str(tuple(city1)) + "\n" + str(tuple(city2)))

    def test3_hae_kaupunki_returns_tuple(self):
        """Funktio hae_kaupunki palauttaa tietokannan rivin."""
        city_name = self.data[0][0][0]
        returned_city = hae_kaupunki(city_name, DB_PATH)
        self.assertIsNotNone(
            returned_city,
            "Funktiolle hae_kaupunki annettiin parametrina {}, mutta funktio palautti None."
            .format(city_name))
        self.assertEqual(
            len(returned_city),
            7,
            "Funktiolle hae_kaupunki annettiin parametrina {} ja funktion pitäisi palauttaa yksi tietokannan rivi, jossa on 7 arvoa, ei {}."
            .format(city_name, len(returned_city)) + "\n\n" +
            "Funktio palautti rivin:\n{}".format(returned_city))

    def test4_hae_kaupunki_returns_city_with_largest_population(self):
        """Funktio hae_kaupunki palauttaa kaupungin, jossa on annetulla nimella suurin asukasluku."""
        def assert_city(city):
            city_name = city[0]
            returned_city = hae_kaupunki(city_name, DB_PATH)
            self.assertEqual(
                returned_city[1],
                city_name,
                "Funktiolle hae_kaupunki annettiin parametrina {}, mutta funktio palautti:\n\n{}"
                .format(city_name, returned_city))
            city_population = city[3]
            self.assertEqual(
                returned_city[1:],
                city,
                "Funktiolle hae_kaupunki annettiin parametrina {}."
                .format(city_name) + "\n\n" +
                "Funktion olisi pitänyt palauttaa kaupunki nimeltä {}, jolla on asukasluku {}, mutta funktio palautti alla olevan rivin."
                .format(city_name, city_population) + "\n\n{}".format(returned_city))

        for city1, city2, _ in self.data:
            assert_city(city1)
            assert_city(city2)


if __name__ in ("__main__", "tests"):
    if not os.path.exists(DB_PATH):
        print("Tietokantaa ei löytynyt. Onko hakemistorakenne sama kuin zip-paketissa?")
        print("Testit olettavat, että tietokanta on yhtä tasoa ylempänä kuin testit (testitiedostosta katsottuna {})".format(DB_PATH))
        sys.exit(1)
    unittest.main(verbosity=2)

