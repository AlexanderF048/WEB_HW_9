import json
from pathlib import Path
import scrapy
from scrapy import Item, Field
from scrapy.crawler import CrawlerProcess
from itemadapter import ItemAdapter


class QuotesScrapy(Item):
    tags = Field()
    author = Field()
    quote = Field()


class AuthorsScrapy(Item):
    fullname = Field()
    born_date = Field()
    born_location = Field()
    description = Field()


class SpiderPipeline(object):  # Т.к. две структуры данных собираем в одном спайдере необходимо их собрать!
    authors = []
    quotes = []



    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        if 'tags' in adapter.keys():
            self.quotes.append(
                {
                    'tags': adapter['tags'],
                    'author': adapter['author'],
                    'quote': adapter['quote']
                }
            )
        if 'fullname' in adapter.keys():
            self.authors.append(
                {
                    'fullname': adapter['fullname'],
                    'born_date': adapter['born_date'],
                    'born_location': adapter['born_location'],
                    'description': adapter['description']
                }
            )
        return item

    def close_spider(self, spider):
        with open(Path(__file__).parent.parent.parent.parent.joinpath('authors.json'), 'w', encoding='utf-8') as fh:
            json.dump(self.authors, fh, ensure_ascii=False)
        with open(Path(__file__).parent.parent.parent.parent.joinpath('quotes.json'), 'w', encoding='utf-8') as fh:
            json.dump(self.quotes, fh, ensure_ascii=False)


class MainSpiderSpider(scrapy.Spider):
    name = 'main_spider'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']
    custom_settings = {
        'ITEM_PIPELINES': {
            SpiderPipeline: 300
        }
    }

    def parse(self, response):
        for quotes in response.xpath("/html//div[@class='quote']"):
            tags = quotes.xpath("div[@class='tags']/a[@class='tag']/text()").extract()
            author = quotes.xpath("span/small[@class='author']/text()").get().strip()
            quote = quotes.xpath("span[@class='text']/text()").get().strip()
            yield QuotesScrapy(tags=tags, author=author, quote=quote)

        for authors in response.xpath("/html//div[@class='quote']"):
            yield response.follow(url=self.start_urls[0] + authors.xpath("span/a/@href").get(),
                                  callback=self.parse_authors)

        next_page = response.xpath("/html//li[@class='next']/a/@href").get()
        if next_page:
            yield scrapy.Request(url=self.start_urls[0] + next_page)

    def parse_authors(self, response):

        author_page_content = response.xpath("/html//div[@class='author-details']")
        fullname = author_page_content.xpath("h3[@class='author-title']/text()").get().strip()
        born_date = author_page_content.xpath("p/span[@class='author-born-date']/text()").get().strip()
        born_location = author_page_content.xpath("p/span[@class='author-born-location']/text()").get().strip()
        description = author_page_content.xpath("div[@class='author-description']/text()").get().strip()
        yield AuthorsScrapy(fullname=fullname, born_date=born_date, born_location=born_location,
                            description=description)


if __name__ == "__main__":
    process = CrawlerProcess()
    process.crawl(MainSpiderSpider)
    process.start()
