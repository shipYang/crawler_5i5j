# -*- coding: utf-8 -*-

import mysql.connector
import uuid
import re
import datetime

def extract_num(str_value):
    return re.findall(r'\d.\d+', str_value)

def extract_integer(str_value):
    return re.findall(r'\d+', str_value)

class Crawler5I5JPipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='zhaoyang', passwd='Zhaoyang2017@qq.com', db='python',
                                    host='123.56.69.13', port=3306,charset='utf8', use_unicode=True)
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):

        id = str(uuid.uuid1())
        domain = '5i5j'

        try:
            self.cursor.execute("""replace into real_estate_copy (id,domain,title,housing_estate,price_num,address,rooms,floorage,decoration_situation,price_unit_num,floor,orientation,house_code,term,year,create_time)
                                                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s,%s,%s,%s,%s,%s)""",
                                (
                                    id,
                                    domain,
                                    item['title'],
                                    item['housing_estate'],
                                    item['price_num'],
                                    item['address'],
                                    item['rooms'],
                                    item['floorage'],
                                    item['decoration_situation'],
                                    item['price_unit_num'],
                                    item['floor'],
                                    item['orientation'],
                                    item['house_code'],
                                    item['term'],
                                    item['year'],
                                    datetime.datetime.now())

                                )

            self.conn.commit()


        except mysql.connector.Error as e:

            print ("error")

        return item








