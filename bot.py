import telebot
import config
import blackjack
import random
import db
import webbrowser
from telebot import types

bot = telebot.TeleBot(config.TOKEN)


markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
markup4 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
markup_empty = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
keyboard = types.InlineKeyboardMarkup()

markup_empty.add(types.KeyboardButton(" "))

item1 = types.KeyboardButton("Почати гру")
markup1.add(item1)

item2 = types.KeyboardButton("Ще")
item3 = types.KeyboardButton("Досить")
markup2.add(item2, item3)

item4 = types.KeyboardButton("Ще одна гра")
item5 = types.KeyboardButton("Ні, я пас")
markup3.add(item4, item5)

key_4 = types.InlineKeyboardButton(text='4', callback_data='4')
key_5 = types.InlineKeyboardButton(text='5', callback_data='5')
key_6 = types.InlineKeyboardButton(text='6', callback_data='6')
key_7 = types.InlineKeyboardButton(text='7', callback_data='7')
key_8 = types.InlineKeyboardButton(text='8', callback_data='8')
key_9 = types.InlineKeyboardButton(text='9', callback_data='9')
key_10 = types.InlineKeyboardButton(text='10', callback_data='10')
#key_sh = types.InlineKeyboardButton(text='Shuffle-machine', callback_data='sh')
keyboard.add(key_4,key_5,key_6,key_7,key_8,key_9,key_10)


player = blackjack.Player()
croupier = blackjack.Croupier()
deck = blackjack.Deck()


@bot.message_handler(commands=['logs'])
def get_logs(message):
    bot.send_message(message.chat.id, db.logs(), reply_markup=markup_empty)

