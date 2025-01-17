from scrapy import Spider, Selector

from locations.items import GeojsonPointItem


class YettelBGSpider(Spider):
    name = "yettel_bg"
    item_attributes = {
        "brand": "Yettel",
        "brand_wikidata": "Q14915070",
        "country": "BG",
    }
    start_urls = ["https://www.yettel.bg/store-locator/json"]

    def parse(self, response):
        for store in response.json()["features"]:
            item = GeojsonPointItem()

            item["lon"], item["lat"] = store["geometry"]["coordinates"]

            item["ref"] = store["properties"]["title"]
            item["phone"] = store["properties"]["gsl_props_phone"]

            address_block = Selector(text=store["properties"]["gsl_addressfield"])

            item["street_address"] = address_block.xpath(
                '//div[@class="thoroughfare"]/text()'
            ).get()
            item["postcode"] = address_block.xpath(
                '//span[@class="postal-code"]/text()'
            ).get()
            item["city"] = address_block.xpath('//span[@class="locality"]/text()').get()

            yield item
