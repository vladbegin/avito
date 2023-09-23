
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from tqdm import tqdm
# from telegram import Bot
# from apscheduler.schedulers.blocking import BlockingScheduler

def setup_selenium():

    service = Service(executable_path='chromedriver.exe')
    
    # change useragent
    useragent = UserAgent()

    # options
    options = webdriver.ChromeOptions()
    # user-agent
    options.add_argument(f"user-agent={useragent.random}")
    # headless mode
    # options.add_argument("--headless=new")
    # options.headless = True
    # disable webdriver mode
    # # for older ChromeDriver under version 79.0.3945.16
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option("useAutomationExtension", False)
    # for ChromeDriver version 79.0.3945.16 or over
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(service=service, options=options)
    return driver