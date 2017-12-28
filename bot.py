from telegram.ext import Updater, CommandHandler, MessageHandler, RegexHandler, Filters
from telegram import ForceReply
import os
from roll import roll, dice_pattern
import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

HELP_TEXT = "你好，我是牢泽香肠\n" \
            "/roll 骰子个数d面数\n" \
            "如 /roll 2d6 即为掷2个6面骰子，可以加减多个骰子或修正值，如/roll 2d6+1d10-5\n" \
            "/help 查看帮助\n" \

def start_handler(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text=HELP_TEXT)

def reply_handler(bot, update, args=None):
    sender = update.message.from_user.first_name
    if args:
        text = args[0]
        msg = " ".join(args)
    else:
        text = update.message.text.split()[0]
        msg = update.message.text
    result = roll(text)
    if result:
        print(result)
        rv = "{} 掷了骰子「 {} 」\n" \
               "掷出: {} \n" \
               "总和为: {}".format(sender, msg, str(result)[1:-1], str(sum([sum(i) for i in result])))
        update.message.reply_text(rv)

def roll_dice_handler(bot, update, args):
    if not args:
        update.message.reply_text(text="请输入 骰子个数d面数", reply_markup=ForceReply(selective=True))
        return
    else:
        reply_handler(bot, update, args)

def error(bot, update, error):
    logging.error('Update "%s" caused error "%s"' % (update, error))
    update.message.reply_text("出现了某种迷之错误")

def main():
    updater = Updater(os.getenv('BOT_TOKEN'))
    updater.dispatcher.add_handler(CommandHandler('start', start_handler))
    updater.dispatcher.add_handler(CommandHandler('help', start_handler))
    updater.dispatcher.add_handler(CommandHandler('roll', roll_dice_handler, pass_args=True))
    updater.dispatcher.add_handler(MessageHandler(Filters.reply, reply_handler))
    updater.dispatcher.add_error_handler(error)
    updater.start_polling()


if __name__ == '__main__':
    main()