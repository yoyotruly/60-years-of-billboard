import requests
import scrapy
from scrapy.http import TextResponse
from scrapy.crawler import CrawlerProcess

# Define spider for scraping song titles
class TitleSpider(scrapy.Spider):

    name = 'title_spider'
    
    def start_requests(self):
        urls = ['https://www.billboard.com/charts/pop-songs/2019-01-12']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)
    
    def parse(self, response):
        res = response.css('.chart-number-one__title, .chart-list-item__title-text').css('::text')
        titles = [t.strip() for t in res.extract()]
        return titles

# Define spider for scraping available lyrics avaiable on billboard.com
class LyricsSpider(scrapy.Spider):
    
    name = 'lyrics_spider'
    
    def start_requests(self):
        urls = ['https://www.billboard.com/charts/pop-songs/2019-01-12']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse_links)
    
    def parse_links(self, response):
        res = response.css('.chart-number-one__lyrics a , .chart-list-item__lyrics a').xpath('./@href')
        links = res.extract()
        for link in links:
            yield response.follow(url=link, callback=self.parse_lyrics)
    
    def parse_lyrics(self, response):
        headline = response.css('.article__headline::text').extract_first()
        lyrics = response.css('p:nth-child(1)::text').extract()
        lyrics_dict[headline] = lyrics

lyrics_dict = dict()

# Start crawlers
process = CrawlerProcess()
process.crawl(TitleSpider)
process.crawl(LyricsSpider)
process.start()
