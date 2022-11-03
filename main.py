import os
my_secret = os.environ['API_KEY']
import httpx
import json
import telebot

bot = telebot.TeleBot(my_secret)

@bot.message_handler(commands=['start'])
def greet(message):
  bot.send_message(message.chat.id, 'use /command to know about all available commands to use in order to get various facts about your fav🧡 country')

@bot.message_handler(commands=['command'])
def command(message):
  reply = """ in these commands you don't need to use / 
              before commands and commands consist of 
              2️⃣ parts (ex: flag india):
              (i) data you want to know about that
                  country
              (ii) name of country

              

              commands👇👇👇(don't use -> before commands)
              
              -> currencies {country_name} - country currency
              
              -> capital {country_name} - country's capital
              
              -> languages {country_name} - country's 
               languages
              
              -> flag {country_name} - flag of the country

              -> region {country_name} - region in which 
              country is situated

              -> unMember {country_name} - to check if the 
                country is the member of united nations

              -> independent {country_name} - to know if 
                 the country is independent or not

              -> games play - if you really want to
               explore and know more about other countries
               use this commands to get games related to 
               countries
              """
  
  bot.send_message(message.chat.id, reply)
info = ['capital','currencies','languages','flag','region','unMember','independent','games']

def country_request(message):
  request = message.text.split()
  if len(request) < 2 or request[0] not in info:
    bot.send_message(message.chat.id, 'wrong keyword entered before country name. Use /command know all available command')
    return False
  else:
    return True

@bot.message_handler(func = country_request)
def send_info(message):
  request = message.text.split()[1]
  data_need = message.text.split()[0]

  if request == 'play':
    bot.reply_to(message, """here are some links to play countries related games
                             
                - 'https://www.sporcle.com/games/g/world?t=country'
                - 'https://www.britannica.com/quiz/the-country-quiz' """)

  else:
    data = httpx.get(f'https://restcountries.com/v3.1/name/{request}')
    if data.status_code == 200:
      data_json = data.json()
      request_reply = data_json[0][data_need]
      if data_need == 'languages':
        for i in list(request_reply.values()):
          bot.send_message(message.chat.id, i)
      else:
        bot.send_message(message.chat.id, request_reply)
    elif data.status_code == 404:
      bot.send_message(message.chat.id,'country not found')
    else:
      bot.send_message(message.chat.id,'😬error occured❗,Check country name    again')

bot.polling()