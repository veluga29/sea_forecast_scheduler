import os
import sys
from celery import Celery
from celery.schedules import crontab
from scrapy import signals
from scrapy.crawler import Crawler
from twisted.internet import reactor
from scrapy.utils.project import get_project_settings
# from multiprocessing import Process
from billiard import Process

from beach_forecast_scraper.spiders.forecast_spider import ForecastSpider
from config import BROKER_SERVER

# Add current path for windows
# sys.path.append(os.path.dirname(__file__))

app = Celery("tasks", broker=BROKER_SERVER)

app.conf.beat_schedule = {
    'run_scraper_task-every-hour': {
        'task': 'tasks.run_scraper_task',
        'schedule': crontab(),
    },
}
app.conf.timezone = 'Asia/Seoul'


def run_scrapy():
    crawler = Crawler(ForecastSpider, settings=get_project_settings())
    crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
    crawler.crawl()
    reactor.run()


@app.task
def run_scraper_task():
    p = Process(target=run_scrapy)
    p.start()
    p.join()
