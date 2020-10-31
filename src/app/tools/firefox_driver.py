# coding=utf8

import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver as wirewebdriver

from app.util import logger

class FirefoxDriver:

    def __init__(self):
        pass

    def inicializar_driver(download_dir, headless=True, proxy=None):
        try:
            os.makedirs(download_dir)
        except FileExistsError:
            pass
        options = webdriver.firefox.options.Options()
        if headless:
            options.headless = True
        options.set_preference('dom.webdriver.enabled', False)
        driver_path = os.path.join(os.getcwd(), 'resources/geckodriver')
        profile_path = os.path.join(os.getcwd(), 'resources/firefox_perfil/')

        profile = webdriver.FirefoxProfile(profile_path)
        user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
        profile.set_preference("general.useragent.override", user_agent)
        profile.set_preference('browser.download.folderList', 2)
        profile.set_preference('browser.download.manager.showWhenStarting', False)
        profile.set_preference('browser.download.dir', download_dir)
        profile.set_preference('browser.helperApps.neverAsk.saveToDisk', 'application/csv,application/force-download,application/pdf,application/x-gzip,text/csv,text/plain')
        profile.set_preference("pdfjs.disabled", True)
        profile.set_preference("places.history.enabled", False)
        profile.set_preference("privacy.clearOnShutdown.offlineApps", True)
        profile.set_preference("privacy.clearOnShutdown.passwords", True)
        profile.set_preference("privacy.clearOnShutdown.siteSettings", True)
        profile.set_preference("privacy.sanitize.sanitizeOnShutdown", True)
        profile.set_preference("signon.rememberSignons", True)
        profile.set_preference("network.cookie.lifetimePolicy", 2)
        profile.set_preference("network.dns.disablePrefetch", True)
        profile.set_preference("network.http.sendRefererHeader", 0)

        driver = None

        if proxy is not None:
            logger.info("Configurando proxy para geckodriver")
            '''
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", proxy.proxy_ip)
            profile.set_preference("network.proxy.http_port", int(proxy.proxy_port))
            profile.set_preference("network.negotiate-auth.allow-proxies", False)
            profile.set_preference("network.automatic-ntlm-auth.allow-proxies", False)
            '''
            profile.update_preferences()
            wire_options = {
                #'verify_ssl': False,
                'connection_timeout': None,
                'proxy': {
                    'http': 'http://{0}:{1}@{2}:{3}'.format(
                        proxy.username,
                        proxy.password,
                        proxy.proxy_ip,
                        proxy.proxy_port,
                    ),
                    'https': 'https://{0}:{1}@{2}:{3}'.format(
                        proxy.username,
                        proxy.password,
                        proxy.proxy_ip,
                        proxy.proxy_port,
                    ),
                    'no_proxy': 'localhost,127.0.0.1,dev_server:8080'
                }
            }
            driver = wirewebdriver.Firefox(
                firefox_profile=profile,
                executable_path=driver_path,
                options=options,
                seleniumwire_options=wire_options
            )
            driver.scopes = [
                'none'
            ]

        else:
            profile.update_preferences()
            driver = webdriver.Firefox(firefox_profile=profile, executable_path=driver_path, options=options)


        driver.maximize_window()
        return driver


if __name__ == '__main__':
    firefox_driver = FirefoxDriver()
    driver = firefox_driver.inicializar_driver('/opt/oito/crawler-projudi/crawler_projudi_repo/')
    driver.get('https://www.google.com')
    body = driver.find_element(By.TAG_NAME, 'body')
    logger.info(body.get_attribute('innerHTML'))