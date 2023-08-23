from cards import *


def list_to_string(list):
    result = "["
    for i in list:
        a = i.__str__() + ", "
        result += a
    result += "]"
    return result


class Game:
    def __init__(self, player_name):
        self.player_name = player_name
        self.bank = 1000000
        self.wallet = 10000
        self.hand = []
        self.deck = []
        self.bid = 0
        self.gameStatus = STATUS_INIT
        self.gameResult = "NOT ENDED"

    def __str__(self) -> str:
        return f"""player_name: {self.player_name} \n
                   bank: {self.bank} \n  
                   wallet: {self.wallet} \n
                   hand: {list_to_string(self.hand)} \n
                   deck: {"deck"} \n
                   bid: {self.bid} \n
                   status: {self.gameStatus} \n
                   result: {self.gameResult} \n
                """

    def shuffleDeck(self):
        self.deck = initDeck()
        self.gameStatus = "INGAME"

    def bid_more(self):
        self.bid += 100
        print(f"CURRENT BID {self.bid}")

    def bet(self):
        if self.bid == 0:
            raise EmptyBet
        if self.bank >= self.bid <= self.wallet:
            self.wallet -= self.bid
            print(f"BET {self.bid}")
        else:
            self.bid = 0
            raise BetMoreThanInWallet

    def moreCards(self):
        if len(self.deck) > 0:
            next_card = self.deck.pop()
            self.hand.append(next_card)
            return "DONE"
        else:
            return "EMPTY DECK"

    def nextGame(self):
        self.hand = []
        self.deck = initDeck()
        self.gameStatus = "INIT"
        self.gameResult = "NOT ENDED"

    def result(self):
        resultValue = 0
        for i in self.hand:
            match i.value:
                case "two":
                    resultValue += 2
                case "three":
                    resultValue += 3
                case "four":
                    resultValue += 4
                case "five":
                    resultValue += 5
                case "six":
                    resultValue += 6
                case "seven":
                    resultValue += 7
                case "eight":
                    resultValue += 8
                case "nine":
                    resultValue += 9
                case "ace":
                    resultValue += 11
                case _:
                    resultValue += 10
        if resultValue < 21:
            self.wallet += self.bid
            self.bid = 0
            self.gameStatus = "ENDED"
            self.gameResult = "PUSH"
        elif resultValue == 21:
            self.wallet += 2 * self.bid
            self.bank -= self.bid
            self.bid = 0
            self.gameStatus = "ENDED"
            self.gameResult = "WIN"
        else:
            self.bank += self.bid
            self.bid = 0
            self.gameStatus = "ENDED"
            self.gameResult = "FAULT"


STATUS_INIT = "GAME_INIT"
STATUS_STARTED = "GAME_STARTED"
STATUS_IN_PROGRESS = "GAME_IN_PROGRESS"
STATUS_ENDED = "GAME_ENDED"


class EmptyBet(Exception):
    message = "Empty BET"


class BetMoreThanInWallet(Exception):
    message = "Empty BET"
