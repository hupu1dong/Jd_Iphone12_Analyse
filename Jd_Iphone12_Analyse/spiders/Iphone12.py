import js2xml
import scrapy
import re
import json

from bs4 import BeautifulSoup
from lxml import etree

from Jd_Iphone12_Analyse.items import Comments

"""
定义网络爬虫类
"""

class ItcastSpider(scrapy.Spider):
    name = "Iphone"
    start_urls = "https://item.jd.com/100016034394.html"

    """
    人口方法，当爬虫启动后会先执行这个方法
    """
    def start_requests(self):
        yield scrapy.Request(url=self.start_urls,callback=self.parse)

    def parse(self, response):
        # html --> xml对象
        soup = BeautifulSoup(response.text, 'lxml')
        # 选择script标签
        src = soup.select("html head script")[0].string
        # js --》xml文档对象
        src_text = js2xml.parse(src, debug=False)
        # xml --》html文档对象
        src_tree = js2xml.pretty_print(src_text)
        selector = etree.HTML(src_tree)

        # 使用html xpath 查找标签
        name = selector.xpath("//property[@name='name']/string/text()")
        # print(name)
        for obj in selector.xpath("//property[@name='colorSize']/array/object"):
            # ./从当前路径开始寻址
            id = obj.xpath("./property/number/@value")[0]
            # PriceUrl = "https://p.3.cn/prices/mgets?callback=jQuery9151994&type=1&area=14_1180_1182_0&pdtk=&pduid=70067091689641793&pdpin=&pin=&pdbp=0&skuIds=J_J_%s%2CJ_100016034428%2CJ_899777%2CJ_3494451%2CJ_10025606692694%2CJ_100009477910%2CJ_72307637968%2CJ_100004325476%2CJ_10021425217424%2CJ_72307504732%2CJ_68752491808&ext=11100000&source=item-pc" % id
            # yield scrapy.Request(url=url, callback=self.parse_Price, dont_filter=True)
            for page in range(20,50):
                url = "https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=%s&score=0&sortType=5&page=%s&pageSize=10&isShadowSku=0&rid=0&fold=1" % (id,page)
                yield scrapy.Request(url=url, callback=self.parse_Comment, dont_filter=True)

    def parse_Comment(self,response):
        p = re.compile(r'[(](.*)[)]', re.S)  # 贪婪匹配
        # 匹配之后返回一个数组
        r = re.findall(p, response.text)
        content = json.loads(r[0])
        productId = content["productCommentSummary"]["productId"]
        # 获取评价列表
        comments = content["comments"]
        for commet in comments:
            item = Comments()

            id = commet["id"] #用户id
            productId = productId
            content = commet['content'] #评价内容
            score = commet['score']#评分
            nickname = commet['nickname'] #昵称
            productColor = commet['productColor'] #颜色
            productSize = commet['productSize'] #内存大小

            item['id'] = id
            item['productId'] = productId
            item['content'] = content
            item['score'] = score
            item['nickname'] = nickname
            item['productColor'] = productColor
            item['productSize'] = productSize
            
            yield item

