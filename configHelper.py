__author__ = 'siyuqiu'
import xml.etree.ElementTree as ET
tree = ET.parse('config')
root = tree.getroot()


# ACCESS_TOKEN = '3472190621-U5GkT9KetqgZt08TJuTXa7PSQWHuZH32r7FMyCr'
# ACCESS_SECRET = 'd9qYqlqqfuqHnDY8U8dsP22IOoJOStMwlpD0sy7nhz4jC'
# CONSUMER_KEY = 'AWFQMU6SQMuC4N2dGUS75uqXP'
# CONSUMER_SECRET = 'SQmziWxo5szZ4dAifDNJNkx2PIY7kSmhUmbdj610qzCuKKThfp'
class config:
    def __init__(self):
        self.accesstoken = root.find('ACCESS_TOKEN').text
        self.accessscecret = root.find('ACCESS_SECRET').text
        self.consumertoken = root.find('CONSUMER_KEY').text
        self.consumersecret = root.find('CONSUMER_SECRET').text
myconfig = config()