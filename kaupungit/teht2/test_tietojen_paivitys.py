# -*- coding: utf-8 -*-
import contextlib
import os
import shutil
import sqlite3
import sys
import tempfile
import unittest

from tietojen_paivitys import paivita_tiedot


DATA_NAME = "suomen_suurimpien_kuntien_asukasluvut.txt"
DB_NAME = "kaupungit.db"
# ../kaupungit.db
DB_PATH = os.path.join(os.path.pardir, DB_NAME)


class TestTietojenPaivitys(unittest.TestCase):

    def setUp(self):
        self.db, self.db_path = tempfile.mkstemp("test_" + DB_NAME)
        shutil.copyfile(DB_PATH, self.db_path)
        with open(DATA_NAME) as f:
            f.readline()
            self.input_populations = dict(l.rstrip().split(";") for l in f)

    def connect_db(self):
        return contextlib.closing(sqlite3.connect(self.db_path))

    def current_row_count(self):
        with self.connect_db() as conn:
            return conn.execute("SELECT COUNT(*) FROM kaupungit").fetchone()[0]

    def finnish_cities_in_db(self):
        with self.connect_db() as conn:
            conn.row_factory = sqlite3.Row
            return conn.execute("SELECT * FROM kaupungit WHERE valtio=?", ("FINLAND", )).fetchall()

    def test1_row_count_is_unaltered(self):
        """Tietokannan rivien lukumäärä pysyy vakiona."""
        rows_before = self.current_row_count()
        paivita_tiedot(DATA_NAME, self.db_path)
        rows_after = self.current_row_count()
        self.assertEqual(
            rows_before,
            rows_after,
            "Ennen funktiosi kutsumista tietokannassa oli {} riviä, mutta kutsun jälkeen on {} riviä.".format(rows_before, rows_after))

    def test2_rows_with_updates_are_updated(self):
        """Funktio päivittää tietokantaan uuden asukasluvun suomalaisille kaupungeille, jotka on tekstitiedostossa."""
        populations_before = {row["nimi"]: row["populaatio"]
                              for row in self.finnish_cities_in_db()}
        paivita_tiedot(DATA_NAME, self.db_path)
        for row in self.finnish_cities_in_db():
            city_name = row["nimi"]
            if city_name not in self.input_populations:
                continue
            pop_before = populations_before[city_name]
            pop_now = row["populaatio"]
            expected_new_pop = int(self.input_populations[city_name])
            self.assertEqual(
                pop_now,
                expected_new_pop,
                "Kaupunki {} on tekstitiedostossa, mutta sen asukasluku tietokannassa ei ole sama kuin tekstitiedostossa.\n\n".format(city_name) +
                "Alkuperäinen asukasluku:\n{}\n".format(pop_before) +
                "Funktiokutsun jälkeen:\n{}\n".format(pop_now) +
                "Tekstitiedostossa:\n{}".format(expected_new_pop))

    def test3_rows_without_updates_are_not_updated(self):
        """Funktio ei päivitä suomalaisten kaupunkien asukaslukua, jos kaupunki ei ole tekstitiedostossa."""
        populations_before = {row["nimi"]: row["populaatio"]
                              for row in self.finnish_cities_in_db()}
        paivita_tiedot(DATA_NAME, self.db_path)
        for row in self.finnish_cities_in_db():
            city_name = row["nimi"]
            if city_name in self.input_populations:
                continue
            pop_before = populations_before[city_name]
            pop_now = row["populaatio"]
            self.assertEqual(
                pop_before,
                pop_now,
                "Kaupunkia {} ei löydy tekstitiedostosta, mutta sen asukasluku oli muuttunut.\n\n".format(city_name) +
                "Alkuperäinen asukasluku:\n{}\n".format(pop_before) +
                "Funktiokutsun jälkeen:\n{}".format(pop_now))

    def tearDown(self):
        os.close(self.db)
        os.remove(self.db_path)


if __name__ in ("__main__", "tests"):
    if not os.path.exists(DB_PATH):
        print("Tietokantaa ei löytynyt. Onko hakemistorakenne sama kuin zip-paketissa?")
        print("Testit olettavat, että tietokanta on yhtä tasoa ylempänä kuin testit (testitiedostosta katsottuna {})".format(DB_PATH))
        sys.exit(1)
    unittest.main(verbosity=2)
