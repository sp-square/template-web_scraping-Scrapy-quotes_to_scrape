import scrapy


class QuotesAllSpider(scrapy.Spider):
    name = 'quotes_all'
    allowed_domains = ['toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        # print a log message
        self.log('I just visited: ' + response.url)
        for quote in response.css('div.quote'):
            item = {
                'author_name': quote.css('small.author::text').extract_first(),
                'text': quote.css('span.text::text').extract_first(),
                'tags': quote.css('a.tag::text').extract()
            }
            yield item

        # follow pagination link
        next_page_relative_url = response.css(
            'li.next > a::attr(href)').extract_first()
        if next_page_relative_url:
            next_page_absolute_url = response.urljoin(next_page_relative_url)
            yield scrapy.Request(url=next_page_absolute_url, callback=self.parse)
