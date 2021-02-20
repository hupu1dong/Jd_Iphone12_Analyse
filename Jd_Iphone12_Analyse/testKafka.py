from kafka import KafkaProducer
import time

# 格式化成2016-03-20 11:45:39形式
Ntime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

"""
192.168.130.10 master
192.168.130.11 node1
192.168.130.12 node2
"""
producer = KafkaProducer(bootstrap_servers='master:9092,node1:9092,node2:9092')
# producer = KafkaProducer(bootstrap_servers='master:9092,node1:9092,node2:9092')

# producer.send("topic",b"hello bitch on kafka")
# producer.send("topic",bytes(Ntime.encode("UTF-8")))
# producer.send("topic",b"hello bitch on kafka I'm from pycharm")
producer.send("topic",bytes(("大傻逼").encode("UTF-8")))

producer.flush()
