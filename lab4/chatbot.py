from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters
import configparser
import logging
from ChatGPT_HKBU import HKBU_ChatGPT

# Global variable for ChatGPT instance
chatgpt = None

# Define the handler function for ChatGPT responses
async def equiped_chatgpt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global chatgpt
    reply_message = chatgpt.submit(update.message.text)
    logging.info("Update: %s", update)
    logging.info("Context: %s", context)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def main():
    global chatgpt

    # Load the configuration file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Initialize ChatGPT instance
    chatgpt = HKBU_ChatGPT(config)

    # Setup logging
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
    )

    # Create the Application
    application = ApplicationBuilder().token(config['TELEGRAM']['ACCESS_TOKEN']).build()

    # Add message handlers
    chatgpt_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, equiped_chatgpt)
    application.add_handler(chatgpt_handler)

    # Start the Bot
    application.run_polling()

if __name__ == '__main__':
    main()
