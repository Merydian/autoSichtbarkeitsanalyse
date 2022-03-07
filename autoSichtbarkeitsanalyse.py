import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import urllib.request
import urllib.parse
import zipfile

class autoSbkA:
    def __init__(self, name, gemeinden):
        self.name = name
        self.kreise = gemeinden
        self.path = os.getcwd() + '/' + self.name
        self.dgmPath = self.path + '/dgm'
        self.domPath = self.path + '/dom'

        self.download_dom(kreise=self.kreise)
        self.extract_zips(self.domPath)
        self.download_dgm(kreise=self.kreise)
        self.extract_zips(self.dgmPath)

    def download_dgm(self, kreise):
        driver = webdriver.Firefox()
        driver.get(
            "https://gds.hessen.de/INTERSHOP/web/WFS/HLBG-Geodaten-Site/de_DE/-/EUR/ViewSearch-Start?customerGroup=PFC_BENUTZERTYP_GEWERBEKUNDE&topic=PFC_THEMENGEBIET_3D_DATEN")

        showDownloads = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.facet__item--no-border')))
        showDownloads.click()

        produktname = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                  'li.subnav__list-item:nth-child(1) > div:nth-child(1) > button:nth-child(1) > svg:nth-child(1)')))
        produktname.click()

        dgm1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#collapse-Produktname > div:nth-child(3) > label:nth-child(2)')))
        dgm1.click()

        filterAnwenden = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.facet__action:nth-child(6) > a:nth-child(1)')))
        filterAnwenden.click()

        for i in range(22):
            for kreis in kreise:
                list = driver.find_elements_by_class_name('content-box')
                time.sleep(1)
                x = [i for i in list if kreis in i.get_attribute('innerHTML')]
                try:
                    html = x[0].get_attribute('innerHTML')
                    link = html.split('"')[11]
                    x = html.split('\n')[3]
                    name = x.replace(' ', '') + '.zip'
                    url_link = 'https://gds.hessen.de' + urllib.parse.quote(link)
                    print('Downloading: ' + url_link)
                    urllib.request.urlretrieve(url_link, name)

                except:
                    continue
            driver.find_element_by_xpath("//*[contains(text(), 'weiter')]").click()

        driver.close()

    def download_dom(self, kreise):
        driver = webdriver.Firefox()
        driver.get(
            "https://gds.hessen.de/INTERSHOP/web/WFS/HLBG-Geodaten-Site/de_DE/-/EUR/ViewSearch-Start?customerGroup=PFC_BENUTZERTYP_GEWERBEKUNDE&topic=PFC_THEMENGEBIET_3D_DATEN")

        showDownloads = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, '.facet__item--no-border')))
        showDownloads.click()

        produktname = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,
                                                                                  'li.subnav__list-item:nth-child(1) > div:nth-child(1) > button:nth-child(1) > svg:nth-child(1)')))
        produktname.click()

        dom1 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#collapse-Produktname > div:nth-child(4) > label:nth-child(2)')))
        dom1.click()

        filterAnwenden = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.facet__action:nth-child(6) > a:nth-child(1)')))
        filterAnwenden.click()

        for i in range(22):
            for kreis in kreise:
                list = driver.find_elements_by_class_name('content-box')
                time.sleep(1)
                x = [i for i in list if kreis in i.get_attribute('innerHTML')]
                try:
                    html = x[0].get_attribute('innerHTML')
                    link = html.split('"')[11]
                    x = html.split('\n')[3]
                    name = x.replace(' ', '') + '.zip'
                    url_link = 'https://gds.hessen.de' + urllib.parse.quote(link)
                    print('Downloading: ' + url_link)
                    urllib.request.urlretrieve(url_link, name)

                except:
                    continue
            driver.find_element_by_xpath("//*[contains(text(), 'weiter')]").click()

        driver.close()

    def extract_zips(self, path):
        print('extracting...')
        files = []
        for file in os.listdir(os.getcwd()):
            if file.endswith(".zip"):
                files.append(os.path.join(os.getcwd(), file))

        for file in files:
            with zipfile.ZipFile(file, 'r') as zip_ref:
                zip_ref.extractall(path)
            os.remove(file)


if __name__ == '__main__':
    name = 'try'
    x = autoSbkA(name=name, gemeinden=['Bad Nauheim', 'Münzenberg', 'Rockenberg', 'Wölfersheim'])

