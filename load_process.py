import psutil
import schedule
import datetime as dt
import sqlite3

sr = 0


def job():
    """Функция, которая считывает процент загрузки процессора"""
    global sr
    d, p = dt.datetime.now(), psutil.cpu_percent()
    if not sr:
        sr = p
    else:
        sr = (sr + p) / 2
    conn = sqlite3.connect('cpu.db')
    cur = conn.cursor()
    cur.execute(f"""insert into data (created_date, load_data, avg_value) values ('{d}', {p}, {sr})""")
    conn.commit()
    conn.close()


# расписание запуска функции job
schedule.every(5).seconds.do(job)
while True:
    schedule.run_pending()