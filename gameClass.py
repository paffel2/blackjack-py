from cards import *
class Game(object):
    def __init__(self, player_name):
        self.player_name = player_name
        self.bank = 1000000
        self.wallet = 10000
        self.hand = []
        self.deck = []
        self.bid = 0
        self.gameStatus = "INIT"
        self.gameResult = 'NOT ENDED'
    
    def shuffleDeck(self):
        self.deck = initDeck()
        self.gameStatus = 'INGAME'
    
    def bidMore(self,value):
        if value >= self.wallet:
            self.bid += value
            self.wallet -= value
            self.gameStatus = 'INGAME'
            return "DONE"
        else:
            self.gameStatus = 'INGAME'
            return "NO MONEY" # TO DO добавить обработку исключений
    
    def moreCards(self):
        if len(self.deck) > 0:
            next_card = self.deck.pop()
            self.hand.append(next_card)
            return 'DONE'
        else:
            return 'EMPTY DECK'
    
    def nextGame(self):
        self.hand = []
        self.deck = initDeck()
        self.gameStatus = "INIT"
        self.gameResult = 'NOT ENDED'
    
    def result(self):
        resultValue = 0
        for i in self.hand:
            match i.value:
                case 'two':
                    resultValue += 2
                case 'three':
                    resultValue += 3
                case 'four':
                    resultValue += 4
                case 'five':
                    resultValue += 5 
                case 'six':
                    resultValue += 6
                case 'seven':
                    resultValue += 7 
                case 'eight':
                    resultValue += 8
                case 'nine':
                    resultValue += 9 
                case 'ace':
                    resultValue += 11
                case _:
                    resultValue += 10
        if resultValue < 21:
            self.wallet += self.bid
            self.bid = 0
            self.gameStatus = 'ENDED'
            self.gameResult = 'PUSH'
        elif resultValue == 21:
            self.wallet += 2 * self.bid
            self.bank -= self.bid
            self.bid = 0
            self.gameStatus = 'ENDED'
            self.gameResult = 'PUSH'
        else:
            self.bank += self.bid
            self.bid = 0
            self.gameStatus = 'ENDED'
            self.gameResult = 'PUSH'
    