from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, FileResponse 
from fastapi.templating import Jinja2Templates
import pandas as pd
import yfinance as yf
from fastapi.staticfiles import StaticFiles
from pathlib import Path

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ Templates
templates = Jinja2Templates(directory="templates")
symbols = ["TCS.NS", "INFY.NS", "RELIANCE.NS"]
data_dict = {}

# ----------------------------
# Load Data
# ----------------------------
def load_data():
    for sym in symbols:
        df = yf.download(sym, period="3mo")
        df.reset_index(inplace=True)

        df.dropna(inplace=True)

        df["Daily Return"] = (df["Close"] - df["Open"]) / df["Open"]
        df["MA7"] = df["Close"].rolling(7).mean()
        df["52W High"] = df["Close"].rolling(252).max()
        df["52W Low"] = df["Close"].rolling(252).min()
        df["Volatility"] = df["Close"].rolling(7).std()

        data_dict[sym] = df

try:
    load_data()
except Exception as e:
    print("Data fetch failed:", e)
    data_dict = {}

# ----------------------------
# Frontend Page
# ----------------------------




@app.get("/")
def home():
    return FileResponse(Path("templates/index.html"))
# ----------------------------
# APIs
# ----------------------------
@app.get("/companies")
def get_companies():
    return symbols

@app.get("/data/{symbol}")
def get_data(symbol: str):
    if symbol not in data_dict:
        return {"error": "Invalid symbol"}
    return data_dict[symbol].tail(30).to_dict(orient="records")

@app.get("/summary/{symbol}")
def summary(symbol: str):
    if symbol not in data_dict:
        return {"error": "Invalid symbol"}

    df = data_dict[symbol]
    return {
        "high": float(df["Close"].max()),
        "low": float(df["Close"].min()),
        "avg": float(df["Close"].mean())
    }

@app.get("/compare")
def compare(symbol1: str, symbol2: str):
    if symbol1 not in data_dict or symbol2 not in data_dict:
        return {"error": "Invalid symbols"}

    df1 = data_dict[symbol1].tail(30)
    df2 = data_dict[symbol2].tail(30)

    return {
        "symbol1": df1["Close"].squeeze().tolist(),
        "symbol2": df2["Close"].squeeze().tolist()
    }
