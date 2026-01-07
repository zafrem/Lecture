# pip install python-telegram-bot
# https://docs.python-telegram-bot.org/en/v21.10/examples.html
from telegram import ForceReply, Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# token
token="Telegtram Token"


async def start(update, context):
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context):
    _help_str = '''This is test bot.'''
    await update.message.reply_text(_help_str)


async def echo(update, context):
    await update.message.reply_text(update.message.text)


async def data(update, context):
    import _1_technical_analysis_Stochastic as stochastic

    df = stochastic.init_pre_df()
    plt, df = stochastic.stochastic(df)
    await update.message.reply_text("")


async def image(update, context):
    import _1_technical_analysis_Stochastic as stochastic
    import os

    screenshop_file_name = 'stochastic_report.png'

    if os.path.exists(screenshop_file_name):
        os.remove(screenshop_file_name)

    df = stochastic.init_pre_df()
    plt, df = stochastic.stochastic(df)
    plt.savefig(screenshop_file_name, bbox_inches='tight')

    context.bot.send_document(chat_id=update.message['chat']['id'], document=open(
        screenshop_file_name, 'rb'), filename='stochastic_report.png')
    #os.remove(screenshop_file_name)


def main():
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(token).build()

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("data", data))
    application.add_handler(CommandHandler("image", image))

    # on non command i.e message - echo
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()