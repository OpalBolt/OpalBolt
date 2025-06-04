import random
import structlog
from game_logic import calculate_score_roll, roll_dice
from models import turn_data, round_data


log = structlog.get_logger(__name__)


def oponent_rolls():
    _strat_rolls = random.randint(2, 5)

    return _strat_rolls


def oponent_play_round(num_dice_input: int) -> round_data:
    rolls = oponent_rolls()
    log.debug(f"Oponent is detirmened to roll {rolls} times")

    turn = turn_data(
        next_roll_dice=num_dice_input,
        avalible_dice=roll_dice(num_dice_input),
        score=0,
        used_dice=0,
    )

    current_round = round_data(
        player="oponent", round_score=0, turn=[], rolls=[], dice_left=0
    )
    log.debug(turn)

    for _ in range(rolls):
        turn = calculate_score_roll(turn.avalible_dice, turn)

        # Check if the turn score is 0
        # If the turn score is 0, the round ends and the round score is set to 0
        if turn.score == 0:
            log.debug("oponent roll came up with a score of 0, ending round")
            current_round.round_score = 0
            current_round.rolls += [turn]

            break

        # Add the turn to the round rolls, and add the score to the round score
        current_round.rolls += [turn]
        current_round.round_score += turn.score

        # Check if the oponent has scored more than 300
        # and if the next roll is less than 3 dice
        if turn.next_roll_dice <= 3 and current_round.round_score >= 300:
            log.debug("round ended, high score or few dice left")
            break

        turn.avalible_dice = roll_dice(turn.next_roll_dice)

    return current_round
    log.debug(f"oponent scored: {current_round.round_score} points this round")

