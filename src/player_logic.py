from models import meta_data, round_data, turn_data
from typing import Optional
from game_logic import roll_dice
from helper import load_round_data
from game_logic import calculate_score_roll, find_dice_to_keep


def player_play_round(
    num_dice_input: int,
    current_round: round_data,
    dice_to_keep: Optional[int] = None,
) -> round_data:
    turn = turn_data(
        avalible_dice=roll_dice(num_dice_input),
        score=0,
        dice_left=0,
    )

    turn = calculate_score_roll(
        turn.avalible_dice, turn, find_dice_to_keep(dice_to_keep)
    )

    if turn.score == 0:
        current_round.round_score = 0
        current_round.rolls += [turn]
        current_round.end = True

        return current_round

        # Add the turn to the round rolls, and add the score to the round score
    current_round.rolls += [turn]
    current_round.round_score += turn.score

    return current_round
