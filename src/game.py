# 10,000 Dice Game - Definitions

# Game: A full play session where players take turns rolling dice to score points.
#       Ends when a player reaches 10,000 or more, triggering a final round for others.
#       Player with the highest score at the end wins.

# Round: One complete cycle where each player takes one turn.

# Turn: A player's sequence of rolls until they:
#       - Choose to stop and keep their score,
#       - Roll no scoring dice (bust), or
#       - Score with all six dice (must reroll all).
#       Must score 800+ in one turn to get "on the board."

# Incomming data: 
# choice: roll, bank, or end
# dice: list of the dice to keep
# player: the player making the choice

import typer
from oponent_logic import oponent_play_round
from models import game_data
from helper import save_game_data, save_round_data, load_game_data, save_meta_roll, load_meta_roll
from game_logic import check_game_end

starting_dice = 6
app = typer.Typer()

@app.command()
def roll_player(game_id: int, player: str, dice: int):
    pass

@app.command()
def roll_oponent(game_id: int = None):
    
    if game_id:
        game = load_game_data(game_id)
    else:
        game = game_data(
            game_score_player=0,
            game_score_opponent=0,
        )

    current_round = oponent_play_round(starting_dice)

    game.game_score_opponent += current_round.round_score
    print(game)
    
    check_game_end(game)


    save_game_data(game, 1)
    save_round_data(current_round, 1, 1)

    
    return game

def main():
    app()

if __name__ == "__main__":
    main()