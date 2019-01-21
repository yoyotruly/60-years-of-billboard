import scrapy
from scrapy.crawler import CrawlerProcess


class ChartSpider(scrapy.Spider):
    name = 'chart_spider'
    start_urls = ['https://www.billboard.com/charts/pop-songs']

    def parse(self, response):
        # scrape artists and titles
        artist_top = response.css('.chart-number-one__artist a::text')
        title_top = response.css('.chart-number-one__title::text')
        artist_rest = response.css('.chart-list-item::attr(data-artist)')
        title_rest = response.css('.chart-list-item::attr(data-title)')
        chart = {
            'artist': [artist_top.extract_first().strip()]
                      + artist_rest.extract(),
            'title': title_top.extract()
                     + title_rest.extract()
        }
        yield chart

        # follow link of available lyrics
        lyrics_urls = response.css('.chart-list-item__lyrics a::attr(href)').extract()
        for url in lyrics_urls:
            yield scrapy.Request(url, self.parse_lyrics)

    def parse_lyrics(self, response):
        headline = response.css('.article__headline::text')
        lyrics = response.css('p:nth-child(1)::text')
        lyrics = {
            'headline': headline.extract(),
            'lyrics': lyrics.extract()[:-3]
        }
        yield lyrics

# Start crawlers
process = CrawlerProcess()
process.crawl(ChartSpider)
process.start()
