nopodcasts
==========

``nopodcasts`` ist eine sehr einfache Möglichkeit, für sich persönlich aus den
aktuell vorhandenen Sendungen im 7-Tage-Archiv von Ö1, regelmäßig Sendungen
herunterzuladen und bereit zu stellen.  Die Sendungen können dann lokal am
Web-Browser angehört werden.

Diese erste Version verzichtet auf eine Datenbank und besteht aus zwei
Komponenten, Scrapy_ und Flask_ die untereinander über JSON-Dateien
kommunizieren.  youtube-dl_ wird verwendet, um die Sendugen herunterzuladen.

Installation
------------

Am besten installiert man das ganze Projekt in eine virtuellen Umgebung:::

    $ git clone https://github.com/nnrcschmdt/nopodcasts
    $ cd nopodcasts
    $ python3 -m venv venv
    $ source venv/bin/activate
    (venv) $ pip install -r requests

Verwendung
----------

Als erstes wird der Spider ``sendereihen`` aufgerufen, um eine Liste der
Sendereihen zu erhalten.  Die Liste wird als JSON-Datei direkt in das aktuelle
Verzeichnis exportiert.::

    (venv) $ ./get_sendereihen.sh

Dann wird die Liste ``sendereihen.json`` von der Web-Applikation verwendet, um
zu fragen welche Sendereihen heruntergeladen werden sollen und um die
Verzeichnisstruktur unter ``sendungen`` zu erzeugen, wo sie abegelgt werden.
Die gekürzte Liste der Sendereihen, wird in das aktuelle Verzeichnis
abgelegt.::

    (venv) $ export FLASK_APP=app.py
    (venv) $ ./import_sendereihen.sh

Der Spider ``sendungen`` wird dann aufgerufen, um die Liste der vorhandenen
Sendungen zu erhalten.  Die Liste wird, wieder als JSON-Datei, in das
aktuelle Verzeichnis exportiert.::

    (venv) $ cd ../scrapy
    (venv) $ ./get_sendungen.sh

Dann wird die Liste ``sendungen.json`` von der Web-Applikation verwendet, um
die einzelnen Sendungen (mit Hilfe von ``youtube-dl``) herunter zu laden.::

    (venv) $ ./download_sendungen.sh

Die Web-Applikation enthält dann alle Sendungen, die für die jeweilige
Sendereihen herunter geladen wurden und am Web-Browser angehört werden
können.::

    (venv) $ flask run
     * Serving Flask app "app"
     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)

Die Aufrufe vor ``get_sendungen.sh`` und ``download_sendungen.sh`` können dann
täglich wiederholt werden.

.. _Scrapy: https://scrapy.org/
.. _Flask: http://flask.pocoo.org/
.. _youtube-dl: https://rg3.github.io/youtube-dl/
