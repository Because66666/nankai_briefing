from init import app,sch,logger
from flask_apscheduler import APScheduler
from function_models.教务处 import run as dean
from function_models.数学科学学院 import run as math
from function_models.南开大学 import run as nk
from function_models.南开大学新闻网 import run as nk_news
from function_models.统计与数据科学学院 import run as statistics
from function_models.网络安全学院 import run as internet_safety
from function_models.商学院 import run as  business
from function_models.文学院 import run as wen




@sch.task("cron", id="dean",day='*',hour='*',minute='0',second='0',misfire_grace_time=600)
def run1():
    with sch.app.app_context():
        logger.info('执行教务处爬取')
        try:
            dean()
        except Exception as e:
            logger.error(e)

@sch.task("cron", id="math",day='*',hour='*',minute='0',second='0',misfire_grace_time=600)
def run1():
    with sch.app.app_context():
        logger.info('执行数院爬取')
        try:
            math()
        except Exception as e:
            logger.error(e)

@sch.task("cron", id="nk",day='*',hour='*',minute='0',second='0',misfire_grace_time=600)
def run1():
    with sch.app.app_context():
        logger.info('执行南开大学官网爬取')
        try:
            nk()
        except Exception as e:
            logger.error(e)

@sch.task("cron", id="nk_news",day='*',hour='*',minute='0',second='0',misfire_grace_time=600)
def run1():
    with sch.app.app_context():
        logger.info('执行南开大学新闻网爬取')
        try:
            nk_news()
        except Exception as e:
            logger.error(e)

@sch.task("cron", id="statistics",day='*',hour='*',minute='0',second='0',misfire_grace_time=600)
def run1():
    with sch.app.app_context():
        logger.info('执行统院爬取')
        try:
            statistics()
        except Exception as e:
            logger.error(e)

@sch.task("cron", id="internet_safety",day='*',hour='*',minute='0',second='0',misfire_grace_time=600)
def run1():
    with sch.app.app_context():
        logger.info('执行网安院爬取')
        try:
            internet_safety()
        except Exception as e:
            logger.error(e)

@sch.task("cron", id="business",day='*',hour='*',minute='0',second='0',misfire_grace_time=600)
def run1():
    with sch.app.app_context():
        logger.info('执行商学院爬取')
        try:
            business()
        except Exception as e:
            logger.error(e)

@sch.task("cron", id="wen",day='*',hour='*',minute='0',second='0',misfire_grace_time=600)
def run1():
    with sch.app.app_context():
        logger.info('执行文学院爬取')
        try:
            wen()
        except Exception as e:
            logger.error(e)