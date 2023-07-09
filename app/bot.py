from pathlib import Path

from telegram import Update, ReplyKeyboardRemove
from telegram.ext import CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters

from app.constants import TARGET_IMAGES, STYLE_IMAGES, RESULT_IMAGES
from app.style_transfer import StyleTransfer

UPLOAD_TARGET_IMAGE, UPLOAD_STYLE_IMAGE, SHOW_RESULT = range(3)


class BotConversation:
    def __init__(self):
        self.model = StyleTransfer()

    def get_conversation(self):
        return ConversationHandler(
            entry_points=[CommandHandler('transfer_style', BotConversation.start)],
            states={
                UPLOAD_TARGET_IMAGE: [MessageHandler(filters.PHOTO, BotConversation.upload_target_image)],
                UPLOAD_STYLE_IMAGE: [MessageHandler(filters.PHOTO, self.upload_style_image)],
            },
            fallbacks=[CommandHandler('cancel', BotConversation.cancel)]
        )

    @staticmethod
    async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Upload target image")
        return UPLOAD_TARGET_IMAGE

    @staticmethod
    async def cancel(update: Update) -> int:
        user = update.message.from_user
        await update.message.reply_text(
            f'Bye {user}!', reply_markup=ReplyKeyboardRemove()
        )
        return ConversationHandler.END

    @staticmethod
    async def upload_target_image(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        file_id = update.message.photo[-1].file_id
        new_file = await context.bot.get_file(file_id)
        Path(TARGET_IMAGES).mkdir(parents=True, exist_ok=True)
        await new_file.download_to_drive(custom_path=f'{TARGET_IMAGES}/{update.effective_chat.id}.jpg')
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Upload style image")
        return UPLOAD_STYLE_IMAGE

    async def upload_style_image(self, update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
        file_id = update.message.photo[-1].file_id
        new_file = await context.bot.get_file(file_id)
        Path(STYLE_IMAGES).mkdir(parents=True, exist_ok=True)

        await new_file.download_to_drive(custom_path=f'{STYLE_IMAGES}/{update.effective_chat.id}.jpg')

        self.model.run_style_transfer(update.effective_chat.id,
                                      TARGET_IMAGES / f'{update.effective_chat.id}.jpg',
                                      STYLE_IMAGES / f'{update.effective_chat.id}.jpg')
        await context.bot.send_photo(update.effective_chat.id,
                               photo=open(RESULT_IMAGES / f'{update.effective_chat.id}.jpg', 'rb'))
        return ConversationHandler.END
