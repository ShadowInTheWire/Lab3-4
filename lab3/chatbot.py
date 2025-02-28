from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import configparser
import logging

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    reply_message = update.message.text.upper()
    logging.info("Update: %s", update)
    logging.info("Context: %s", context)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def main():
    # Load the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    # Create the Application
    application = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()

    # Add message handler
    echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    application.add_handler(echo_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()