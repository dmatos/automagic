# coding=utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from seleniumwire import webdriver as wirewebdriver
import os
import zipfile

from app.util.logger import logger

def _get_manifest_json():
    manifest_json = """
    {
        "version": "1.0.0",
        "manifest_version": 2,
        "name": "Chrome Proxy",
        "permissions": [
            "proxy",
            "tabs",
            "unlimitedStorage",
            "storage",
            "<all_urls>",
            "webRequest",
            "webRequestBlocking"
        ],
        "background": {
            "scripts": ["background.js"]
        },
        "minimum_chrome_version":"22.0.0"
    }
    """
    return manifest_json

def _get_background_js(proxy_ip, proxy_port, proxy_user, proxy_password):
    background_js = """
    var config = {
            mode: "fixed_servers",
            rules: {
            singleProxy: {
                scheme: "http",
                host: "%s",
                port: parseInt(%s)
            },
            bypassList: ["localhost"]
            }
        };
    
    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});
    
    function callbackFn(details) {
        return {
            authCredentials: {
                username: "%s",
                password: "%s"
            }
        };
    }
    
    chrome.webRequest.onAuthRequired.addListener(
                callbackFn,
                {urls: ["<all_urls>"]},
                ['blocking']
    );
    """ % (proxy_ip, proxy_port, proxy_user, proxy_password)
    return background_js



def inicializar_driver(download_dir, headless=True, proxy=None):
    try:
        os.makedirs(download_dir)
    except FileExistsError:
        pass

    options = webdriver.ChromeOptions()
    if headless:
         options.add_argument('headless')
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument('--window-size=1920,1080')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_experimental_option('prefs', {
        "download.default_directory": download_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

    driver_path = os.path.join(os.getcwd(), 'resources/chromedriver')

    driver = None
    if proxy is None:
        driver = webdriver.Chrome(executable_path=driver_path, chrome_options=options)
    else:
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
        driver = wirewebdriver.Chrome(executable_path=driver_path, chrome_options=options, seleniumwire_options=wire_options)
        driver.scopes = [
            'none'
        ]
    if headless:
        params = {'behavior': 'allow', 'downloadPath': download_dir}
        driver.execute_cdp_cmd('Page.setDownloadBehavior', params)
    driver.set_window_size(1024, 768)
    return driver


if __name__=='__main__':
    driver = inicializar_driver('resources/downloads')
    driver.get('https://www.google.com')
    body = driver.find_element(By.TAG_NAME, 'body')
    logger.info(body.get_attribute('innerHTML'))

