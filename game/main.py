from game_engine import Game
from playerBot import Player as PlayerBot
from practice_bot import PracticeBot
import random


def main():
    game = Game()
    print("""██╗███████╗███████╗███████╗    ███╗   ███╗███████╗██████╗     
██║██╔════╝██╔════╝██╔════╝    ████╗ ████║██╔════╝██╔══██╗    
██║█████╗  █████╗  █████╗      ██╔████╔██║███████╗██████╔╝    
██║██╔══╝  ██╔══╝  ██╔══╝      ██║╚██╔╝██║╚════██║██╔══██╗    
██║███████╗███████╗███████╗    ██║ ╚═╝ ██║███████║██████╔╝    
╚═╝╚══════╝╚══════╝╚══════╝    ╚═╝     ╚═╝╚══════╝╚═════╝    """)
    
    print(""" ___    _____  ___    ___            ___    _____  _____  _____  _ 
(  _`\ (  _  )(  _`\ (  _`\         (  _`\ (  _  )(_   _)(_   _)(_)
| ( (_)| ( ) || | ) || (_(_) ______ | |_) )| (_) |  | |    | |  | |
| |  _ | | | || | | )|  _)_ (______)| ,__/'|  _  |  | |    | |  | |
| (_( )| (_) || |_) || (_( )        | |    | | | |  | |    | |  | |
(____/'(_____)(____/'(____/'        (_)    (_) (_)  (_)    (_)  (_)
                                                                   
                                                                   """)
    print(""" _____ _                        _                   _ _            _         _                _             _             
|_   _| |__   ___    ___  _ __ | |_   _    ___ _ __(_) |_ ___ _ __(_) __ _  (_)___  __      _(_)_ __  _ __ (_)_ __   __ _ 
  | | | '_ \ / _ \  / _ \| '_ \| | | | |  / __| '__| | __/ _ \ '__| |/ _` | | / __| \ \ /\ / / | '_ \| '_ \| | '_ \ / _` |
  | | | | | |  __/ | (_) | | | | | |_| | | (__| |  | | ||  __/ |  | | (_| | | \__ \  \ V  V /| | | | | | | | | | | | (_| |
  |_| |_| |_|\___|  \___/|_| |_|_|\__, |  \___|_|  |_|\__\___|_|  |_|\__,_| |_|___/   \_/\_/ |_|_| |_|_| |_|_|_| |_|\__, |
                                  |___/                                                                             |___/ """)

    bots = {
        0: PlayerBot(0),
        1: PracticeBot(1),
        2: PracticeBot(2),
        3: PracticeBot(3)
    }

    for pid, bot in bots.items():
        bot.receive_cards([game.deck.draw_card() for _ in range(7)])
        game.players[pid] = bot

    game.turn_order = list(bots.keys())
    game.current_player = game.turn_order[0]
    # Draw initial top card (must not be a Wild, +4 or action card)
    while True:
        first_card = game.deck.draw_card()
        if first_card and (
                first_card[0] in ['R', 'G', 'B', 'Y'] and  # Valid color
                first_card[1:].isdigit()  # Must be a number (not action)
        ):
            game.played_cards.append(first_card)
            break
        else:
            # Put invalid card back and reshuffle
            game.deck.cards.insert(0, first_card)
            random.shuffle(game.deck.cards)

    print(f"Game Start — Top card: {game.played_cards[-1]}")

    round_counter = 0
    while True:
        current_player = game.current_player
        bot = game.players[current_player]
        top_card = game.played_cards[-1]

        print(f"\n🔁 Turn: Player {current_player} — Hand({len(bot.hand)}): {bot.hand}")
        print(f"Top Card: {top_card}")

        move = bot.choose_card(top_card)
        if move:
            print(f"Player {current_player} plays: {move}")
            winner = game.play_turn(current_player, move)
            if winner is not None:
                print(f"🏁 Game Over — Player {winner} wins!")
                break
        else:
            print(f"Player {current_player} has no move, drawing...")
            winner = game.play_turn(current_player, None)
            if winner is not None:
                print(f"🏁 Game Over — Player {winner} wins!")
                break

        round_counter += 1
        if round_counter > 200:
            print("❌ Game stopped after 1000 turns — possible bot deadlock.")
            break


if __name__ == "__main__":
    main()
