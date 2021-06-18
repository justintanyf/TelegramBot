import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from datetime import datetime
import os
import psycopg2

PORT = int(os.environ.get('PORT', '8443'))

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

# the token is a variable in heroku
TOKEN = os.environ["TOKEN"]

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    # Ideally I would get the Chat ID here and send it to the database and assign it to a new account
    # This enables us to start a conversation without prompting
    chatID = getChatID(update, context)
    print(chatID)
    timeNow = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(timeNow)
    # Supposedly code to connect to database
    DATABASE_URL = os.environ['DATABASE_URL']
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    cur = conn.cursor()
    cur.execute("INSERT INTO users (created_on, chat_id) VALUES (%s, %s)",
        (timeNow, chatID))
    conn.commit()
    cur.close()
    conn.close()
    update.message.reply_text('Begin your journey through the KingKiller chronicles')

def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text("GET HELP! PLEASE! My brother, he's dying. Get help, HELP HIM!")

def getID(update, context):
    """Send a message when the command /login is issued."""
    update.message.reply_text("Want to play this game with better visuals and music? \n Download our game in the store(insert IOS and Android Store link here) and enter your unique code(insert code here) to not lose your progress!")

def echo(update, context):
    """Echo the user message."""
    update.message
    if update.message.text == None: # Should check if it is a sticker?
        update.message.reply_text("“Words are pale shadows of forgotten names. As names have power, words have power. Words can light fires in the minds of men. Words can wring tears from the hardest hearts.” + \n + ― Patrick Rothfuss, The Name of the Wind")
    update.message.reply_text(update.message.text)

def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

# The JSON can be in different formats, so this ensures we get the right chat_id everytime
def getChatID(update, context):
    chat_id = -1

    if update.message is not None:
        chat_id = update.message.chat.id
    elif update.callback_query is not None:
        chat_id = update.callback_query.message.chat.id
    elif update.poll is not None:
        chat_id = context.bot_data[update.poll.id]

    return chat_id

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
    # Webhooks lower our server usage compared to long polling
    updater.start_webhook(listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url="https://the-paramours-candour.herokuapp.com/" + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()

if __name__ == '__main__':
    main()