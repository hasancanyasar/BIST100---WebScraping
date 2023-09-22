import requests
from bs4 import BeautifulSoup
import sqlite3
import datetime
import time

db = sqlite3.connect("stockinfo.db")
table_name = "StockData_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
auth = db.cursor()
auth.execute(f"CREATE TABLE IF NOT EXISTS {table_name} (StockName TEXT, StockPrice REAL, StockChangeRate REAL)")

print("Borsa Verileri Çıkarılıyor...")
time.sleep(2)
print("Veriler Veritabanına Kaydediliyor...")
time.sleep(2)

url = "https://www.haberturk.com/ekonomi/borsa/bist-100"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
}

parser = BeautifulSoup(requests.get(url, headers=headers).content, "html.parser")
mainData = parser.find("div", {"class": "w-full min-w-full"}).find_all("tr")
for tr in mainData:
    stockName = tr.find("span", {"class": "text-sm"})
    stockPrice = tr.find("div", {"class": "min-w-max"})
    stockChangeRate = tr.find("span", {"class": "text-green-700"})
    stockChangeRateMinus = tr.find("span", {"class": "text-red-700"})

    if stockPrice and stockPrice is not None:
        stockName = stockName.get_text(strip=True)
        stockPrice = stockPrice.get_text(strip=True)
        if stockChangeRate is not None:
            stockChangeRate = stockChangeRate.get_text(strip=True)
        elif stockChangeRateMinus is not None:
            stockChangeRate = stockChangeRateMinus.get_text(strip=True)
        auth.execute(f"INSERT INTO {table_name} (StockName, StockPrice, StockChangeRate) VALUES (?, ?, ?)", (stockName, stockPrice, stockChangeRate))
        print(stockName, stockPrice, stockChangeRate)

db.commit()
print(f"Veriler '{table_name}' tablosuna eklendi.")
input("Uygulamadan Çıkmak İçin 'ENTER' tuşuna basınız.")
