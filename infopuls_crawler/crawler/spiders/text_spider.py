import scrapy
import json
from w3lib.html import remove_tags


class TextSpider(scrapy.Spider):
    name = "text"

    def start_requests(self):
        urls = [
            'https://www.infopulse.com/services/software-engineering/'
            'mobile-application-development/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        results = []
        for i in range(1, 10):
            categories = response.xpath(
                '/html/body/main/div/div[3]/div[1]/div[1]/article/div[{}]'
                '/h4'.format(i)).extract()
            for category in categories:
                category = remove_tags(category.replace('&amp;', 'and'))
                texts = response.xpath(
                    '/html/body/main/div/div[3]/div[1]/div[1]/'
                    'article/div[{}]/ul/li'.format(i)).extract()
                results.append({'category': category, 'text': category})
                for text in texts:
                    if text:
                        results.append(
                            {'category': category, 'text': remove_tags(text)}
                        )
        categories = response.xpath(
            '/html/body/main/div/div[3]/div[1]/div[1]/article/h4/text()'
        ).extract()
        for category in categories:
            results.append({'category': category, 'text': category})
            headers = response.xpath(
                '/html/body/main/div/div[3]/div[1]/div[1]/article/h4/text()'
            ).extract()
            for header in headers:
                results.append({'category': category, 'text': header})
            for i in range(6, 11):
                text = response.xpath(
                    '/html/body/main/div/div[3]/div[1]/div[1]/article/'
                    'p[{}]/text()'.format(i)
                ).extract_first()
                results.append({'category': category, 'text': text})

        with open('mobile-development.json', 'w') as f:
            json.dump(results, f, ensure_ascii=False).encode('utf-8')
