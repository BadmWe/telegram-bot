import logging
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import qrcode
# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))

# Command Handlers


def start(update, context):
    # how do we pass class instance here
    context.bot.sendAnimation(chat_id=update.message.chat_id,
                              animation='https://c.tenor.com/8IIQDBECgssAAAAM/hello-sexy-hi.gif',
                              caption='Hello!',
                              )
    # datastorage.add_counter()

    """Send a message when the command /start is issued."""
    # update.message.reply_text(f'Hi!')
    # update.message.reply_text(f'Hi! number:{datastorage.counter}')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )

    qr.add_data(update.message.text)
    qr.make(fit=True)

    img = qr.make_image(back_color=(255, 195, 235), fill_color=(55, 95, 35))
    img.save('output.png')
    context.bot.send_photo(chat_id=update.message.chat_id,
                           photo=open('output.png', 'rb'))
    #context.bot.send_photo(update.message.chat_id, img)


def help(update, context):
    """Send a message when the command /help is issued."""

    update.message.reply_text('Help! Help! Help! Help!')


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary

    TOKEN = os.environ.get("API_KEY")
    APP_NAME = 'https://qrskynet.herokuapp.com/'

    updater = Updater(TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)
    updater.start_webhook(listen="0.0.0.0", port=PORT,
                          url_path=TOKEN, webhook_url=APP_NAME + TOKEN)
    updater.idle()


if __name__ == '__main__':
    main()
