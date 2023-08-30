from random import shuffle
import pygame
import sys
import os
from enum import Enum


class Suit(Enum):
    CLUBS = "clubs"
    DIAMONDS = "diamonds"
    HEARTS = "hearts"
    SPADES = "spades"


class CardValue(Enum):
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


class Card:
    def __init__(self, suit: Suit, value: CardValue):
        self.suit = suit
        self.value = value

    def __str__(self):
        return f"{self.suit.value} {self.value.value}"

    def __repr__(self) -> str:
        return str(self)

    def __eq__(self, other):
        if isinstance(other, Card):
            return self.suit == other.suit and self.value == other.value
        return NotImplemented


def to_card(str):
    suit_str, value_str = str.split(" ")
    return Card(Suit(suit_str), CardValue(value_str))


def initDeck():
    tempList = []
    for i in Suit:
        for j in CardValue:
            tempList.append(Card(i, j))
    shuffle(tempList)
    return tempList


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(relative)


def read_card(card: Card):
    card_image_path = resource_path(
        os.path.join(f"./img/cards/{card.suit.value}", f"{card.value.value}.png")
    )
    return pygame.image.load(card_image_path)
