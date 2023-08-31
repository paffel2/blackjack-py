from game_class import *
import unittest
from exceptions import *


class TestGameClass(unittest.TestCase):
    def test_init(self):
        default_game = Game(
            1000000, 10000, [], [], 0, GameStatus.STATUS_INIT, GameResult.GAME_NOT_ENDED
        )
        self.assertEqual(Game(), default_game)

    def test_shuffle_deck(self):
        game = Game()
        game1 = Game()
        game.shuffleDeck()
        self.assertNotEqual(len(game.deck), len(game1.deck))

    def test_shuffle_deck_len_of_deck(self):
        game = Game()
        game.shuffleDeck()
        self.assertEqual(len(game.deck), 52)

    def test_bid_more_is_ok(self):
        game = Game()
        game.bid_more()
        self.assertEqual(game.bid, 100)

    def test_bid_more_no_money_in_wallet(self):
        game = Game(wallet=0)
        self.assertRaises(BetMoreThanInWallet, game.bid_more)

    def test_bid_more_no_money_in_bank(self):
        game = Game(bank=0)
        self.assertRaises(BetMoreThanInBank, game.bid_more)

    def test_bet_is_ok(self):
        game = Game()
        game.bid_more()
        game.bet()
        self.assertEqual(game.wallet, 9900)

    def test_bet_is_null(self):
        game = Game()
        self.assertRaises(EmptyBet, game.bet)

    def test_more_cards_deck_is_empty(self):
        game = Game()
        self.assertRaises(EmptyDeck, game.moreCards)

    def test_result_win(self):
        hand = [Card(Suit.CLUBS, CardValue.ACE), Card(Suit.DIAMONDS, CardValue.TEN)]
        bid = 1000
        game = Game(hand=hand, bid=bid)
        game.result()
        self.assertEqual(game.game_result, GameResult.GAME_WIN)

    def test_result_fault(self):
        hand = [Card(Suit.CLUBS, CardValue.ACE), Card(Suit.DIAMONDS, CardValue.ACE)]
        bid = 1000
        game = Game(hand=hand, bid=bid)
        game.result()
        self.assertEqual(game.game_result, GameResult.GAME_FAULT)

    def test_result_tie(self):
        hand = [Card(Suit.CLUBS, CardValue.ACE), Card(Suit.DIAMONDS, CardValue.SIX)]
        bid = 1000
        game = Game(hand=hand, bid=bid)
        game.result()
        self.assertEqual(game.game_result, GameResult.GAME_TIE)

    def test_more_cards(self):
        a = Game()
        a.shuffleDeck()
        head_card = a.deck[0]
        a.moreCards()
        card_in_hand = a.hand[0]
        self.assertEqual(head_card, card_in_hand)

    def test_more_cards_to_much_cards_in_hand(self):
        b = Game()
        b.shuffleDeck()
        for _ in range(0, 7):
            b.moreCards()
        self.assertRaises(ToMuchCards, b.moreCards)

    def test_anext_game(self):
        game2 = Game()
        game1 = Game()
        game1.nextGame()
        self.assertEqual(game2, game1)


if __name__ == "__main__":
    unittest.main()
