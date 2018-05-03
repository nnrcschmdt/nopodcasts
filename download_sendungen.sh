#!/bin/bash

source venv/bin/activate

FLASK_APP=app.py flask download_sendungen
