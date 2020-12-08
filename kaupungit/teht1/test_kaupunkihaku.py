# -*- coding: utf-8 -*-
import unittest
import os
import sqlite3
import tempfile

from kaupunkihaku import find_city_by_name


INIT_DB_SCRIPT = (
"""DROP TABLE IF EXISTS kaupungit;
CREATE TABLE kaupungit (
  id         INTEGER PRIMARY KEY,
  nimi       TEXT,
  alue       TEXT,
  valtio     TEXT,
  populaatio INTEGER,
  lat        REAL,
  lon        REAL
);""")


class TestKaupunkihaku(unittest.TestCase):

    def setUp(self):
        self.db, self.db_path = tempfile.mkstemp("testing.db")
        self.connection = sqlite3.connect(self.db_path)
        self.connection.executescript(INIT_DB_SCRIPT)
        self.connection.commit()

    def insert_into_database(self, values):
        query = "INSERT INTO kaupungit VALUES (?, ?, ?, ?, ?, ?, ?)"
        self.connection.execute(query, values)
        self.connection.commit()

    def dump_database(self):
        return ("Tietokannassa oli seuraavat rivit:\n\n" +
                "\n".join(str(tuple(row)) for row in self.connection.execute("SELECT * FROM kaupungit")))


    def test1_nonexisting_city(self):
        """Funktio palauttaa None jos funktiota kutsutaan kaupungin nimellä, jota ei ole olemassa."""
        # Tässä vaiheessa tietokanta on vielä tyhjä.
        city_name = "Helsinki"
        returned_answer = find_city_by_name(city_name, self.db_path)
        self.assertIsNone(
            returned_answer,
            "Tietokannasta pyydettiin kaupunkia nimellä '{}'.".format(city_name) +
            " Funktion olisi pitänyt palauttaa None mutta se palautti {}".format(returned_answer) + "\n\n" + self.dump_database())

        # Lisätään vaikka Tukholma.
        city_data = (1, 'Stockholm', 'Stockholms Lan', 'SWEDEN', 1253309, 59.333333, 18.05)
        self.insert_into_database(city_data)

        # Tietokannasta ei pitäisi vieläkään löytyä Helsinkiä.
        returned_answer = find_city_by_name(city_name, self.db_path)
        self.assertIsNone(
            returned_answer,
            "Tietokannasta pyydettiin kaupunkia nimellä '{}'.".format(city_name) +
            " Funktion olisi pitänyt palauttaa None mutta se palautti {}".format(returned_answer) + "\n\n" + self.dump_database())


    def test2_one_existing_city(self):
        """Funktio palauttaa yhden kaupungin jos funktiota kutsutaan kaupungin nimellä, joita on olemassa vain yksi."""
        # Lisätään tällä kertaa Helsinki.
        city_data = (1, 'Helsinki', 'Southern Finland', 'FINLAND', 558457, 60.175556, 24.934167)
        self.insert_into_database(city_data)

        # Nyt tietokannasta pitäisi löytyä Helsinki.
        city_name = city_data[1]
        returned_answer = find_city_by_name(city_name, self.db_path)
        assert_msg = ("Tietokannasta pyydettiin kaupunkia nimellä '{0}'. Funktion olisi pitänyt palauttaa {1} mutta se palautti {2}.".format(city_name, city_data, returned_answer) + "\n\n" + self.dump_database())

        self.assertIsNotNone(returned_answer, assert_msg)
        self.assertTupleEqual(returned_answer, city_data, assert_msg)


    def test3_several_existing_cities(self):
        """Funktio palauttaa yhden kaupungin jolla on muihin samannimisiin kaupunkeihin verrattuna suurin väkimäärä."""
        # Lisätään muutama Oxford.
        cities_data = (
            (1, 'Oxford', 'Auckland', 'NEW ZEALAND', 1776, -43.3, 172.183333),
            (2, 'Oxford', 'Oxfordshire', 'UNITED KINGDOM', 154567, 51.75, -1.25),
            (3, 'Oxford', 'Alabama', 'UNITED STATES', 16058, 33.6141667, -85.835)
        )
        for city_data in cities_data:
            self.insert_into_database(city_data)

        city_name = cities_data[0][1]

        returned_answer = find_city_by_name(city_name, self.db_path)
        expected_answer = max(cities_data, key=lambda city_data: city_data[4])
        assert_msg = ("Tietokannasta pyydettiin kaupunkia nimellä '{0}'. Funktion olisi pitänyt palauttaa {1} mutta se palautti {2}.".format(city_name, expected_answer, returned_answer) + "\n\n" + self.dump_database())

        self.assertIsNotNone(returned_answer, assert_msg)
        self.assertTupleEqual(returned_answer, expected_answer, assert_msg)


    def tearDown(self):
        self.connection.close()
        os.close(self.db)
        os.remove(self.db_path)


if __name__ in ("__main__", "tests"):
    unittest.main(verbosity=2)

