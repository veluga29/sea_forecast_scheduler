# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import psycopg2
import json
from datetime import datetime

from config import POSTGRES_SERVER, POSTGRES_USER, POSTGRES_PASSWORD, POSTGRES_DB

class PostgreSQLPipeline(object):

    def open_spider(self, spider):
        hostname = POSTGRES_SERVER
        username = POSTGRES_USER
        password = POSTGRES_PASSWORD 
        database = POSTGRES_DB
        try:
            self.connection = psycopg2.connect(host=hostname, user=username, password=password, dbname=database)
            self.cur = self.connection.cursor()
        except Exception as e:
            print(e)

    def close_spider(self, spider):
        self.cur.close()
        self.connection.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute("select * from beachforecastlist where beach_id = %s", [item['beach_id']])
            row = self.cur.fetchall()
            if not row:
                self.cur.execute("insert into beachforecastlist(create_dt, update_dt, beach, region, ocean, beach_id, live_info, forecast_info) values(%s,%s,%s,%s,%s,%s,%s,%s)",(
                    datetime.now(), datetime.now(), 
                    item['beach'], item['region'],
                    item['ocean'],item['beach_id'],
                    json.dumps(item['live_info']),
                    json.dumps(item['forecast_info'])
                    )
                )
            else:
                self.cur.execute("update beachforecastlist set update_dt = %s, live_info = %s, forecast_info = %s where beach_id = %s", (
                    datetime.now(), 
                    json.dumps(item['live_info']),
                    json.dumps(item['forecast_info']),
                    item['beach_id']
                    )
                )
            self.cur.execute("insert into beachforecastlisthistory(create_dt, update_dt, beach, region, ocean, beach_id, live_info, forecast_info) values(%s,%s,%s,%s,%s,%s,%s,%s)",(
                datetime.now(), datetime.now(), 
                item['beach'], item['region'],
                item['ocean'],item['beach_id'],
                json.dumps(item['live_info']),
                json.dumps(item['forecast_info'])
                )
            )
            
            self.connection.commit()
        except Exception as e:
            print(e)
        finally:
            return item


# JSON pipeline
# from itemadapter import ItemAdapter
# from scrapy.exporters import JsonItemExporter


# class JsonPipeline(object):
#     def __init__(self):
#         self.file = open("assets/beach_forecast.json", "wb")
#         self.exporter = JsonItemExporter(self.file, encoding="utf-8")
#         self.exporter.start_exporting()

#     def close_spider(self, spider):
#         self.exporter.finish_exporting()
#         self.file.close()

#     def process_item(self, item, spider):
#         self.exporter.export_item(item)
#         return item
