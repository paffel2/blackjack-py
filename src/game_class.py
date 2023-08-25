from cards import *
import json

STATUS_INIT = "GAME_INIT"
STATUS_STARTED = "GAME_STARTED"
STATUS_IN_PROGRESS = "GAME_IN_PROGRESS"
STATUS_ENDED = "GAME_ENDED"


def list_to_string(list):
    result = "["
    for i in list:
        a = i.__str__() + ", "
        result += a
    result += "]"
    return result


class Game:
    def __init__(
        self,
        bank=1000000,
        wallet=10000,
        hand=[],
        deck=[],
        bid=0,
        game_status=STATUS_INIT,
        game_result="NOT ENDED",
    ):
        self.bank = bank
        self.wallet = wallet
        self.hand = hand
        self.deck = deck
        self.bid = bid
        self.game_status = game_status
        self.game_result = game_result

    def __str__(self) -> str:
        return f""" GAME:
bank: {self.bank} \n  
wallet: {self.wallet} \n
hand: {list_to_string(self.hand)} \n
deck: {list_to_string(self.deck)} \n
bid: {self.bid} \n
status: {self.game_status} \n
result: {self.game_result} \n
                """

    def shuffleDeck(self):
        self.deck = initDeck()
        self.game_status = "INGAME"

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
        if len(self.hand) == 8:
            raise ToMuchCards
        elif len(self.deck) > 0:
            next_card = self.deck.pop()
            self.hand.append(next_card)
            return "DONE"
        else:
            return "EMPTY DECK"

    def nextGame(self):
        self.hand = []
        self.deck = initDeck()
        self.game_status = "INIT"
        self.game_result = "NOT ENDED"

    def result(self):
        resultValue = 0
        for i in self.hand:
            match i.value:
                case "2":
                    resultValue += 2
                case "3":
                    resultValue += 3
                case "4":
                    resultValue += 4
                case "5":
                    resultValue += 5
                case "6":
                    resultValue += 6
                case "7":
                    resultValue += 7
                case "8":
                    resultValue += 8
                case "9":
                    resultValue += 9
                case "A":
                    resultValue += 11
                case _:
                    resultValue += 10
        print(f"result_value: {resultValue}")
        if resultValue < 21:
            self.wallet += self.bid
            self.bid = 0
            self.game_status = "ENDED"
            self.game_result = "PUSH"
        elif resultValue == 21:
            self.wallet += 2 * self.bid
            self.bank -= self.bid
            self.bid = 0
            self.game_status = "ENDED"
            self.game_result = "WIN"
        else:
            self.bank += self.bid
            self.bid = 0
            self.game_status = "ENDED"
            self.game_result = "FAULT"

    def save_game(self):
        to_save = {
            "bank": self.bank,
            "wallet": self.wallet,
            "hand": [str(i) for i in self.hand],
            "game_status": self.game_status,
            "game_result": self.game_result,
        }
        filename = f"saves/save.save"
        with open(filename, "w") as f:
            json.dump(to_save, f)
        f.close()


def load_game():
    filename = f"saves/save.save"
    with open(filename) as f:
        readed_dict = json.load(f)
    readed_dict["hand"] = list(map(to_card, readed_dict["hand"]))
    f.close()
    return Game(**readed_dict)


class EmptyBet(Exception):
    message = "Empty BET"


class BetMoreThanInWallet(Exception):
    message = "Empty BET"


class ToMuchCards(Exception):
    message = "I don't need more cards"


# test values
# a = Game()

# card1 = Card(SPADES, "2")
# card2 = Card(DIAMONDS, "A")
# a.hand = [card1, card2]

# print(a)
# a.save_game()


# d = load_game()

# print(d)
# print((d.hand[0]))
