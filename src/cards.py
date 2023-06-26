from random import shuffle

class Card(object):
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        #self.inGameValue = inGameValue
        #self.img = img
    def __str__(self):
        return f"(Card: Suit: {self.suit} Value: {self.value})"

TWO = "two"
THREE = 'three'
FOUR = 'four'
FIVE = 'five'
SIX = 'six'
SEVEN = 'seven'
EIGHT = 'eight'
NINE = 'nine'
TEN = 'ten'
JACK = 'jack'
QUEEN = 'queen'
KING = 'king'
ACE = 'ace'

CLUBS = 'clubs'
DIAMONDS = 'diamonds'
HEARTS = 'hearts'
SPADES = 'spades'



def initDeck():
    tempList = []
    for i in [CLUBS,DIAMONDS,HEARTS,SPADES]:
        for j in [TWO, THREE,FOUR,FIVE,SIX,SEVEN,EIGHT,NINE,TEN,JACK,QUEEN,KING,ACE]:
            tempList.append(Card(i,j))
    shuffle(tempList)
    return tempList

