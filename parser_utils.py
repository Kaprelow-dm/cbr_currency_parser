import random
import time
import requests
from bs4 import BeautifulSoup

import os
import pandas as pd
from datetime import datetime

# Список реальных User-Agent'ов (можно расширять)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15",
    "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/115.0"
]

def get_random_headers():
    """Возвращает словарь с рандомным User-Agent"""
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7",
    }

def safe_request(url, payload=None, proxies_list=None):
    """
    Универсальная функция для запроса с маскировкой.
    proxies_list: список строк вида ["http://user:pass@ip:port", ...]
    """
    # 1. Маскировка
    headers = get_random_headers()
    
    # 2. Выбор прокси (если есть)
    proxy = None
    if proxies_list:
        proxy = {"http": random.choice(proxies_list), "https": random.choice(proxies_list)}
    
    # 3. Случайная задержка (от 1 до 3 секунд), чтобы не быть роботом
    time.sleep(random.uniform(1.0, 3.0))
    
    try:
        # Если payload есть - делаем POST, если нет - GET
        if payload:
            response = requests.post(url, data=payload, headers=headers, proxies=proxy, timeout=15)
        else:
            response = requests.get(url, headers=headers, proxies=proxy, timeout=15)
            
        response.raise_for_status()
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Ошибка запроса к {url}: {e}")
        return None

def save_to_excel(data_list, filename="result.xlsx"):
    """
    Принимает список словарей (результат парсинга) и сохраняет в Excel.
    """
    if not data_list:
        print("❌ Нечего сохранять, список пуст.")
        return

    # 1. Создаем DataFrame
    df = pd.DataFrame(data_list)
    
    # 2. Добавляем колонку с датой парсинга (чтобы заказчик знал, когда это собрано)
    df['parsed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # 3. Сохраняем в Excel. 
    # index=False убирает нумерацию строк слева (чтобы было чисто).

    df.to_excel(filename, index=False)
    print(f"✅ Данные сохранены в {filename}. Всего строк: {len(df)}")

def save_to_csv(data_list, filename="result.csv"):
    """
    Если Excel не нужен, а нужен просто CSV (легче и быстрее).
    """
    if not data_list: return
    
    df = pd.DataFrame(data_list)
    df['parsed_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # ВОТ ОНА, МАГИЯ. utf-8-sig спасает русские буквы в Excel!
    df.to_csv(filename, index=False, encoding="utf-8-sig", sep=";")
    print(f"✅ Данные сохранены в {filename}. Всего строк: {len(df)}")


# --- ТОТ САМЫЙ БЛОК ЗАПУСКА ---
if __name__ == "__main__":
    url = "https://www.cbr.ru/currency_base/daily/"
    response = safe_request(url)
    if response:
        print(f"✅ Успешно! Статус: {response.status_code}")
        print(f"Длина ответа: {len(response.text)}")

    # А ВОТ ЗДЕСЬ ТЕСТОВЫЕ ДАННЫЕ
    test_data = [
        {"name": "Товар 1", "price": 1000, "url": "http://example.com/1"},
        {"name": "Товар 2", "price": 2500, "url": "http://example.com/2"},
        {"name": "Товар 3", "price": 500, "url": "http://example.com/3"}
    ]
    save_to_excel(test_data)
