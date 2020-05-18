import scrapy
import logging
import tldextract
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..urls import urls


allow_domains = list()
file_map = dict()
for url in urls:
    result = tldextract.extract(url)
    domain = result.domain
    suffix = result.suffix
    real_domain = domain+"."+suffix
    allow_domains.append(real_domain)
    file_map[real_domain] = open(domain + ".txt", "a")


link_extractor = LinkExtractor(allow_domains=allow_domains)
img_extractor = LinkExtractor(allow=allow_domains, deny_extensions=set(), tags=('img',), attrs=('src',), canonicalize=True, unique=True)
link_set = set()
img_set = set()
max_level = 30


class someSpider(CrawlSpider):
    name = 'img_dev'
    item = []
    user_agent = 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36'

    start_urls = urls  # ['http://www.poliform.it/']

    def parse(self, response):
        links = link_extractor.extract_links(response)
        img_links = img_extractor.extract_links(response)
        level = response.meta.get("level", 0)
        if level > max_level:
            return
        result = tldextract.extract(response.url)
        domain = result.domain
        suffix = result.suffix
        real_domain = domain + "." + suffix
        for link in links:
            url = link.url
            if url not in link_set:
                link_set.add(url)
                logging.info("level: %d" % (level, ) + url)
                yield scrapy.Request(url, callback=self.parse, meta={"level": level+1})
        for link in img_links:
            url = link.url
            if url not in img_set:
                img_set.add(url)
                logging.info(url)
                file = file_map[real_domain]
                file.write(url + "\n")
