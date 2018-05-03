#!/bin/bash

OUT="sendereihen.json"

[ -e $OUT ] && rm $OUT

source venv/bin/activate

scrapy runspider sendereihen.py --nolog -o $OUT
