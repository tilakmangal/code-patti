from base_bot import BaseBot
from rules import Rules

class Player(BaseBot):
    def choose_card(self, top_card):
        # This is intentionally left simple for competition participants to implement their strategy.
        # They have access to self.hand and the top_card.
        # Example:
        #   top_card = "R5"
        #   self.hand = ["B2", "RS", "WC", "Y4", ...]

        # Participants should return a valid card from self.hand or None if no playable card.
        return None


# For local testing only
if __name__ == "__main__":
    bot = Player(player_id=0)

    # Example input
    bot.hand = input("Enter your hand as space-separated cards: ").strip().split()
    top_card = input("Enter the top card: ").strip()

    move = bot.choose_card(top_card)
    print(f"Chosen card: {move}")
