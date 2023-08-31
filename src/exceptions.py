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
