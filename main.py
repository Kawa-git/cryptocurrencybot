import telegram.ext
import logging
import pandas_datareader as web
import time
import os
from datetime import datetime

# Enables logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

def start(update, context):
    update.message.reply_text("Welcome!\n\nType \help to start using this bot!")

def help(update, context):
    update.message.reply_text("""
    Prints out the value of the selected stock.
    To print cyptocurrency, provide the complete stock name: BTC-USD

    /start -> Welcome message
    /help -> This message
    /stock -> Prints the stock you provided
    /bat -> Prints the BAT-USD stock
    /btc -> Prints the BTC-USD stock
    """)

def handle_message(update, context):
    try:
        threshold = float(update.message.text)
        update.message.reply_text(f"New threshold [ {threshold} ]")
    except:
        update.message.reply_text("Cannot update threshold.\nFormat is invalid")

def stock(update, context):
    end = datetime.today()
    start = datetime(end.year-1, end.month, end.day)

    try:
        t = str(context.args[0]).upper()
        data = web.DataReader(t, 'yahoo', start, end)
        price = data.iloc[-1]['Close']
        update.message.reply_text(f"The current price of {t} is {price:.2f}$!")
    except:
        update.message.reply_text("Cannot print the price.\nFormat is invalid")
        
def btc(update, context):
    t = ""
    end = datetime.today()
    start = datetime(end.year-1, end.month, end.day)

    try:
        data = web.DataReader("BTC-USD", 'yahoo', start, end)
        price = data.iloc[-1]['Close']
        update.message.reply_text(f"The current price of {t} is {price:.2f}$!")
    except:
        update.message.reply_text("Cannot print the price.\nFormat is invalid")
    

def bat(update, context):
    t = ""
    end = datetime.today()
    start = datetime(end.year-1, end.month, end.day)

    try:
        data = web.DataReader("BAT-USD", 'yahoo', start, end)
        price = data.iloc[-1]['Close']
        update.message.reply_text(f"The current price of {t} is {price:.2f}$!")
    except:
        update.message.reply_text("Cannot print the price.\nFormat is invalid")

def main():
    TOKEN = os.environ["TOKEN"]

    APP_NAME = 'https://telegramcryptocurrencybot.herokuapp.com/'
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    # Get the dispatcher to register handlers
    disp = updater.dispatcher

    disp.add_handler(telegram.ext.CommandHandler("start", start))
    disp.add_handler(telegram.ext.CommandHandler("help", help))
    disp.add_handler(telegram.ext.CommandHandler("stock", stock))
    disp.add_handler(telegram.ext.CommandHandler("btc", btc))
    disp.add_handler(telegram.ext.CommandHandler("bat", bat))

    updater.start_webhook(listen="0.0.0.0", port=PORT, url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    updater.idle()

if __name__ == "__main__":
    main()