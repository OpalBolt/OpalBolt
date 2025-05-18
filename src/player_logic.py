from models import meta_data, turn_data
from game_logic import roll_dice
from helper import load_round_data
from game_logic import calculate_score_roll


def player_play_round(
    num_dice_input: int, game_meta: meta_data, player: str
) -> turn_data:
    turn = turn_data(
        next_roll_dice=num_dice_input,
        avalible_dice=roll_dice(num_dice_input),
        score=0,
        used_dice=0,
    )

    current_round = load_round_data(game_meta.game_id, game_meta.round_id)

    turn = calculate_score_roll(turn.avalible_dice, turn)

    if turn.score == 0:
        current_round.round_score = 0
        current_round.rolls += [turn]

        return turn

        # Add the turn to the round rolls, and add the score to the round score
    current_round.rolls += [turn]
    current_round.round_score += turn.score

    # Check if the oponent has scored more than 300
    # and if the next roll is less than 3 dice
    if turn.next_roll_dice <= 3 and current_round.round_score >= 300:
        return turn

    return turn
