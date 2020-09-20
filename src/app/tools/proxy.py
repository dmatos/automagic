# coding=utf8

import requests
import random

from crawler.util.logger import logger
from crawler.tools import chrome_driver, firefox_driver
import crawler.config.application_config as app_config


class Proxy:

    def __init__(self):
        logger.info('initializing proxy service')
        self.proxy_ip = None
        self.proxy_port = None
        self.username = None
        self.password = None
        self.proxy_status = None

    def print_proxie_params(self):
        logger.info('proxy_ip: {}'.format(self.proxy_ip))
        logger.info('proxy_port: {}'.format(self.proxy_port))
        logger.info('username: {}'.format(self.username))
        logger.info('password: {}'.format(self.password))
        logger.info('proxy_status: {}'.format(self.proxy_status))

    def _initialize_random_proxy_01(self):
        proxies_url = app_config.proxy_url_01
        resp = requests.get(proxies_url)
        if resp.status_code != 200:
            # This means something went wrong.
            logger.error('GET /tasks/ {}'.format(resp.status_code))
        proxies_para_usar = []
        proxies_list = resp.json()
        for proxy_item in proxies_list:
            logger.debug('{0} {1} {2} {3} {4}'.format(
                proxy_item['proxy_ip'],
                proxy_item['proxy_port'],
                proxy_item['username'],
                proxy_item['password'],
                proxy_item['proxy_status']))
            if str(proxy_item['proxy_ip']).startswith('173'):
                proxies_para_usar.append(proxy_item)
            elif str(proxy_item['proxy_ip']).startswith('23'):
                proxies_para_usar.append(proxy_item)

        if len(proxies_para_usar) < 1:
            proxies_para_usar = proxies_list
        proxy_online = False
        tentativa = 0
        while not proxy_online and tentativa < len(proxies_para_usar):
            proxy_random_index = random.randint(0, len(proxies_para_usar)-1)
            self.proxy_ip = proxies_para_usar[proxy_random_index]['proxy_ip']
            self.proxy_port = proxies_para_usar[proxy_random_index]['proxy_port']
            self.username = proxies_para_usar[proxy_random_index]['username']
            self.password = proxies_para_usar[proxy_random_index]['password']
            self.proxy_status = proxies_para_usar[proxy_random_index]['proxy_status']
            if self.proxy_status == 'online':
                proxy_online = True
            tentativa += 1
        self.print_proxie_params()


    def _initialize_random_proxy_02(self):
        proxies_url = app_config.proxy_url_02
        resp = requests.get(proxies_url)
        if resp.status_code != 200:
            # This means something went wrong.
            logger.error('GET /tasks/ {}'.format(resp.status_code))
        proxies_list = resp.iter_lines()
        proxies_para_usar = []
        for proxy_row in proxies_list:
            logger.info(proxy_row.decode("utf-8"))
            proxie_configs = proxy_row.decode("utf-8").split(':')
            proxy_item = {'proxy_ip': proxie_configs[0], 'proxy_port': proxie_configs[1], 'username': proxie_configs[2],
                          'password': proxie_configs[3], 'proxy_status': 'online'}
            logger.debug('{0} {1} {2} {3} {4}'.format(
                proxy_item['proxy_ip'],
                proxy_item['proxy_port'],
                proxy_item['username'],
                proxy_item['password'],
                proxy_item['proxy_status']))
            proxies_para_usar.append(proxy_item)
        if len(proxies_para_usar) < 1:
            proxies_para_usar = proxies_list
        proxy_online = False
        tentativa = 0
        while not proxy_online and tentativa < len(proxies_para_usar):
            proxy_random_index = random.randint(0, len(proxies_para_usar)-1)
            self.proxy_ip = proxies_para_usar[proxy_random_index]['proxy_ip']
            self.proxy_port = proxies_para_usar[proxy_random_index]['proxy_port']
            self.username = proxies_para_usar[proxy_random_index]['username']
            self.password = proxies_para_usar[proxy_random_index]['password']
            self.proxy_status = proxies_para_usar[proxy_random_index]['proxy_status']
            if self.proxy_status == 'online':
                proxy_online = True
            tentativa += 1
        self.print_proxie_params()

    def get_driver(self, download_dir,  browser='firefox', headless=True):
        self._initialize_random_proxy_01()
        if browser == 'firefox':
            driver = firefox_driver.inicializar_driver(download_dir, headless=headless, proxy=self)
            return driver
        elif browser == 'chrome':
            driver = chrome_driver.inicializar_driver(download_dir, headless=headless, proxy=self)
            return driver
        else:
            logger.info('nenhum browser selencionado...')
            return None


