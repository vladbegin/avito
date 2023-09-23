import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select
from tqdm import tqdm

# from selenoid_init import setup_browser


import logging

from selenium_init import setup_selenium
from sql import setup_database, insert_into_database


def parser(url:str):
    logging.info("Start")
    # driver = setup_browser()
    driver = setup_selenium()
    driver.get(url)
    driver.implicitly_wait(4)
    driver.maximize_window()
    # try:
    #     # Находим элемент span по тексту
    #     element = driver.find_element(By.XPATH, '//span[text()="Сначала в выбранном радиусе"]')
    #     # Нажимаем на элемент
    #     element.click()
    #     driver.find_element(by=By.XPATH, value="//button[@data-marker='search-filters/submit-button']").click()
    # except Exception as ex:
    #     logging.error("Не нашел кнопку сначала в выбранном регионе", exc_info=True)

    # try:
    #
    #     # Сортировка по дате
    #     # Находим элемент выпадающего списка по его атрибуту 'data-marker'
    #     sort_select = driver.find_element(by=By.CSS_SELECTOR, value="select[data-marker='sort-select/input']")
    #     # Создаем объект Select для работы с выпадающим списком
    #     select = Select(sort_select)
    #     # Выбираем опцию "По дате" по значению
    #     select.select_by_value("104")
    #     driver.implicitly_wait(3)
    # except Exception as ex:
    #     print(ex)


    try:
        ads_count = driver.find_element(by=By.XPATH, value="//span[@data-marker='page-title/count']").text.replace(' ','')
        print(ads_count)
        ads_count = int(ads_count)
        if ads_count % 50 > 0:
            page_count = (ads_count // 50) + 1
        else:
            page_count = ads_count // 50
        print(page_count)
        time.sleep(30)
        for page in tqdm(range(1, page_count + 1)):
            driver.get(f"{url}&p={page}")
            driver.implicitly_wait(3)
            ads_elements = driver.find_elements(by=By.XPATH, value='//a[@data-marker="item-title"]')
            # print(ads_elements)
            for ad in ads_elements:
                link = ad.get_attribute("href")
                ad_id = link.split('_')[-1]
                # print(ad_id)
                insert_into_database(link,ad_id)
            print(f"Закончил сбор объявлений на странице {page}")
    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

if __name__=='__main__':
    setup_database()
    parser(url='https://www.avito.ru/velikiy_novgorod/avtomobili/s_probegom-ASgBAgICAUSGFMjmAQ?cd=101&f=ASgBAQECA0TyCrCKAYYUyOYB~vAP6Lv3AgJAxOsRFP7nigOE0RJk_MjaEYjJ2hGSydoRnMnaEaLJ2hGoydoRA0X4Ahd7ImZyb20iOjI4NDUsInRvIjpudWxsfb4VGHsiZnJvbSI6bnVsbCwidG8iOjE1NTcyfcaaDBd7ImZyb20iOjAsInRvIjoxMDUwMDAwfQ&radius=500&searchRadius=500&user=1')