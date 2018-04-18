#!/bin/bash

OUT="sendereihen.json"

[ -e $OUT ] && rm $OUT

scrapy runspider sendereihen.py --nolog -o $OUT
