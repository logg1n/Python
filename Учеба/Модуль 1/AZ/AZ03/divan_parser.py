"""
    3. Необходимо спарсить цены на диваны с сайта divan.ru в csv файл,
     обработать данные, найти среднюю цену и вывести ее,
     а также сделать гистограмму цен на диваны​
"""

import scrapy
from urllib.parse import urljoin
from scrapy.crawler import CrawlerProcess


class DivannewparsSpider(scrapy.Spider):
    name = "divannewpars"

    def __init__(self, start_url=None, *args, **kwargs):
        super(DivannewparsSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.kwargs = kwargs

    def parse(self, response):
        divans = response.css(self.kwargs["items"])
        print(len(divans))

        for divan in divans:
            print("Вхождение")

            relative_url = divan.css('a::attr(href)').get()
            absolute_url = urljoin(response.url, relative_url)

            print(absolute_url)

            name = divan.css(self.kwargs["name"]).get()
            price = int(divan.css(self.kwargs["price"]).get())

            if not all([name, price, absolute_url]):
                continue

            item = {
                "name": name,
                "price": price,
                "url": absolute_url
            }

            yield item

            # Проверяем есть ли кнопка "следующая страница"
            if response.css('a.PaginationLink:contains("›"), a.PaginationLink'):
                current_page = response.meta.get('page', 1)
                yield response.follow(
                    f"{url}/page-{current_page + 1}",
                    callback=self.parse,
                    meta={'page': current_page + 1}
                )


if __name__ == '__main__':
    url = 'https://www.divan.ru/category/divany'
    #url = input("Введите URL категории (divan.ru): ").strip()

    # Проверка URL
    if not url.startswith(('http://', 'https://')):
        url = f'https://divan.ru{url}' if url.startswith('/') else f'https://divan.ru/category/{url}'

    path = f"{url.split('/')[-1]}.csv"
    print(path)

    process = CrawlerProcess(settings={
        'FEED_FORMAT': 'csv',
        'FEED_URI': path,
        'FEED_EXPORT_ENCODING': 'utf-8-sig',
        'FEED_EXPORT_FIELDS': ['name', 'price', 'url'],
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOAD_DELAY': 5,
        'LOG_ENABLED': False,
        'ROBOTSTXT_OBEY': True
    })

    process.crawl(
        DivannewparsSpider,
        start_url=url,
        items="div.WdR1o",
        name='a.ActiveProduct span[itemprop="name"]::text',
        price='meta[itemprop="price"]::attr(content)'
    )
    print(f"\nСтарт парсинга {url}...\n")
    process.start()
