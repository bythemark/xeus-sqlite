SQL
===

Pääkysymys:
    Miten hallita SQL-tietokantaa Python-ohjelmasta?

Mitä käsitellään?
    SQLite modulia.
    
Mitä sinun oletetaan tekevän?
    Lue ohjeet ja tee tehtävät.

Suuntaa antava vaativuusarvio:
    Helpohko.

Suuntaa antava työläysarvio:
    2-3 tuntia.

Ohjelmointitehtävät:
    Tehtävät ja niiden testit löytyvät omista hakemistoistaan. 
    
Yleistä
-------
   
Demografia
..........

Kaikissa tehtävissä käytetään alla olevaa tietokantaa, johon on ladattu suuri määrä maailman kaupunkeja ja niiden asukasmääriä ja koordinaatteja. Tietokannassa on vain yksi taulu, jonka tietueet kuvaavat maailman kaupunkeja.

Tietokannan rakenne
...................

Ennen tehtävien aloittamista kannattaa tutkia tietokannan tietoja. Missä muodossa kaupunkien ja valtioiden nimet on annettu?

+----------------------------------------------------+
|  .. code-block:: sql                               |
|                                                    |
|    TABLE kaupungit                                 |
|                                                    |
|        id           integer primary key            |
|                                                    |
|        nimi         text                           |
|                                                    |
|        alue         text                           |
|                                                    |
|        valtio       text                           |
|                                                    |
|        populaatio   integer                        |
|                                                    |
|        lat          real                           |
|                                                    |
|        lon	        real                         |
|                                                    |
+----------------------------------------------------+


Ohjeet
------

Itsenäinen tiedon haku
......................

SQL on paljon laajempi kyselykieli kuin mitä tällä kurssilla on mahdollista syvällisemmin käydä läpi.
Harjoitukissa on kuitenkin tarkoitus saada yleiskuva kielen laajuudesta ja opetella ongelmanratkaisua.
Siksi tällä kierroksella on tehtäviä, joihin tulee etsiä
oikeat komennot itse ja joita ei pikaoppaastamme löydy.
Käytä esim. jo aikaisemmin mainittua referenssimanuaalia,
joka löytyy osoitteesta `w3schools.com <http://www.w3schools.com/sql/default.asp>`__.

Vihjeitä
........

Jos seuraavissa tehtävissä konsoliin tulostuu virheilmoitus,

  .. figure:: kuvat/SQL_python_virhe.png

jossa kerrotaan, että tietokantaa tai jotain taulua ei löydy,
kannattaa antaa main()-funktion *tietokanta*-muuttujaan koko tiedostopolku, jossa tietokanta sijaitsee.

  .. figure:: kuvat/SQL_python_korjaus.png


Toinen vaihtoehto on siirtää tietokanta samaan kansioon kuin ajettava python-tiedosto.

Tietokanta luodaan automaattisesti, jos sitä ei löydy. Tietokanta on tällöin tyhjä, joten vaikka näyttäisi siltä, että
tietokanta on oikeassa paikassa, se ei toimi.

  .. figure:: kuvat/tyhja_tietokanta.png

SQL-komennon palauttamat tietueet talteen
.........................................

Suoritettuasi esimerkiksi komennon

.. code-block:: python

  c.execute("""SELECT * FROM kaupungit;""")

Saat komennon palauttaman ensimmäisen tietueen talteen komennolla

.. code-block:: python

  tietue = c.fetchone()

Saat kaikki komennon palauttamat tietueet talteen komennolla

.. code-block:: python

  tietueet = c.fetchall()  #palauttaa kaikki c.excecute()-komennon palauttamat tietueet listana


Tehtävä 1: Kaupunkihaku
-----------------------

Täydennä Python-ohjelmaa ``kaupunkihaku.py``, joka etsii
tietokannasta nimen perusteella kaupungin ja tulostaa sen nimen,
alueen, valtion, asukasmäärän sekä koordinaatit. Lue olemassa oleva koodi ja
sen kommentointi ennen kuin alat kirjoittaa ratkaisua.

