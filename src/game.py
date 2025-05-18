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

from typing import Optional

import typer

from game_logic import check_game_end
from helper import (
    load_game_data,
    load_meta,
    load_round_data,
    load_turn_data,
    save_game_data,
    save_meta,
    save_round_data,
)
from models import game_data, meta_data, round_data
from oponent_logic import oponent_play_round
from player_logic import player_play_round

starting_dice = 6
app = typer.Typer()


@app.command()
def roll_player(game_id: int, player: str, dice: int):
    game_meta = load_meta()

    if game_id:
        game = load_game_data(game_id)
    else:
        game_id = game_meta.game_id
        game = load_game_data(game_meta.game_id)

    current_round = load_round_data(game_meta.game_id, game_meta.round_id)

    if game_meta.turn_id == 0:
        current_turn = player_play_round(starting_dice, game_meta, player)
    else:
        _tmp_meta = game_meta
        _tmp_meta.turn_id -= 1
        last_turn = load_turn_data(_tmp_meta)
        current_turn = player_play_round(
            last_turn.avalible_dice, game_meta=game_meta, player=player
        )


def make_checks(game_meta: meta_data, game: game_data, current_round: round_data):
    check_game_end(game)
    save_game_data(game, game_meta.game_id)
    save_round_data(current_round, game_meta.game_id, game_meta.round_id)
    game_meta.round_id += 1
    save_meta(game_meta)

    if game.game_ended:
        game_meta.game_id += 1
        game_meta.round_id = 0
        game.game_score_player = 0
        game.game_score_opponent = 0
        save_meta(game_meta)
        save_game_data(game, game_meta.game_id)


@app.command()
def roll_game(game_id: Optional[int] = None, player: str = "oponent"):
    game_meta = load_meta()

    if game_id:
        game = load_game_data(game_id)
    else:
        game = load_game_data(game_meta.game_id)

    if player != "oponent":
        player_play_round(
            num_dice_input=starting_dice, game_meta=game_meta, player=player
        )
    else:
        current_round = oponent_play_round(starting_dice)

    game.game_score_opponent += current_round.round_score

    make_checks(game_meta, game, current_round)

    return game


def main():
    app()


if __name__ == "__main__":
    main()
