import pandas as pd
import requests
import datetime
import logging
import curlify
import traceback
import time
import pyotp
import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


url = "https://assets.upstox.com/market-quote/instruments/exchange/complete.csv.gz"

instrument_list = pd.read_csv(url, compression = "gzip")

def get_dataToken_upstox(tradesymbol, exchange = "NFO"):
    if exchange == "NFO":
        exchange = "NSE_FO"
    if exchange == "NSE":
        exchange = "NSE_EQ"
    if exchange == "MCX":
        exchange = "MCX_FO"
    if exchange == "BFO":
        exchange = "BSE_FO"
    if exchange == "BSE":
        exchange = "BSE_EQ"

    dataToken = instrument_list[(instrument_list["tradingsymbol"] == tradesymbol) & (instrument_list["exchange"] == exchange)]

    return dataToken.instrument_key.iloc[0]