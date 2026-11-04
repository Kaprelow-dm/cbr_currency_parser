# 📈 Парсер курсов валют ЦБ РФ + Power BI Dashboard

Проект для автоматического сбора, обработки и визуализации официальных курсов валют Центрального Банка Российской Федерации.

## 🚀 Возможности
- **Парсинг истории:** Сбор курсов за последние 30 дней (с пропуском выходных).
- **Anti-Ban:** Использование рандомных User-Agent и задержек для обхода блокировок.
- **Экспорт в Excel:** Сохранение чистых данных в `cbr_history.xlsx` через Pandas.
- **Визуализация (Power BI):** Интерактивный дашборд с карточками курсов USD/EUR, графиком динамики и рейтингом валют.

## 🛠️ Стек технологий
- **Python 3.12**
- **Библиотеки:** `requests`, `BeautifulSoup4`, `pandas`, `lxml`
- **Визуализация:** Power BI Desktop

## 📦 Установка и запуск
1. Клонируйте репозиторий:
    git clone https://github.com/Kaprelow-dm/cbr_currency_parser.git
    cd cbr_currency_parser

2. Установите зависимости:
    pip install -r requirements.txt

3. Запустите парсер:
    python cbr_parser.py
    (Скрипт создаст файл cbr_history.xlsx с данными за 30 дней).

4. 📊 Дашборд
    Файл cbr_currency_dashboard.pbit содержит интерактивный дашборд. Для обновления данных достаточно обновить запрос в Power BI.

<img width="1313" height="735" alt="dashboard" src="https://github.com/user-attachments/assets/602ca827-3da2-4dc2-b38f-e8ce752e673c" />


👨‍💻 Автор
Telegram: @BigDiccNRG
