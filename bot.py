import telebot
from telebot import types
from telebot.types import InputMediaPhoto
import os
import time
import argparse


TOKEN = ""
bot = telebot.TeleBot(TOKEN)

imgs = []
img_name = {}
flag = False

@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Отправить")
    markup.add(item1)
    bot.send_message(m.chat.id, 'Если хочешь отдать вещь: \nПришли фото с её описанием.\nИ нажми отправить.',reply_markup=markup)





@bot.message_handler(content_types=["text"])
def massage_reply(message):
    global flag
    global imgs
    global img_name

    user_id = message.chat.id

    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add("Отправить")
    markup.add("Сбросить")


    if message.text == "Отправить" and flag == True:
        print("-"*10 + "True")
        flag = False

        mention = f'<a href="tg://user?id={message.chat.id}">{message.chat.first_name} {message.chat.last_name}</a>'
        bot.send_message(CHANAL_NAME, f'Вещи от {mention}', parse_mode="HTML") 
        bot.send_media_group(CHANAL_NAME,imgs)
        bot.send_message(user_id, f'Публикация отправлена в канал {CHANAL_NAME}\n\nБудем ждать что твои вещи пригодятся.')
        bot.send_message(user_id, 'Если хочешь поделиться чем-то ещё: \nПришли фото с её описанием.\nИ нажми отправить.',reply_markup=markup)
        
        for  name in img_name:
            img_name[name][0].close()
            os.remove(name)
        imgs = []
        img_name = {}

    elif message.text == "Отправить" and flag == False or message.text == "Да":
        print("-"*10 + "False")
        flag = True
        bot.send_message(user_id, "Ваш пост с вещами:")
        bot.send_media_group(user_id,imgs)
        bot.send_message(user_id, "Для подтверждения нажмите отправить, в противном случае сбросить", reply_markup= markup)
        
        imgs = []
        for name in img_name:
            img_name[name][0].close()
            img = open(name, 'rb')
            imgs.append(InputMediaPhoto(img, caption=img_name[name][1]))
            img_name[name][0] = img

    
    elif message.text == "Сбросить":
        print("-"*10 + "Сбросить")
        flag = False

        bot.send_message(user_id, 'Если хочешь отдать вещь: \nПришли фото с её описанием.\nИ нажми отправить',reply_markup=markup)

        for  name in img_name:
            img_name[name][0].close()
            os.remove(name)
        imgs = []
        img_name = {}
    else:
        markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        markup.add("Да")
        markup.add("Сбросить")
        bot.send_message(user_id, 'Добавить описание к фото?')
        bot.send_message(user_id, message.text,reply_markup=markup)
        imgs[0].caption = message.text
        img_name[list(img_name.keys())[0]][1] = message.text



@bot.message_handler(content_types=["photo"])
def massage_reply(message):
    if message.content_type == 'photo':
        raw = message.photo[2].file_id
        description = message.caption
        name = raw+".jpg"
        file_info = bot.get_file(raw)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(name,'wb') as new_file:
            new_file.write(downloaded_file)
        img = open(name, 'rb')
        imgs.append(InputMediaPhoto(img, caption=description))
        img_name[name] = [img, description]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Конфигурация бота")
    parser.add_argument('--chanal','-c',type=str, help="Имя канала")
    args = parser.parse_args()
    
    CHANAL_NAME = args.chanal  
    bot.infinity_polling()