
import importlib.util
import os
import zipfile
from game import Game

def load_bot(filepath, class_name, player_id):
    """Dynamically load a bot/player from a file."""
    spec = importlib.util.spec_from_file_location(f"bot{player_id}", filepath)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    bot_class = getattr(module, class_name)
    return bot_class(player_id)

def extract_and_load_bots(zip_path):
    """Extract the bot zip and return a list of bot instances."""
    extract_path = "player_zips"
    if os.path.exists(extract_path):
        # clear old bots
        for f in os.listdir(extract_path):
            os.remove(os.path.join(extract_path, f))
    else:
        os.makedirs(extract_path)

    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_path)

    # Define mapping of bot filename to class name
    bot_files = [
        ("botAlpha.py", "botAlpha"),
        ("botBravo.py", "botBravo"),
        ("botCharlie.py", "botCharlie"),
        ("player.py", "Player"),  # human participant
    ]

    bots = []
    for i, (filename, class_name) in enumerate(bot_files):
        filepath = os.path.join(extract_path, filename)
        bot_instance = load_bot(filepath, class_name, player_id=i)
        bots.append(bot_instance)

    return bots

def main():
    bots = extract_and_load_bots("players.zip")
    game = Game(bots=bots)
    
    print("Starting game...")
    while not game.is_over():
        print(f"Top card: {game.top_card}")
        for pid, player in game.players.items():
            print(f"Player {pid} has {len(player.hand)} cards: {player.hand}")

        current_bot = game.players[game.current_player]
        move = current_bot.choose_card(current_bot.hand, game.top_card)
        
        if move:
            print(f"Player {game.current_player} plays {move}")
            game.play_card(game.current_player, move)
        else:
            print(f"Player {game.current_player} draws a card")
            current_bot.draw_card(game.deck)
        
        game.next_turn()

    print("Game over!")
    print(f"Winner: Player {game.get_winner()}")

if __name__ == "__main__":
    main()
