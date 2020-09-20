# coding=utf8

from app.util.logger import logger
from app.tools import chrome_driver, firefox_driver

class AppService:

    def __init__(self):
        print('App inicializado')

    def inicializar_driver(self, headless=True, browser='chrome'):
        if browser == 'chrome':
            return chrome_driver.inicializar_driver(self.download_dir, headless)
        elif browser == 'firefox':
            return firefox_driver.inicializar_driver(self.download_dir, headless)
        else:
            # chrome by default
            return chrome_driver.inicializar_driver(self.download_dir, headless)