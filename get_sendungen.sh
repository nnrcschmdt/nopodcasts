#!/bin/bash

OUT="sendungen.json"

[ -e $OUT ] && rm $OUT

scrapy runspider sendungen.py --nolog -o $OUT
