# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JdIphone12AnalyseItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
class Comments(scrapy.Item):
    id = scrapy.Field()  # 用户id
    productId = scrapy.Field()
    content = scrapy.Field()  # 评价内容
    score = scrapy.Field() # 评分
    nickname = scrapy.Field()  # 昵称
    productColor = scrapy.Field()  # 颜色
    productSize = scrapy.Field()  # 内存大小
