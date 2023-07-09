from telegram.ext import ApplicationBuilder

from app.bot import BotConversation
from app.constants import TOKEN
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

if __name__ == '__main__':
    application = ApplicationBuilder().token(TOKEN).build()
    stages = BotConversation()
    app_handler = stages.get_conversation()

    application.add_handler(app_handler)
    application.run_polling()
