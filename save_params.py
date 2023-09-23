import logging
import re
import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from sql import insert_into_cars_info, update_status_to_done, update_status_to_wait_error, update_status_to_error
logging.basicConfig(level=logging.INFO, filename="logi.log",filemode="a",format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')

def extract_data_by_xpath(driver, xpath, default_value, attribute=None):
    try:
        element = driver.find_element(by=By.XPATH, value=xpath)
        if attribute:
            return element.get_attribute(attribute)
        else:
            return element.text
    except Exception as ex:
        logging.error(exc_info=True)
        return default_value
def save_test_data(driver):
    try:
        logging.info(f"driver start function save_test_data")
        time.sleep(3)
        current_url = driver.current_url
        title = driver.find_element(By.XPATH, "//h1[@data-marker='item-view/title-info']").text.split(',')[0].strip('"')
        price = driver.find_element(By.XPATH,'//span[@data-marker="item-view/item-price"]').get_attribute('content')
        seller_type = driver.find_element(by=By.XPATH, value='//div[@data-marker="seller-info/label"]').text
        address = driver.find_element(by=By.XPATH, value="//div[@itemprop='address']/span").text
        ad_id = driver.find_element(by=By.XPATH, value="//span[@data-marker='item-view/item-id']").text
        try:
            params_ul = driver.find_element(By.XPATH, "//ul[contains(@class, 'params-paramsList')]")
            for param_li in params_ul.find_elements(by=By.TAG_NAME, value='li'):
                text = param_li.text
                if "Год выпуска" in text:
                    year = param_li.text.split(": ")[1]
                    # print(year)
                elif "Поколение" in text:
                    generation = param_li.text.split(": ")[1]
                    # print(generation)
                elif "Пробег" in text:
                    mileage = ''.join(filter(str.isdigit, param_li.text))
                    # print(mileage)
                elif 'Владельцев по ПТС' in text:
                    pts = param_li.text.split(": ")[1]
                    # print(pts)
                    if "4+" in pts:
                        print(f"in pts 4+")
                        owner_element = driver.find_element(by=By.XPATH, value="//h4[contains(@class, 'list-list-header')]")
                        num_owners = re.search(r'(\d+)', owner_element.text)
                        if num_owners:
                            pts = int(num_owners.group(1))
                            print(f"new pts: {pts}")
                        else:
                            pts = param_li.text.split(": ")[1]


                    # print(pts)
                elif "Состояние" in text:
                    condition = param_li.text.split(": ")[1]
                    # print(condition)
                elif "Модификация" in text:
                    modification = param_li.text.split(": ")[1]
                    # print(modification)
                elif "Объём двигателя" in text:
                    engine_capacity = param_li.text.split(": ")[1]
                    # print(engine_capacity)
                elif "Тип двигателя" in text:
                    type_engine = param_li.text.split(": ")[1]
                    # print(type_engine)
                elif "Коробка передач" in text:
                    transmission = param_li.text.split(": ")[1]
                    # print(transmission)
                elif "Тип кузова" in text:
                    body_type = param_li.text.split(": ")[1]
                    # print(body_type)
                elif "Цвет" in text:
                    color = param_li.text.split(": ")[1]
                    # print(color)
            data = (ad_id, title, price, year, generation, mileage, pts, condition, modification, engine_capacity,
                    type_engine, transmission, body_type, color, seller_type, address, current_url)
            # print(data)
            insert_into_cars_info(data)
            time.sleep(3)
            update_status_to_done(current_url)
        except Exception as ex:
            logging.error(msg="Ошибка при сборе данных с объявления",exc_info=True)
            update_status_to_error(current_url)


    except Exception as ex:
        print(ex)
        update_status_to_wait_error(current_url)