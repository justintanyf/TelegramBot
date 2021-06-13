import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import os
PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# https://stackoverflow.com/questions/55776767/how-to-hide-bot-telegram-token-with-gitignore
TOKEN = os.environ["TOKEN"]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("GET HELP! PLEASE! My brother, he's dying. Get help, HELP HIM!")

def getID(update, context):
    """Send a message when the command /login is issued."""
    update.message.reply_text("Want to play this game with better visuals and music? + \n + Download our game in the store(insert IOS and Android Store link here) and enter your unique code(insert code here) to not lose your progress!")

def echo(update, context):
    """Echo the user message."""
    if (update.message.text != None): # Should check if it is a sticker?
        update.message.reply_text("“Words are pale shadows of forgotten names. As names have power, words have power. Words can light fires in the minds of men. Words can wring tears from the hardest hearts.” + \n + ― Patrick Rothfuss, The Name of the Wind")
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("getid", getID))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url="https://the-paramours-candour.herokuapp.com/" + TOKEN)
    #updater.bot.setWebhook('https://the-paramours-candour.herokuapp.com/' + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()