Huomaa, että kaupungin nimellä hakiessa voi tulla useita tuloksia.
Tällöin halutaan se kaupunki, jossa on eniten asukkaita. Helpoin tapa
valita väkimäärän perusteella on lisätä hakukomentoon
``ORDER BY populaatio DESC`` eli järjestä laskevasti väkimäärän
mukaan. Tällöin suurin kaupunki on listassa ensimmäinen.

Merkistöistä
............

Ennen seuraavan tehtävän aloittamista kannattaa tutkia tehtäväpaketin mukana tulleita tiedostoja.
Mitä `merkistöä <https://fi.wikipedia.org/wiki/Merkist%C3%B6>`_ esimerkiksi `tekstitiedosto <https://fi.wikipedia.org/wiki/Tekstitiedosto>`_ kaupungit.txt käyttää?
Ongelmien välttämiseksi tiedoston avaamisen yhteyteen on syytä lisätä tieto käytetystä merkistöstä.
Python 3:ssa se onnistuu lisäämällä määre **encoding** esimerkiksi seuraavasti

.. code-block:: python

  f = open(filename, 'r', encoding='utf-8')

Tehtävä 2: Tietojen päivittäminen
---------------------------------

Tehtäväpaketin mukana tulee tiedosto *suomen_suurimpien_kuntien_asukasluvut.txt*, jossa on listattuna Suomen suurimpien kuntien asukaslukuja.
Tehtävänäsi on tiedostoa hyödyntämällä päivittää kaupunkien asukasluvut. Jos tiedostossa olevaa kaupunkia ei löydy tietokannasta, ohita kyseinen kaupunki.
Älä kuitenkaan luo uutta kaupunkia tietokantaan. 

Tehtävä 3: Kahden kaupungin etäisyys
------------------------------------

Tee Python-ohjelma, joka etsii kaksi kaupunkia tietokannasta
nimen perusteella ja laskee niiden välisen etäisyyden. Voit käyttää
apunasi viidennessä tehtävässä tekemääsi kaupunkihakua. (Säilytä
kuitenkin toimiva kopio tehtävästä 5 tarkistusta varten!) Huomioi jälleen,
että samannimisistä kaupungeista halutaan se, jolla on suurin asukasluku.

**Vihje.** \ Etäisyys koordinaattien välillä kannattaa laskea
isoympyrän kulman avulla. Pisteiden ``(lon1,lat1)`` ja
``(lon2,lat2)`` väliselle etäisyydelle saadaan seuraavat yhtälöt, jos
Maapallon säde on R. Muista pohtia, oletko käyttämässä radiaaneja vai
asteita. Käytä ratkaisussasi math-kirjaston funktioita, tarkistin ei
hyväksy numpyä.

**Huom.** Älä kopioi kaavoja suoraan, sillä mukaan tulee ylimääräisiä `tulostumattomia merkkejä <https://fi.wikipedia.org/wiki/Tulostumaton_merkki>`_,
jolloin python-tulkki valittaa `syntax-errorista <https://docs.python.org/3.6/library/exceptions.html#SyntaxError>`_.

.. math::

   \\frac{ \sum_{t=0}^{N}f(t,k) }{N}

Kulma isoympyrällä:

.. math::
  \alpha = \arccos(\sin(lat1) * \sin(lat2) + \cos(lat1) * cos(lat2) * cos(lon2-lon1))

Etäisyys isoympyrällä:

.. math::

  b = \alpha * R



Miten voin testata tehtävien toimivuutta?

#. Etsi SQLite DB Browserilla joku kaupunki tietokannasta ja tutki löytääkö ohjelma sen.

#. Tietojen päivittämisen jälkeen tutki SQLite DB Browserilla ovatko tiedot päivittyneet tietokantaan.

#. Laske esimerkiksi laskimella oikea tulos ja vertaa sitä ohjelmasi palauttamaan tulokseen.
