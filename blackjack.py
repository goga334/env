import random
import config


class Deck:
    
    values = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'Валет', 'Дама', 'Король', 'Туз']
    weight = {
        0: 2,
        1: 3,
        2: 4,
        3: 5,
        4: 6,
        5: 7,
        6: 8,
        7: 9,
        8: 10,
        9: 10,
        10: 10,
        11: 10,
        12: 1
    }
    stickers = [ config.sticker_id_2,
                 config.sticker_id_3,
                 config.sticker_id_4,
                 config.sticker_id_5,
                 config.sticker_id_6,
                 config.sticker_id_7,
                 config.sticker_id_8,
                 config.sticker_id_9,
                 config.sticker_id_10,
                 config.sticker_id_jack,
                 config.sticker_id_queen,
                 config.sticker_id_king,
                 config.sticker_id_ace
                 ]

    def sum(self):
        sum=0
        for i in self.taken_cards:
            sum += self.weight[i]
            if (i == 'Ace' and sum <= 10 ):
                sum+=10
        return sum

    def take_card(self):     
        self.taken_cards.append(random.randrange(0,12,1))


           

class Player(Deck):
    money = 0
    taken_cards = list()
    stake = 0
    win = 0
    
    
class Croupier(Deck):
    decks = 0
    cards = list()
    taken_cards = list()
    
    def get_cards_num(self):
        num = 0
        for i in self.cards:
            num +=i
        return num

    def play(self):
        while (self.sum() <17):
            self.taken_cards.append(random.randrange(0,12,1))
            self.cards[self.taken_cards[len(self.taken_cards)-1]] -= 1



