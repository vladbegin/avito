import sqlite3
import os
import logging

# import urllib3
# from telepot.loop import MessageLoop
# import telepot.api
#
# telepot.api._pools = {
#     'default': urllib3.PoolManager(num_pools=3, maxsize=10, retries=6, timeout=30),
# }
#
# my_bot = telepot.Bot('2138397598:AAH7xu0fx_PJIYHc8a1wq7TzOwzSNG2s9CA')
#
# def handle(msg):
#     print(msg)
#
# MessageLoop(my_bot, handle).run_as_thread()
db_names = 'cars_nov_database.db'

def setup_database():
    db_name = db_names

    # Если файл базы данных уже существует, не делаем ничего
    if os.path.exists(db_name):
        return

    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Создание таблицы links, если она не существует
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS links (
            ad_id INTEGER NOT NULL,
            link TEXT NOT NULL,
            status TEXT NOT NULL
        )
    """)

    # Создание таблицы cars_info, если она не существует
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars_info (
            ad_id INTEGER NOT NULL,
            title TEXT,
            price TEXT,
            Year TEXT,
            Generation TEXT,
            Mileage TEXT,
            PTS TEXT,
            Condition TEXT,
            Modification TEXT,
            Engine_capacity TEXT,
            Type_engine TEXT,
            Transmission TEXT,
            Body_type TEXT,
            color TEXT,
            seller_type TEXT,
            address TEXT,
            current_url TEXT
        )
    """)

    conn.commit()
    conn.close()


def insert_into_database(link, ad_id, status='wait'):
    conn = sqlite3.connect(db_names)
    cursor = conn.cursor()

    # Проверяем существование ad_id в таблице
    cursor.execute("SELECT * FROM links WHERE ad_id=?", (ad_id,))
    entry = cursor.fetchone()

    # Если ad_id не существует, вставляем новую запись
    if entry is None:
        cursor.execute("INSERT INTO links (ad_id, link, status) VALUES (?, ?, ?)", (ad_id, link, status))
        conn.commit()



    conn.close()


def insert_into_cars_info(data):
    logging.info(data)
    conn = sqlite3.connect(db_names)
    cursor = conn.cursor()

    # Проверяем существование ad_id в таблице
    cursor.execute("SELECT * FROM cars_info WHERE ad_id=?", (data[0],))
    entry = cursor.fetchone()

    # Если ad_id не существует, вставляем новую запись
    if entry is None:
        cursor.execute("""
            INSERT INTO cars_info (ad_id, title, price, year, generation, mileage, pts, condition, 
                                   modification, engine_capacity, type_engine, transmission, body_type,
                                   color, seller_type, address, current_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        """, data)
        # my_bot.sendMessage('87355412', f'Новое объявление {data[1]}\nЦена: {data[2]}\n{data[16]}', disable_web_page_preview=True)
        conn.commit()

    conn.close()


def update_status_to_done(url):
    conn = sqlite3.connect(db_names)
    cursor = conn.cursor()

    cursor.execute("UPDATE links SET status='done' WHERE link=?", (url,))

    conn.commit()
    conn.close()


def update_status_to_pending(url):
    conn = sqlite3.connect(db_names)
    cursor = conn.cursor()
    cursor.execute("UPDATE links SET status='pending' WHERE link=?", (url,))
    conn.commit()
    conn.close()


def update_status_to_wait_error(url):
    conn = sqlite3.connect(db_names)
    cursor = conn.cursor()
    cursor.execute("UPDATE links SET status='wait' WHERE link=?", (url,))
    conn.commit()
    conn.close()

def update_status_to_error(url):
    conn = sqlite3.connect(db_names)
    cursor = conn.cursor()
    cursor.execute("UPDATE links SET status='error' WHERE link=?", (url,))
    conn.commit()
    conn.close()


def fetch_next_url():
    conn = sqlite3.connect(db_names)
    cursor = conn.cursor()
    cursor.execute("SELECT link FROM links WHERE status='wait' LIMIT 1")
    url = cursor.fetchone()
    conn.close()
    return url[0] if url else None