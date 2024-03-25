#!/usr/bin/python3

import pprint
import json
import telegram
import requests
import os
from requests import *
from telegram import *
from telegram.ext import *

telegram_bot_token = "<TELEGRAM_BOT_TOKEN>"

updater = Updater(token=telegram_bot_token, use_context=True)
dispatcher = updater.dispatcher

############################ MENUS #########################################
def start(update, context):
    update.message.reply_text(main_menu_message(),
            reply_markup=main_menu_keyboard())

def main_menu(update,context):
  query = update.callback_query
  query.answer()
  query.edit_message_text(
                        text=main_menu_message(),
                        reply_markup=main_menu_keyboard())

############################ KEYBOARDS #########################################
def main_menu_keyboard():
    buttons = [[KeyboardButton("KDA_Stats")]]
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

############################# MESSAGES #########################################
def main_menu_message():
    return 'Welcome to the This Bot. Change this message if you so desire!!'

def help_message():
    return 'This is just a help message'

############################ MESSAGE HANDLER #########################################
def messageHandler(update: Update, context: CallbackContext):
    if "KDA_Stats" in update.message.text:
        stats(update, context)

############################# KDA STATS #########################################
def stats(update, context):
    chat_id = update.effective_chat.id
    message = ""

    kda = os.popen("curl https://api.mainnet.klever.finance/v1.0/assets/<KDA_ID>")
    holders = os.popen("curl https://api.mainnet.klever.finance/v1.0/assets/holders/<KDA_ID>") 
    kdapool = os.popen("curl https://api.mainnet.klever.finance/assets/pool/<KDA_ID>")
    bitcoinme = os.popen("curl https://api.exchange.bitcoin.me/v1/market/ticker?symbol=<KDA>-USDT")

    kdaStats = json.load(kda)
    hold = json.load(holders)
    pool = json.load(kdapool)
    exchange_data = json.load(bitcoinme)

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

    message += f"Name: {name}\nTicker: {ticker}\nPrice: *${price}*\nMC: *${mc}*\n\nAsset Type: {assetType}\nID: {assetID}\nPrecision: {precision}\nMax Supply: {max} KDA\nInitial Supply: {init} KDA\nCirculating Supply: {circ} KDA\nMinted: {mint} KDA\nTotal Staked: {staked} KDA\nKDA:KLV Fee Pool? {poolStatus}\nPool Ratio: {ratio1}%\n--Ex. Transfer: 0.375 {ticker}\nPool Bal: {klvpool} KLV / {kdapool} KDA\nTotal Holders: {totalHolders}\n"

    context.bot.send_message(chat_id=chat_id, text=message, parse_mode="Markdown")

############################# Handlers #########################################

updater = Updater(token=telegram_bot_token, use_context=True)

updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
updater.dispatcher.add_handler(CallbackQueryHandler(stats, stats))
updater.dispatcher.add_handler(MessageHandler(Filters.text, messageHandler))

updater.start_polling()
