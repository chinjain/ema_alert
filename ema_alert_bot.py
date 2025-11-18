import time
import requests
import pandas as pd
import numpy as np

TOKEN = "8594303077:AAHdWANkCWZu_Ri97C5r8iiBSG_ain_0Xsg"
CHAT_ID = "925975762"

def send_alert(message):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={"chat_id": CHAT_ID, "text": message})

def fetch_data(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit}"
    data = requests.get(url).json()
    
    df = pd.DataFrame(data, columns=[
        "time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "num_trades", "tbbav", "tbqav", "ignore"
    ])
    df["close"] = df["close"].astype(float)
    return df

def check_crossover():
    df = fetch_data()

    df["ema9"] = df["close"].ewm(span=9).mean()
    df["ema20"] = df["close"].ewm(span=20).mean()

    prev_ema9 = df["ema9"].iloc[-2]
    prev_ema20 = df["ema20"].iloc[-2]
    curr_ema9 = df["ema9"].iloc[-1]
    curr_ema20 = df["ema20"].iloc[-1]

    if prev_ema9 < prev_ema20 and curr_ema9 > curr_ema20:
        send_alert("🔔 **Bullish Crossover (EMA 9 > EMA 20)** on 15m")

    if prev_ema9 > prev_ema20 and curr_ema9 < curr_ema20:
        send_alert("🔔 **Bearish Crossover (EMA 9 < EMA 20)** on 15m")

if __name__ == "__main__":
    send_alert("🚀 EMA Alert Bot Started on 15m chart")
    
    while True:
        try:
            check_crossover()
        except Exception as e:
            send_alert(f"⚠️ Error: {e}")
        
        time.sleep(60)  # Check every 1 minute
