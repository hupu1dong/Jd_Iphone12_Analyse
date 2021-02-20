# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import csv
import json
from kafka import KafkaProducer

from itemadapter import ItemAdapter


class JdIphone12AnalysePipelineToCsv:
    # 保存为csv格式
    def __init__(self):
        # 打开文件，指定方式为写，利用第3个参数把csv写数据时产生的空行消除
        self.f = open("Iphone12.csv", "a+", newline="")
        # 设置文件第一行的字段名，注意要跟spider传过来的字典key名称相同
        self.fieldnames = ["content", "id", "nickname", "productColor", "productId", "productSize", "score"]
        # 指定文件的写入方式为csv字典写入，参数1为指定具体文件，参数2为指定字段名
        self.writer = csv.DictWriter(self.f, fieldnames=self.fieldnames)
        # 写入第一行字段名，因为只要写入一次，所以文件放在__init__里面
        self.writer.writeheader()

    def process_item(self, item, spider):
        # 写入spider传过来的具体数值
        self.writer.writerow(item)
        # 写入完返回
        return item

    def close(self, spider):
        self.f.close()



class JsonPipeline(object):
    """生成json文件!"""
    def open_spider(self, spider):
        self.f = open('./Iphone12.json', 'a+')
    def process_item(self, item, spider):
        content = json.dumps(dict(item), ensure_ascii=False) + ',\n'
        self.f.write(content)  #python3
        return item
    def close_spider(self, spider):
        print ("{}:爬虫数据处理完毕!".format(spider.name))
        self.f.close()

class CommentPipelineToKafka(object):

    # 初始化函数，一般用作建立数据库连接
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='master:9092,node1:9092,node2:9092')

    # 输出据处理方法
    def process_item(self, item, spider):
        id = item["id"]  # 用户id
        productId = item["productId"]
        content = item['content']  # 评价内容
        score = item['score']  # 评分
        nickname = item['nickname']  # 昵称
        productColor = item['productColor']  # 颜色
        productSize = item['productSize']  # 内存大小

        line = "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (
            id, productId, score, nickname, productColor, productSize, content)
        # 数据打入kafka
        self.producer.send("jingdong_comment", line.encode('utf-8'))
        self.producer.flush()