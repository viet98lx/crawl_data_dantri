import scrapy.spiders
import logging
import re

logger = logging.getLogger('mylogger')
logger.info("This is an information")

class News_spider(scrapy.Spider):
    name = "get_links_spider"
    allowed_domains = ["dantri.com.vn"]

    start_urls = ["https://dantri.com.vn/"]

    def parse(self, response):
        root_str = '/html/body/header/nav/div/ol/li[contains(@class, "dropdown dropdown--hover")]'
        list_header = response.xpath(root_str)
        # print(list_header)
        print(len(list_header))
        for item in list_header[2:19]:
            # print(item)
            # print("---------------------")
            # title = item.css("a").attrib['title']
            # print(title)
            link = item.css("a").attrib['href']
            # print(link)
            # print("---------------------")
            #     title = response.xpath(root_str + folder + "/@title").extract()
            #     print(title)
            #     print()
            next_url = response.urljoin(link)
            # print(next_url)
            yield scrapy.Request(next_url, callback=self.parse_level_2)

    def parse_level_2(self, response):
        list_links = []
        cater = response.xpath("/html/body/main/div/div/ul/li")
        # print(type(cater))
        # logger.debug(f"list link xpath : {cater}")
        for c in cater:
            # print(type(c))
            link = c.css("h2 > a").attrib['href']
            # print(f"link : {link}")
            list_links.append(link)
            next_url = response.urljoin(link)
            logger.debug(f"Next url : {next_url}")
            yield scrapy.Request(next_url, callback=self.parse_category)
        # pass
        # print(list_links)

    def parse_category(self, response):
        list_news = response.xpath("//div[contains(@class, 'container')]/div[contains(@class, 'clearfix')]/div[contains(@class, 'col')]/ul[contains(@class, 'dt-list')]/li")
        save_link_file = 'D://crawl_dantri//links_news.txt'
        logger.debug(f"Length of list news: {len(list_news)}")
        for new in list_news:
            # logger.debug(f"New element: {new}")
            if (not new.css("div.news-item > a").extract()):
                continue
            link_new = new.css("div.news-item > a").attrib['href']
            # print(link_new)
            logger.debug(f"link new: {link_new}")
            new_url = response.urljoin(link_new)
            with open(save_link_file, 'a') as f:
                f.write(new_url)
                f.write('\n')
                f.close()

        next_pages = response.xpath("//div[contains(@class, 'container')]/div[contains(@class, 'clearfix')]/div[contains(@class, 'col')]/ul[contains(@class, 'list-unstyled')]/li")
        next_url = response.urljoin(next_pages[-1].css("a").attrib['href'])
        print(next_url)
        logger.debug(f"Next pages url : {next_url}")
        yield scrapy.Request(next_url, callback=self.parse_category)