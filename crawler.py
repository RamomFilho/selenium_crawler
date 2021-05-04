from json import dumps
from time import time
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


class SeniorUp(object):
    def __init__(self):
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--headless")
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--log-level=3")
        self.chrome_options.add_argument("--disable-gpu")
        self.chrome_options.add_argument("--start-maximized")
        self.chrome_options.add_argument("--disable-infobars")
        self.chrome_options.add_argument("--disable-extensions")
        self.chrome_options.add_argument("--disable-dev-shm-usage")
        self.chrome_options.add_argument("user-agent=Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0)")
        self.driver = webdriver.Remote("http://127.0.0.1:4444/wd/hub",
                                       desired_capabilities=self.chrome_options.to_capabilities())

    def open_browser(self):
        self.driver.set_page_load_timeout(60)
        self.driver.get("https://www.freeproxylists.net/")

    def first_page(self):
        proxies_list = list()
        for _ in range(0, 7):
            print(f'Page Number: {_ + 1}')
            try:
                self.wait(2, By.XPATH, f'//tr[@class="Even" or @class="Odd"][1]')
            except TimeoutException:
                print('Demora no carregamento da página!')
                break
            number = 1
            while True:
                try:
                    ips = self.driver.find_element_by_xpath(f'//tr[@class="Even" or @class="Odd"][{number}]')
                    ip = ips.find_element_by_xpath('./td[1]').text
                    if ip:
                        porta = ips.find_element_by_xpath('./td[2]').text
                        protocolo = ips.find_element_by_xpath('./td[3]').text
                        pais = ips.find_element_by_xpath('./td[5]').text
                        uptime = ips.find_element_by_xpath('./td[8]').text
                        ip_dict = {
                            'ip': ip,
                            'porta': porta,
                            'protocolo': protocolo,
                            'pais': pais,
                            'uptime': uptime
                        }
                        proxies_list.append(ip_dict)
                        print(
                            f"Number: {number} -> {ip}, porta -> {porta}, protocolo -> {protocolo}, pais -> {pais}, uptime -> {uptime}")
                    number += 1
                except NoSuchElementException:
                    break

            try:
                next_button = self.driver.find_element_by_xpath('//*[@class="current"]/following-sibling::a[1]')
                next_button.click()
            except NoSuchElementException:
                pass
        self.driver.close()

        with open(Path.cwd().joinpath('proxies.json'), 'a') as f:
            f.write(dumps(proxies_list))
        print(f'Total de Proxies Capturadas: {len(proxies_list)}')

    def wait(self, time, type_by, query):
        element = WebDriverWait(self.driver, time).until(
            ec.element_to_be_clickable((type_by, query)))
        return element


if __name__ == "__main__":
    start_time = time()
    rpa = SeniorUp()
    rpa.open_browser()
    rpa.first_page()
    print(f'Feito em {round(time() - start_time, 2)} segundos')
