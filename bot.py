from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
import logging
import telegram
from telegram import InlineQueryResultArticle, InputTextMessageContent, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from settings import API_TOKEN, ID_CHAT
import core_shopping_list

logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )

PROXY = {'proxy_url': 'socks5://t1.learn.python.ru:1080',
    'urllib3_proxy_kwargs': {'username': 'learn', 'password': 'python'}}

shopping_list = []

def build_menu(buttons, n_cols, header_buttons=None, footer_buttons=None):
    menu = [buttons[i:i + n_cols] for i in range(0, len(buttons), n_cols)]
    if header_buttons:
        menu.insert(0, header_buttons)
    if footer_buttons:
        menu.append(footer_buttons)
    return menu    

def table(bot,update):
    reply_markup =  button_list = [InlineKeyboardButton('Кукуруза', callback_data = 'Кукуруза'),
                                   InlineKeyboardButton('Горошек', callback_data = 'Горошек'),
                                   InlineKeyboardButton('Оливки зеленые', callback_data = 'Оливки зеленые'),
                                   InlineKeyboardButton('Оливки черные', callback_data = 'Оливки черные'),
                                   InlineKeyboardButton('Макароны Макфа', callback_data = 'Макароны Макфа'),
                                   InlineKeyboardButton('Спагетти Макфа', callback_data = 'Спагетти Макфа'),
                                   InlineKeyboardButton('Яблочный сок', callback_data = 'Яблочный сок'),
                                   InlineKeyboardButton('Гранатовый сок', callback_data = 'Гранатовый сок'),
                                   InlineKeyboardButton('Готово', callback_data = 'Готово')
                                   ]
    reply_markup = InlineKeyboardMarkup(build_menu(button_list, n_cols=len(button_list)//4))
    message_text = 'выбирайте продукты'
    bot.send_message(chat_id=ID_CHAT, text=message_text, reply_markup=reply_markup, parse_mode='HTML')

def callbackHandler(bot, update):
    global shopping_list
    user_id = update.callback_query.from_user.id
    user_name = update.callback_query.from_user.name
    print(update.callback_query.data)
    if update.callback_query.data != 'Готово':
        shopping_list.append(update.callback_query.data)
        print(shopping_list)
    else:
        check = core_shopping_list.main(shopping_list)
        text ='В Ашане покупки по данному списку обойдутся в {}, в Metro цена составит {}, а в перекрестке {}'.format(check[0][1],check[1][1], check[2][1])
        shopping_list = []
        bot.send_message(chat_id=ID_CHAT, text=text)
        
            
def main():
    mybot = Updater(API_TOKEN, request_kwargs=PROXY)
    dp = mybot.dispatcher
   # dp.add_handler(CommandHandler('start', insertion))
    dp.add_handler(CommandHandler('start', table))
    clb_handler = CallbackQueryHandler(callbackHandler)
    dp.add_handler(clb_handler)
    #Начало цикла
    mybot.start_polling()
    mybot.idle()
 
if __name__ == "__main__":
    main()