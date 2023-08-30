from cards import *
import json
import csv
from datetime import date
from common import *
from enum import Enum


class GameStatus(Enum):
    STATUS_INIT = "GAME_INIT"
    STATUS_STARTED = "GAME_STARTED"
    STATUS_IN_PROGRESS = "GAME_IN_PROGRESS"
    STATUS_ENDED = "GAME_ENDED"


class GameResult(Enum):
    GAME_WIN = "WIN"
    GAME_FAULT = "FAULT"
    GAME_TIE = "TIE"
    GAME_NOT_ENDED = "NOT_ENDED"


class Game:
    def __init__(
        self,
        bank=1000000,
        wallet=10000,
        hand=[],
        deck=initDeck(),
        bid=0,
        game_status=GameStatus.STATUS_INIT,
        game_result=GameResult.GAME_NOT_ENDED,
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
hand: {self.hand} \n
deck: {self.deck} \n
bid: {self.bid} \n
status: {self.game_status.value} \n
result: {self.game_result} \n
                """

    def shuffleDeck(self):
        self.deck = initDeck()

    def bid_more(self):
        if self.bid >= self.wallet:
            self.bid = 0
            raise BetMoreThanInWallet
        if self.bid >= self.bank:
            self.bid = 0
            raise BetMoreThanInBank
        else:
            self.bid += 100

    def bet(self):
        if self.bid == 0:
            raise EmptyBet
        if self.bank >= self.bid <= self.wallet:
            self.wallet -= self.bid
        else:
            self.bid = 0
            raise BetMoreThanInWallet

    def moreCards(self):
        if len(self.hand) == 8:
            raise ToMuchCards
        elif len(self.deck) > 0:
            next_card = self.deck.pop()
            self.hand.append(next_card)
        else:
            raise EmptyDeck

    def nextGame(self):
        self.hand = []
        self.deck = initDeck()
        self.bid = 0
        self.game_status = GameStatus.STATUS_INIT
        self.game_result = GameResult.GAME_NOT_ENDED

    def recalculate_score(self):
        win, tie, fault = 0, 0, 0
        try:
            with open("./saves/score.csv", "r") as score_file:
                win, tie, fault = [int(i) for i in score_file.readline().split(",")]
        except FileNotFoundError:
            pass
        except ValueError:
            pass
        match self.game_result:
            case "WIN":
                win += 1
            case "FAULT":
                fault += 1
            case "TIE":
                tie += 1
        with open("./saves/score.csv", "w") as score_file:
            score_file.write(f"{win},{tie},{fault}")
        return (
            f"{self.game_result}. Statistic: win - {win}; tie - {tie}; fault - {fault}"
        )

    def add_result_to_history(self):
        list_of_results = []
        read_csv_to_list(list_of_results)
        with open("./saves/results.csv", "w", newline="") as csvfile:
            result_writer = csv.DictWriter(
                csvfile, fieldnames=["date", "bet", "result"]
            )
            current_date = str(date.today())
            bet = str(self.bid)
            result = self.game_result
            list_of_results.insert(
                0, {"date": current_date, "bet": bet, "result": result}
            )
            if len(list_of_results) == 11:
                list_of_results.pop()
            result_writer.writerows(list_of_results)

    def result(self):
        resultValue = 0
        for i in self.hand:
            match i.value:
                case CardValue.TWO:
                    resultValue += 2
                case CardValue.THREE:
                    resultValue += 3
                case CardValue.FOUR:
                    resultValue += 4
                case CardValue.FIVE:
                    resultValue += 5
                case CardValue.SIX:
                    resultValue += 6
                case CardValue.SEVEN:
                    resultValue += 7
                case CardValue.EIGHT:
                    resultValue += 8
                case CardValue.NINE:
                    resultValue += 9
                case CardValue.ACE:
                    resultValue += 11
                case _:
                    resultValue += 10
        if resultValue < 21:
            self.wallet += self.bid
            self.game_result = GameResult.GAME_TIE
        elif resultValue == 21:
            self.wallet += 2 * self.bid
            self.bank -= self.bid
            self.game_result = GameResult.GAME_WIN
        else:
            self.bank += self.bid
            self.game_result = GameResult.GAME_FAULT
        self.game_status = GameStatus.STATUS_ENDED
        self.add_result_to_history()
        return self.recalculate_score()

    def save_game(self):
        to_save = {
            "bank": self.bank,
            "wallet": self.wallet,
            "hand": [str(i) for i in self.hand],
            "game_status": self.game_status.value,
            "game_result": self.game_result.value,
            "bid": self.bid,
        }
        filename = f"./saves/save.save"
        with open(filename, "w") as f:
            json.dump(to_save, f)


def load_game():
    filename = f"./saves/save.save"
    try:
        with open(filename) as f:
            readed_dict = json.load(f)
    except FileNotFoundError:
        return Game()
    readed_dict["hand"] = list(map(to_card, readed_dict["hand"]))
    loaded_game = Game(**readed_dict)
    loaded_game.shuffleDeck()
    for card in loaded_game.hand:
        loaded_game.deck.remove(card)
    return loaded_game


class EmptyBet(Exception):
    message = "Empty bet"


class BetMoreThanInWallet(Exception):
    message = "Too big bet for your wallet"


class ToMuchCards(Exception):
    message = "You don't need more cards"


class EmptyDeck(Exception):
    message = "There are no more cards in the deck"


class BetMoreThanInBank(Exception):
    message = "Too big bet for bank"


# test values
# a = Game()

# card1 = Card(Suit.SPADES, CardValue.TWO)
# card3 = Card(SPADES, "2")
# card2 = Card(Suit.DIAMONDS, CardValue.ACE)
# a.hand = [card1, card2]

# a.deck = []

# print(a)
# a.save_game()


# d = load_game()

# print(d)
# print((d.hand[0]))

# print(card1 == card3)


# print(123)
