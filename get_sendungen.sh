#!/bin/bash

OUT="sendungen.json"

[ -e $OUT ] && rm $OUT

source venv/bin/activate

scrapy runspider sendungen.py --nolog -o $OUT
