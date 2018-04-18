import scrapy


class SendereihenSpider(scrapy.Spider):
    name = 'sendereihen'
    allowed_domains = ['oe1.orf.at']
    start_urls = ['https://oe1.orf.at/selection/581856?page=%s' % page for page in range(1, 11)]

    def parse(self, response):
        for sendereihe in response.css('div.listItem'):
            url = sendereihe.css('a::attr(href)').extract_first()
            name = sendereihe.css('div.content > h2::text').extract_first()

            yield dict(url=url, name=name)
