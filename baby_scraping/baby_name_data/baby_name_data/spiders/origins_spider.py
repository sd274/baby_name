import scrapy


class NameOriginsSpider(scrapy.Spider):
    name = "name_origins"
    start_urls = [
        'https://www.behindthename.com/names',
    ]

    def parse(self, response):
        name_divs =response.xpath('//div[@class="browsename"]')
        for name_div in name_divs:
            name = name_div.xpath('span[@class="listname"]/a/text()').get()
            usage = name_div.xpath('span[@class="listusage"]/a')
            usage = [use.xpath('text()').get() for use in usage]


            yield {
                'name': name,
                'usage': usage
            }
        nav = response.xpath('//nav[@class="pagination"]')
        next_page = nav.xpath('a[contains(text(),"Next")]/@href').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)