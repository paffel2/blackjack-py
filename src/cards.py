from random import shuffle
import pygame
import sys
import os


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value
        # self.inGameValue = inGameValue
        # self.img = img

    def __str__(self):
        return f"{self.suit[0]} {self.value}"


def to_card(str):
    suit_str, value_str = str.split(" ")
    card = Card(None, None)
    match suit_str:
        case "C":
            card.suit = CLUBS
        case "D":
            card.suit = DIAMONDS
        case "H":
            card.suit = HEARTS
        case "S":
            card.suit = SPADES
    card.value = value_str
    return card


TWO = "2"
THREE = "3"
FOUR = "4"
FIVE = "5"
SIX = "6"
SEVEN = "7"
EIGHT = "8"
NINE = "9"
TEN = "10"
JACK = "J"
QUEEN = "Q"
KING = "K"
ACE = "A"

CLUBS = "clubs"
DIAMONDS = "diamonds"
HEARTS = "hearts"
SPADES = "spades"


def initDeck():
    tempList = []
    for i in [CLUBS, DIAMONDS, HEARTS, SPADES]:
        for j in [
            TWO,
            THREE,
            FOUR,
            FIVE,
            SIX,
            SEVEN,
            EIGHT,
            NINE,
            TEN,
            JACK,
            QUEEN,
            KING,
            ACE,
        ]:
            tempList.append(Card(i, j))
    shuffle(tempList)
    return tempList


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def read_card(card: Card):
    card_image_path = resource_path(
        os.path.join(f"./img/cards/{card.suit}", f"{card.value}.png")
    )
    return pygame.image.load(card_image_path)