@bot.message_handler(commands=['start'])
def start(message):
    if db.get_id(str(message.from_user.id)) is  None :
        db.add(str(message.from_user.id))
        print('add')
    else:
        db.restart(str(message.from_user.id))
        print('restart')
    player.money = db.get_money(str(message.from_user.id))
    bot.send_message(message.chat.id, "Вітаю, {0.first_name}!\nЯ - <b>{1.first_name}</b>, "
                                      "бот для гри BlackJack.".format(message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup1)
    print('{0} has began to play'.format(message.from_user))
    print('has began to play'+str(message.from_user.id))

@bot.message_handler(commands=['help'])
def help(message):
	bot.send_message(message.from_user.id, "Команда /start дозволить почати гру\nКоманда /rules дасть посилання на правила")
@bot.message_handler(commands=['rules'])
def help(message):
    bot.send_message(message.from_user.id,'https://www.pokerstarscasino.com/ua/games/blackjack/rules/?no_redirect=1')

@bot.message_handler(content_types=['text'])
def game_logic(message):

    if message.text == 'Почати гру' or  message.text == "Ще одна гра":
        bot.send_message(message.from_user.id, text= "Окей, поїхали!", reply_markup=markup_empty)
        bot.send_message(message.chat.id, text = "Оберіть кількість колод в грі", reply_markup=keyboard)

    elif message.text.isdigit():
        for i in range(13*croupier.decks * 4):
            croupier.cards.append(i+1)
        db.update_decks(str(message.from_user.id), croupier.decks)

        player.stake = int(message.text)
        db.update_stake(str(message.from_user.id),player.stake)
        player.money = db.get_money(str(message.from_user.id))

        if (player.stake > player.money):
            bot.send_message(message.from_user.id,"У вас немає стільки грошей. Але якщо хочеш зробити велику ставку, я візьму все")
            player.stake = player.money

        player.money -=player.stake
        db.update_money(str(message.from_user.id),player.money)

        player.taken_cards.clear()
        db.update_pl_taken_cards(str(message.from_user.id),'0000000000000')
        croupier.taken_cards.clear()
        db.update_cr_taken_cards(str(message.from_user.id),'0000000000000')
        player.taken_cards.append(random.randrange(0,12,1))
        player.taken_cards.append(random.randrange(0,12,1))
        croupier.taken_cards.append(random.randrange(0,12,1))
        croupier.taken_cards.append(random.randrange(0,12,1))

        croupier.cards[player.taken_cards[0]] -= 1
        croupier.cards[player.taken_cards[1]] -= 1
        croupier.cards[croupier.taken_cards[0]] -= 1
        croupier.cards[croupier.taken_cards[1]] -= 1

        bot.send_message(message.from_user.id,"У вас '" + deck.values[player.taken_cards[0]] + "' та '" + deck.values[player.taken_cards[1]]+ "'")
        bot.send_sticker(message.from_user.id,deck.stickers[player.taken_cards[0]])
        bot.send_sticker(message.from_user.id,deck.stickers[player.taken_cards[1]])
        bot.send_message(message.from_user.id,"Одна з карт круп'є ")
        bot.send_sticker(message.from_user.id,deck.stickers[croupier.taken_cards[0]])
        bot.send_message(message.from_user.id,'Ваша сума: ' + str(player.sum()), reply_markup=markup2)

        if (player.sum() == 21 ):
            player.win = 1
            if player.win:
                bot.send_message(message.from_user.id, "Ви виграли")
                player.win = 0
                player.money += player.stake * 1.5
                db.update_money(str(message.from_user.id), player.money)
        else:
            bot.send_message(message.from_user.id, '*очікую*', reply_markup=markup2)



    elif message.text == "Ще":

        player.taken_cards.append(random.randrange(0,12,1))
#		croupier.cards[player.taken_cards[len(player.taken_cards)-1]] -= 1
        bot.send_message(message.from_user.id, "У вас:")
        for i in player.taken_cards:
            bot.send_sticker(message.from_user.id, deck.stickers[i])
        bot.send_message(message.from_user.id, 'Ваша сума:' + str(player.sum()))

        if (player.sum() < 21):
            bot.send_message(message.from_user.id, '*очікую*', reply_markup=markup2)
            return

        elif (player.sum() == 21 ):
            player.win = 1
            if player.win:
                bot.send_message(message.from_user.id, "Ви виграли")
                player.win = 0
                player.money += player.stake * 1.5
                db.update_money(str(message.from_user.id), player.money)
        else:
            bot.send_message(message.from_user.id,"Багато")
            bot.send_message(message.from_user.id,"Виграв круп'є")
            if (db.get_money(str(message.from_user.id)) < 5):
                bot.send_message(message.chat.id, "У вас немає грошей аби зробити ставку. Почніть заново /start", reply_markup=markup_empty)
                return
            # if croupier.get_cards_num() < croupier.decks*52/3:
            #     bot.send_message(message.from_user.id,"Ще одну гру?", reply_markup = markup3)
            # else:
            #     bot.send_message(message.from_user.id,"Ваша ставка:\nВід 5 до {0}".format(player.money), reply_markup = markup_empty)

        if croupier.get_cards_num() < croupier.decks*52/3:
            bot.send_message(message.from_user.id,"Ще одну гру?", reply_markup = markup3)
        else:
            bot.send_message(message.from_user.id,"Ваша ставка:\nВід 5 до {0}".format(player.money), reply_markup=markup_empty)



    elif message.text == "Досить":
        bot.send_message(message.from_user.id, "Черга круп'є")
        croupier.play()
        bot.send_message(message.from_user.id,"Карти круп'є '")
        for i in croupier.taken_cards:
            bot.send_sticker(message.from_user.id, deck.stickers[i])
        bot.send_message(message.from_user.id, "Сума круп'є:" + str(croupier.sum()))

        if croupier.sum() <= player.sum() and player.sum() <21 or croupier.sum() > 21:
            player.win = 1

        if player.win:
            bot.send_message(message.from_user.id,"Ви виграли")
            player.win = 0
            player.money+=player.stake*1.5
            db.update_money(str(message.from_user.id), player.money)
        else:
            bot.send_message(message.from_user.id,"Виграв круп'є")
            if (db.get_money(str(message.from_user.id)) < 5):
                bot.send_message(message.chat.id, "У вас немає грошей аби зробити ставку. Почніть заново /start", reply_markup=markup_empty)
                return

        if croupier.get_cards_num() < croupier.decks*52/3:
            bot.send_message(message.from_user.id,"Ще одну гру?", reply_markup = markup3)
        else:
            bot.send_message(message.from_user.id,"Ваша ставка:\nВід 5 до {0}".format(player.money), reply_markup=markup_empty)



    elif message.text == "Ні, я пас":
        bot.send_message(message.from_user.id, "Як надумаєте повернутися, напишіть /start", reply_markup=markup_empty)



    else:
        bot.send_message(message.from_user.id, "Я не розумію, що саме я не розумію. Напиши /help.", reply_markup=markup_empty)



@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):

    if call.data == '4':
        croupier.decks = 4
    elif call.data == '5':
        croupier.decks = 5
    elif call.data == '6':
        croupier.decks = 6
    elif call.data == '7':
        croupier.decks = 7
    elif call.data == '8':
        croupier.decks = 8
    elif call.data == '9':
        croupier.decks = 9
    elif call.data == '10':
        croupier.decks = 10
    bot.send_message(call.message.chat.id, "Гра з {0} колодами карт".format(croupier.decks))
    bot.send_message(call.message.chat.id, "Ваш баланс: {0}$".format(player.money))
    bot.send_message(call.message.chat.id, "Ваша ставка:\nВід 5 до {0}".format(player.money))



bot.polling(none_stop=True)
# RUN
