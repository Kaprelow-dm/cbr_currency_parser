import time
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from parser_utils import safe_request, save_to_excel

def parse_cbr_history(days_back=30):
    data_list = []
    # Задаем жесткую дату старта: 31 октября 2026
    end_date = datetime.now()
    
    for i in range(days_back):
        date = end_date - timedelta(days=i)
        
        # Пропускаем субботу (5) и воскресенье (6)
        if date.weekday() >= 5:
            continue
            
        date_str = date.strftime("%d.%m.%Y")
        url = f"https://www.cbr.ru/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To={date_str}"
        
        print(f"Парсим {date_str}...")
        response = safe_request(url)
        
        if not response:
            print(f"❌ Не удалось получить данные за {date_str}. Пропускаем.")
            continue
            
        soup = BeautifulSoup(response.text, "lxml")
        table = soup.find("table", class_="data")
        if not table: 
            continue
            
        rows = table.find_all("tr")[1:]
        
        # Берем только USD, EUR и CNY (чтобы не перегружать график)
        target_currencies = ["USD", "EUR", "CNY", "GBP", "JPY"]
        
        for row in rows:
            cols = row.find_all("td")
            if len(cols) == 5:
                letter_code = cols[1].text.strip()
                if letter_code in target_currencies:
                    data_list.append({
                        "date": date_str, # Добавляем дату в данные!
                        "code": cols[0].text.strip(),
                        "letter_code": letter_code,
                        "name": cols[3].text.strip(),
                        "rate": cols[4].text.strip()
                    })
        
        # Пауза между запросами, чтобы ЦБ не забанил
        time.sleep(1)

    print(f"✅ Собрано {len(data_list)} записей.")
    save_to_excel(data_list, "cbr_history.xlsx")

if __name__ == "__main__":
    parse_cbr_history(days_back=31)