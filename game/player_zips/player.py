
from utils import is_next_uno, is_any_uno, draw_cards
from deck import Deck

class Player:
    def __init__(self, player_id, deck):
        """Initialize a player with an ID and a starting hand."""
        self.player_id = player_id
        self.hand = [deck.draw_card() for _ in range(7)]

    def get_card_count(self):
        """Return the number of cards the player has."""
        return len(self.hand)

    def draw_card(self, deck, num_cards=1):
        """Draw a specified number of cards into the player's hand."""
        draw_cards(deck, self.hand, num_cards)

    def choose_card(self, top_card, game_state):
        """
        Participant's logic to choose a card to play.
        This is where their strategy can go.
        Currently plays the first valid card found.
        """
        for card in self.hand:
            if game_state.rules.is_valid_move(card, top_card):
                return card
        return None  # Draw a card if no valid move

    def play_card(self, card, top_card, game_state):
        """Attempt to play a card. If invalid, draw a card."""
        if card in self.hand and game_state.rules.is_valid_move(card, top_card):
            self.hand.remove(card)
            game_state.played_cards.append(card)
            game_state.rules.apply_card_effect(card, game_state)

            if self.has_uno():
                print(f"⚠ Player {self.player_id} has UNO! ⚠")
            return True
        else:
            print(f"Invalid move! Player {self.player_id} draws a card.")
            self.draw_card(game_state.deck)
            return False

    def has_uno(self):
        """Return True if player has only one card left."""
        return len(self.hand) == 1

    def __str__(self):
        """Return string representation of the player's hand."""
        return f"Player {self.player_id} hand: {self.hand}"


# Example standalone usage (test)
if __name__ == "__main__":
    deck = Deck()
    player = Player(0, deck)
    print(player)
    player.draw_card(deck)
    print(player)
