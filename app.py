import contextlib
import glob
import os
import re
from datetime import datetime, timedelta

import youtube_dl
from flask import Flask, render_template, json, send_from_directory

app = Flask(__name__)


@contextlib.contextmanager
def chdir(path):
    cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(cwd)


@app.route('/', methods=['GET'])
def get_sendungen():
    sendereihen = {}

    with chdir('sendungen'):
        verzeichnisse = [element for element in glob.glob('*') if os.path.isdir(element)]

    verzeichnisse.sort()

    for verzeichnis in verzeichnisse:
        with chdir('sendungen/%s' % verzeichnis):
            dateienamen = glob.glob('*.mp3')

            sendungen = []

            for dateiname in dateienamen:
                match = re.match(r'(?P<titel>\S.+)-(?P<datum>\d{4}-\d{2}-\d{2})_(?P<hh>\d{2})(?P<mm>\d{2})\w*', dateiname)
                if match:
                    titel = match.group('titel')
                    datum = match.group('datum')
                    hh = match.group('hh')
                    mm = match.group('mm')
                    datum_uhrzeit = datetime.strptime('%s %s:%s' % (datum, hh, mm), '%Y-%m-%d %H:%M')
                    if datetime.now() - datum_uhrzeit < timedelta(days=7):
                        sendungen.append(
                            {'titel': titel, 'datum_uhrzeit': datum_uhrzeit.strftime('%d.%m.%Y %H:%M'), 'datei': dateiname})
                    else:
                        os.remove(dateiname)

            sendungen.sort(key=lambda s: s['datum_uhrzeit'])

        if len(sendungen) > 0:
            sendereihen[verzeichnis] = reversed(sendungen)

    return render_template('sendungen.html', sendereihen=sendereihen)


@app.route('/<string:sendereihe>/<path:filename>', methods=['GET'])
def get_sendung(sendereihe, filename):
    return send_from_directory('sendungen/%s' % sendereihe, filename)


@app.cli.command()
def import_sendereihen():
    """Sendereihen aus Scrapy Ergebnissen importieren."""
    with open("sendereihen.json") as f_in:
        sendereihen_in = json.load(f_in)
        sendereihen_in.sort(key=lambda s: s['name'])

        sendereihen_out = []

        if not os.path.exists('sendungen'):
            os.makedirs('sendungen')

        for sendereihe in sendereihen_in:
            if input('"%s" herunter laden? (j/N) ' % sendereihe['name']) == 'j':
                sendereihen_out.append(sendereihe)
                if not os.path.exists('sendungen%s' % sendereihe['url']):
                    os.makedirs('sendungen%s' % sendereihe['url'])

    with open("sendereihen.json", 'w') as f_out:
        f_out.write(json.dumps(sendereihen_out))


@app.cli.command()
def download_sendungen():
    """Sendungen aus Scrapy Ergebnissen downloaden"""
    with open("sendungen.json") as f:
        sendungen_in = json.load(f)
        sendungen_in.sort(key=lambda s: s['sendereihe'])

        with chdir('sendungen'):
            options = {'quiet': False, 'download_archive': 'sendungen.txt'}

            with youtube_dl.YoutubeDL(options) as youtubeDL:
                for sendung in sendungen_in:
                    with chdir(sendung['sendereihe']):
                        youtubeDL.download([sendung['url']])
