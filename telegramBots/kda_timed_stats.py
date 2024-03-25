#!/usr/bin/python3

from telegram import Bot
from telegram.error import TelegramError
from telegram.ext import Updater, CommandHandler
from telegram.ext import CallbackContext
from datetime import datetime, timedelta
import time
import requests
import json

TOKEN = '<TELEGRAM_BOT_ID>'  # Replace 'YOUR_TOKEN' with your actual bot token
CHAT_ID = '<-100xxxxxxxxx>'  # Replace 'CHAT_ID' with your actual chat ID


def stats(update, context):
    chat_id = CHAT_ID
    message = ""

    kda_response = requests.get("https://api.mainnet.klever.finance/v1.0/assets/<KDA_ID>")                  # Replace 'KDA_ID' with your actual KDA-ID
    hold_response = requests.get("https://api.mainnet.klever.finance/v1.0/assets/holders/<KDA_ID>")         # Replace 'KDA_ID' with your actual KDA-ID
    kdapool_response = requests.get("https://api.mainnet.klever.finance/assets/pool/<KDA_ID>")              # Replace 'KDA_ID' with your actual KDA-ID
    bitcoinme_response = requests.get("https://api.exchange.bitcoin.me/v1/market/ticker?symbol=kda-USDT")   # Replace 'KDA_ID' with your actual KDA-ID

    kdaStats = kda_response.json()
    hold = hold_response.json()
    pool = kdapool_response.json()
    exchange_data = bitcoinme_response.json()

    name = kdaStats['data']['asset']['name']
    ticker = kdaStats['data']['asset']['ticker']
    assetType = kdaStats['data']['asset']['assetType']
    assetID = kdaStats['data']['asset']['assetId']
    precision = kdaStats['data']['asset']['precision']
    maxSupply = kdaStats['data']['asset']['maxSupply']
    initialSupply = kdaStats['data']['asset']['initialSupply']
    circulatingSupply = kdaStats['data']['asset']['circulatingSupply']
    mintedValue = kdaStats['data']['asset']['mintedValue']
    totalStaked = kdaStats['data']['asset']['staking']['totalStaked']
    totalHolders = hold['pagination']['totalRecords']
    poolStatus = pool['data']['pool']['active']
    fRatioKDA = pool['data']['pool']['fRatioKDA']
    fRatioKLV = pool['data']['pool']['fRatioKLV']
    klvBal = pool['data']['pool']['klvBalance']
    kdaBal = pool['data']['pool']['kdaBalance']
    ratioKDA = "{:,.0f}".format(fRatioKDA/1000)
    ratioKLV = "{:,.0f}".format(fRatioKLV/1000000)
    ratio = pool['data']['pool']['ratio']
    ratio1 = "{:,.2f}".format(ratio*1000)
    kda_price = float(exchange_data['data']['price'])

    max = "{:,.0f}".format(maxSupply/1000)
    init = "{:,.0f}".format(initialSupply/1000)
    circ = "{:,.3f}".format(circulatingSupply/1000)
    mint = "{:,.3f}".format(mintedValue/1000)
    staked = "{:,.3f}".format(totalStaked/1000)
    kdapool = "{:,.3f}".format(kdaBal/1000)
    klvpool = "{:,.1f}".format(klvBal/1000000)
    price = "{:,.3f}".format(float(kda_price))
    mc = "{:,.3f}".format(circulatingSupply * kda_price / 1000)

    
###### YOU CAN CHANGE THE REFERENCE TO KDA TO YOUR TOKEN IN THE MESSAGE BELOW. MODIFY ACCORDINGLY AS YOU WISH ######
    
    message += f"Name: {name}\nTicker: {ticker}\nPrice: *${price}*\nMC: *{mc} *\n\nAsset Type: {assetType}\nID: {assetID}\nPrecision: {precision}\nMax Supply: {max} kda\nInitial Supply: {init} kda\nCirculating Supply: {circ} kda\nMinted: {mint} kda\nTotal Staked: {staked} kda\nkda:KLV Fee Pool? {poolStatus}\nPool Ratio: {ratio1}%\n--Ex. Transfer: 0.375 {ticker}\nPool Bal: {klvpool} KLV / {kdapool} kda\nTotal Holders: {totalHolders}\n"

    context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

class DummyContext:
    def __init__(self, bot):
        self.bot = bot

def main():
    bot = Bot(token=TOKEN)

    # Add the handler for the 'stats' command
    updater = Updater(token=TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("stats", stats))

  
###### SET THE DESIRED TIME YOU WOULD LIKE TO START STATS. YOU CAN THEN START THE BOT AND STATS WILL BEGIN AT YOUR SPECIFIED TIME ######
  
    desired_start_time = datetime.strptime("2024-03-08 07:00:00", "%Y-%m-%d %H:%M:%S")
    current_time = datetime.now()
    delay = (desired_start_time - current_time).total_seconds()

    if delay < 0:
        desired_start_time += timedelta(days=1)
        delay = (desired_start_time - current_time).total_seconds()

    # Sleep for the calculated delay
    time.sleep(delay)


###### SET STATS INTERVAL. BELOW USES EVERY 6 HOURS TO DISPLAY KDA STATS ######
  
    dummy_context = DummyContext(bot) 
    while True:
        stats(None, dummy_context)  # Call the stats function
        time.sleep(6 * 60 * 60)  # Sleep for 1 minute

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()

