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

import structlog
from game_logic import calculate_score_roll, check_game_end, roll_dice
import typer
import logging

from models import game_data, meta_data, round_data, turn_data
from oponent_logic import oponent_play_round
from player_logic import player_play_round

app = typer.Typer()


structlog.stdlib.recreate_defaults()
log = structlog.get_logger(__name__)

# structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(logging.DEBUG))
logging.basicConfig(
    level=logging.DEBUG,
)


@app.command()
def roll_player(game_id: int, player: str, choice: str, dice_to_keep: list):
    game_meta = meta_data.load()

    if game_id:
        current_game = game_data.load(f"_{str(game_id)}")
    else:
        current_game = game_data.load(f"_{game_meta.game_id}")

    current_round = round_data.load(f"_{game_meta.game_id}_{game_meta.round_id}")
    current_round.player = player

    turn = calculate_score_roll(game_meta.avalible_dice, turn_data(), dice_to_keep)

    if turn.score == 0:
        current_round.round_score = 0
        turn.save(f"_{game_meta.game_id}_{game_meta.round_id}_{game_meta.turn_id}")
        return None

    current_round.round_score += turn.score
    turn.save(f"_{game_meta.game_id}_{game_meta.round_id}_{game_meta.turn_id}")

    if choice == "keep":
        current_round.end = True
    else:
        game_meta.avalible_dice = roll_dice(turn.dice_left)

    make_checks(game_meta, current_game, current_round)

    return current_game


def make_checks(
    game_meta: meta_data, current_game: game_data, current_round: round_data
):
    check_game_end(current_game)
    current_game.save(f"_{game_meta.game_id}")
    current_round.save(f"_{game_meta.game_id}_{game_meta.round_id}")
    game_meta.turn_id += 1
    game_meta.save()

    if current_round.end:
        game_meta.round_id += 1
        game_meta.turn_id = 0
        game_meta.save()

    if current_game.game_ended:
        game_meta.game_id += 1
        game_meta.round_id = 0
        current_game.game_score_player = 0
        current_game.game_score_opponent = 0
        game_meta.save()
        current_game.save(f"_{game_meta.game_id}")


@app.command()
def test_save():
    # game_meta = meta_data(game_id=4, round_id=29)
    game_meta = meta_data.load()
    log.info(game_meta)
    current_round = round_data.load(f"_{game_meta.game_id}_{game_meta.round_id}")
    log.info(current_round)


@app.command()
def roll_game(game_id: Optional[int] = None, player: str = "oponent"):
    game_meta = meta_data.load()

    if game_id:
        current_game = game_data.load(f"_{str(game_id)}")
    else:
        current_game = game_data.load(f"_{game_meta.game_id}")

    current_round = round_data.load(f"_{game_meta.game_id}_{game_meta.round_id}")

    current_round = oponent_play_round(current_round.next_roll_dice, current_round)

    current_game.game_score_opponent += current_round.round_score

    game_meta.avalible_dice = roll_dice(6)

    make_checks(game_meta, current_game, current_round)

    return current_game


def main():
    app()


if __name__ == "__main__":
    main()
