from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CommandHandler
from telegram.ext import ConversationHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import CallbackContext
from telegram.ext.filters import Filters

from telegram import ReplyKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram import InlineKeyboardMarkup
from telegram import Update

from telegram.chataction import ChatAction


Token = "6646963907:AAHuru4PeoRVzhj4PWoEil-Q1V4463eA5Jg"
message= {
    "msg_start":"سلام {} {} \n به ربات رسمی سامان بان خوش آمدید",
    "msg_menu1":"یک",
    "msg_menu2":"دو",
    "msg_menu3":"سه",
    "msg_menu4":"چهار",
    


}

Conversation = {}
First, Second = range(2)

def start_handler(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    first_name = update.message.chat.first_name
    last_name = update.message.chat.last_name
    context.bot.send_chat_action(chat_id, ChatAction.TYPING)
    if last_name == None:
        last_name = "عزیز"
    update.message.reply_text(text=message["msg_start"].format(first_name,last_name))
    main_menu_handler(update,context)


def main_menu_handler(update: Update, context:CallbackContext):
    buttons = [
        [message["msg_menu1"]],
        [message["msg_menu2"],message["msg_menu3"]],
        [message["msg_menu4"]]
    ]

    update.message.reply_text(
        text="منو اصلی \n یکی از گزینه های زیر را انتخاب کنید", 
        reply_markup=ReplyKeyboardMarkup(buttons, resize_keyboard=True)
    )

def return_handler(update: Update, context: CallbackContext):
    main_menu_handler(update, context)


def link_handler(update: Update, context:CallbackContext):
    buttons = [
    [
        InlineKeyboardButton("فیلیشا",callback_data="filisha"),
        InlineKeyboardButton("سامان بان",callback_data="samanban")
    ]
    ]
    update.message.reply_text(
        text="صفحه مورد نظر را انتخاب کنید",
        reply_markup=InlineKeyboardMarkup(buttons)
    )

def end_link_handler(update: Update, context:CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if data == "filisha":
        text= "شما سایت فیلیشا را انتخاب کرده اید"
    else :
        text= "شما سایت سامان بان را انتخاب کرده اید"
    context.bot.editMessageText(text=text, chat_id=chat_id, message_id=message_id)

def glass_handler(update: Update, context:CallbackContext):
    buttons = [
        [
            InlineKeyboardButton("برنامه نویس", callback_data="programmer"),
            InlineKeyboardButton("گرافیک دیزاینر", callback_data="designer")
        ] 
    ]
    update.message.reply_text(
        text="شغل مورد نظرخود را واردکنید",
        reply_markup=InlineKeyboardMarkup(buttons)
    )
    return First

def programmer_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    buttons =[
        [
        InlineKeyboardButton("vs code", callback_data="vs code \n :لینک دانلود"),
        InlineKeyboardButton("pycharm", callback_data="pycharm \n :لینک دانلود"),
        InlineKeyboardButton("atom", callback_data="atom \n :لینک دانلود")
        ]
    ]
    context.bot.editMessageText(text= " کامپایلر مورد نظر را انتخاب کنید",
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(buttons))
    return Second


def designer_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    buttons =[
        [
        InlineKeyboardButton("photoshop", callback_data="photoshop"),
        InlineKeyboardButton("paint", callback_data="paint"),
        InlineKeyboardButton("picsart", callback_data="picsart")
        ]
    ]
    context.bot.editMessageText(text= "ادیتور عکس خود را انتخاب کنید",
                                chat_id=chat_id,
                                message_id=message_id,
                                reply_markup=InlineKeyboardMarkup(buttons))
    return Second

def end_handler(update: Update, context:CallbackContext):
    global Conversation
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    Conversation[chat_id] = data
    context.bot.editMessageText(
        text="{} نرم افزار مورد نیاز شما است".format(Conversation[chat_id]),
        chat_id=chat_id,
        message_id=message_id
    )
    return ConversationHandler.END



def main():
    updater = Updater(Token, use_context= True)
    conversation_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex(message["msg_menu2"]), glass_handler)],
        states={
            First: [CallbackQueryHandler(programmer_handler, pattern="^programmer$"),
                    CallbackQueryHandler(designer_handler, pattern="^designer$")],
            Second: [CallbackQueryHandler(end_handler)]
        },
        fallbacks=[MessageHandler(Filters.regex(message["msg_menu2"]), glass_handler)],
        allow_reentry=True
    )
    updater.dispatcher.add_handler(conversation_handler)
    updater.dispatcher.add_handler(CommandHandler("Start", start_handler))

    updater.dispatcher.add_handler(CallbackQueryHandler(end_link_handler))

    updater.dispatcher.add_handler(MessageHandler(Filters.regex("menu"), main_menu_handler))
    #updater.dispatcher.add_handler(MessageHandler(Filters.regex(message["msg_menu4"]), return_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.regex(message["msg_menu1"]), link_handler))
    



    updater.start_polling()
    updater.idle()



main()


    

