import telebot
import config
import blackjack
import random
 
from telebot import types
 
bot = telebot.TeleBot(config.TOKEN)
markup1 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
markup3 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
markup_empty = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard = True)
keyboard = types.InlineKeyboardMarkup()


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




@bot.message_handler(commands=['start'])
def welcome(message):

	option1 = ''
	option2 = ''
	print ("{0.first_name} has began to play".format(message.from_user))

	bot.send_message(message.chat.id, "Вітаю, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот для гри BlackJack.".format(message.from_user, bot.get_me()),
		parse_mode='html', reply_markup=markup1)
 



@bot.message_handler(content_types=['text'])
def get_deck(message):

	if message.text == 'Почати гру' or  message.text == "Ще одна гра":
		if (player.money < 5):
			bot.send_message(message.chat.id,"У вас немає грошей аби зробити ставку. Почніть заново")
		bot.send_message(message.chat.id, text = "Оберіть кількість колод в грі", reply_markup=keyboard)

	elif message.text == "/help":
		bot.send_message(message.from_user.id, "Напишіть /start")

	elif message.text.isdigit():

		player.stake = int(message.text)

		if (player.stake > player.money):
			bot.send_message(message.from_user.id,"У вас немає стільки грошей. Але якщо хочеш зробити велику ставку, я візьму все")
			player.stake = player.money

		player.money -=player.stake
		player.taken_cards.clear()
		croupier.taken_cards.clear()
		player.taken_cards.append(random.randrange(0,12,1))
		player.taken_cards.append(random.randrange(0,12,1))
		croupier.taken_cards.append(random.randrange(0,12,1))
		croupier.taken_cards.append(random.randrange(0,12,1))

		croupier.cards[player.taken_cards[0]] -= 1
		croupier.cards[player.taken_cards[1]] -= 1
		croupier.cards[croupier.taken_cards[0]] -= 1
		croupier.cards[croupier.taken_cards[1]] -= 1

		bot.send_message(message.from_user.id,"У вас '" + deck.values[player.taken_cards[0]] + "' та '" + deck.values[player.taken_cards[1]]+ "'")
		bot.send_message(message.from_user.id,"Одна з карт круп'є '" + deck.values[croupier.taken_cards[0]]+ "'")
		bot.send_message(message.from_user.id,'Ваша сума: ' + str(player.sum()), reply_markup = markup2)
		if (player.sum() == 21 ):
			player.win = 1
			if player.win:
				bot.send_message(message.from_user.id, "Ви виграли")
				player.win = 0
				player.money += player.stake * 1.5
		else:
			bot.send_message(message.from_user.id, '*очікую*', reply_markup=markup2)

	elif message.text == "Ще":
		player.taken_cards.append(random.randrange(0,12,1))
		croupier.cards[player.taken_cards[len(player.taken_cards)-1]] -= 1
		bot.send_message(message.from_user.id, "У вас:")
		for i in player.taken_cards:
			bot.send_message(message.from_user.id, deck.values[i])
		bot.send_message(message.from_user.id, 'Ваша сума:' + str(player.sum()))

		if (player.sum() < 21):
			bot.send_message(message.from_user.id, '*очікую*', reply_markup=markup2)
		elif (player.sum() == 21 ):
			player.win = 1
			if player.win:
				bot.send_message(message.from_user.id, "Ви виграли")
				player.win = 0
				player.money += player.stake * 1.5
		else:
			bot.send_message(message.from_user.id,"Багато")
			bot.send_message(message.from_user.id,"Виграв круп'є")
		if croupier.get_cards_num() < croupier.decks*52/3:
			bot.send_message(message.from_user.id,"Ще одну гру?", reply_markup = markup3)
		else:
			bot.send_message(message.from_user.id,"Ваша ставка:\nВід 5 до {0}".format(player.money), reply_markup = markup_empty)


	elif message.text == "Досить":
		bot.send_message(message.from_user.id, "Черга круп'є")
		croupier.play()
		bot.send_message(message.from_user.id,"Карти круп'є '")
		for i in croupier.taken_cards:
			bot.send_message(message.from_user.id, deck.values[i])
		bot.send_message(message.from_user.id, "Сума круп'є":' + str(croupier.sum()))

		if croupier.sum() <= player.sum() and player.sum() <21 or croupier.sum() > 21:
			player.win = 1

		if player.win:
			bot.send_message(message.from_user.id,"Ви виграли")
			player.win = 0
			player.money+=player.stake*1.5
		else:
			bot.send_message(message.from_user.id,"Виграв круп'є")

		if croupier.get_cards_num() < croupier.decks*52/3:
			bot.send_message(message.from_user.id,"Ще одну гру?", reply_markup = markup3)
		else:
			bot.send_message(message.from_user.id,"Ваша ставка:\nВід 5 до {0}".format(player.money))

	elif message.text == "Ні, я пас":
		bot.send_message(message.from_user.id, "Як надумаєте повернутися, напишіть /start")

	else:
		bot.send_message(message.from_user.id, "Я не розумію, що саме я не розумію. Напиши /help.")



@bot.callback_query_handler(func=lambda call: True)

def callback_worker(call):

	if call.data == '4' :
		croupier.decks = 4
	elif call.data == '5' :
		croupier.decks = 5
	elif call.data == '6' :
		croupier.decks = 6
	elif call.data == '7' :
		croupier.decks = 7
	elif call.data == '8' :
		croupier.decks = 8
	elif call.data == '9' :
		croupier.decks = 9
	elif call.data == '10' :
		croupier.decks = 10
	bot.send_message(call.message.chat.id, "Гра з {0} колодами карт".format(croupier.decks))

	for i in range(13):
		croupier.cards.append(croupier.decks*4)
	bot.send_message(call.message.chat.id, "Ваш баланс: {0}$".format(player.money))
	bot.send_message(call.message.chat.id, "Ваша ставка:\nВід 5 до {0}".format(player.money))



bot.polling(none_stop=True)
# RUN
