import logging
import time
from multiprocessing import Process

from save_params import save_test_data
# from selenoid_init import setup_browser
from selenium_init import setup_selenium
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

from sql import fetch_next_url, update_status_to_pending, update_status_to_wait_error, update_status_to_error

# from loader import driver
logging.basicConfig(level=logging.INFO, filename="logi.log",filemode="w",format="%(asctime)s %(levelname)s %(message)s", encoding='utf-8')
def worker1():
    logging.info("start worker1")
    # driver = setup_browser()
    driver = setup_selenium()
    logging.info('setup browser')
    while True:
        try:
            url = fetch_next_url()
            logging.info('fetch_next_url')
            if not url:
                print("No URLs left with status 'wait'")
                logging.info(msg="No URLs left with status 'wait'")
                driver.close()
                driver.quit()
                break  # Это выйдет из цикла while True


            update_status_to_pending(url)
            logging.info('update_status_to_pending')

            driver.get(url)
            logging.info(msg=f"driver get url={url}")
            # driver.maximize_window()
            driver.implicitly_wait(3)
            try:
                logging.info(f"driver try find 'closed-warning-content'")
                closed_warning_element = driver.find_element(By.XPATH,
                                                             "//span[contains(@class, 'closed-warning-content') and contains(text(), 'Объявление снято с публикации.')]")
                update_status_to_error(url=driver.current_url)
                logging.info(msg=f"for url {driver.current_url} change status to error")
                continue
            except Exception as ex:
                logging.error(msg="driver not find 'closed-warning-content'", exc_info=False)

            try:
                logging.info(f"driver try find ad don't show")
                driver.find_element(By.XPATH,'//span[contains(@class,"desktop-") and contains(text(),"Перейти к поиску")]')

                update_status_to_error(url=driver.current_url)
                logging.info(msg=f"for url {driver.current_url} change status to error")
                continue
            except Exception as ex:
                logging.error(msg="driver not find ad don't show", exc_info=False)

            try:
                # save_data(driver=driver)
                save_test_data(driver)
                # time.sleep(3)
            except Exception as ex:
                print(ex)
                logging.error(exc_info=True)
                # print(url)
        except Exception as ex:
            logging.info(exc_info=True, msg='Обновил статус на wait')
            update_status_to_wait_error(url)
            driver.close()
            driver.quit()




def main():
   try:
       worker1()
   except Exception as ex:
       print(ex)
       worker1()


if __name__=='__main__':
    main()
