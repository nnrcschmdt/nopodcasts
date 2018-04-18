import json

import scrapy

with open('sendereihen.json') as f:
    sendereihen = json.load(f)


class SendungenSpider(scrapy.Spider):
    name = 'sendungen'
    allowed_domains = ['oe1.orf.at']
    start_urls = ['https://oe1.orf.at%s' % sendereihe['url'] for sendereihe in sendereihen]

    def parse(self, response):
        sendereihe = response.request.url.split('/')[-1]
        for sendung in response.css('div.accordionSubContent > div.accordionSubItem'):
            url = sendung.css('a.infoButton7Tage::attr(href)').extract_first()

            if url:
                yield dict(sendereihe=sendereihe, url='https://oe1.orf.at%s' % url)
