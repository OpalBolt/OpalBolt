import random
from collections import Counter
from typing import Optional
from models import round_data, turn_data, game_data


def calculate_score_roll(
    dice_to_calc_from: list, turn: turn_data, dice_to_keep: Optional[list] = []
) -> turn_data:
    print(f"Dice used to do calculations: {dice_to_calc_from}")
    _keep = False

    if dice_to_keep:
        for die in dice_to_keep:
            if die not in dice_to_calc_from:
                _keep = True

    if _keep:
        print("Invalid keep dice. Keeping all dice.")
        counts = Counter(dice_to_keep)
    else:
        counts = Counter(dice_to_calc_from)

    values = list(counts.values())
    unique_numbers = set(dice_to_calc_from)
    turn.score = 0

    if len(unique_numbers) == 6:
        turn.dice_left = 6
        turn.score = 1500
        return turn

    if len(dice_to_calc_from) == 6 and values.count(2) == 3:
        turn.dice_left = 6
        turn.score = 1000
        return turn

    # Count each number
    for num in counts:
        count = counts[num]
        turn.dice_left -= count

        if count >= 3:
            print("3 pairs")
            base_score = 1000 if num == 1 else num * 100
            multiplier = 2 ** (count - 3)  # 3 of a kind = x1, 4 = x2, 5 = x4, 6 = x8
            turn.score += base_score * multiplier
            count -= 3  # Remove the three used for the set

        # Singles of 1s or 5s after sets
        if num == 1:
            print("1")
            turn.score += count * 100

        elif num == 5:
            print("5")
            turn.score += count * 50

    if turn.dice_left == 0:
        turn.dice_left = 6

    return turn


def roll_dice(num_dice: int) -> list:
    return [random.randint(1, 6) for _ in range(num_dice)]


def check_game_end(current_game: game_data) -> game_data:
    if (
        current_game.game_score_player >= 10000
        or current_game.game_score_opponent >= 10000
    ):
        current_game.game_ended = True

    return current_game


# converts the dice int to a string
# Iritiate over the string, and then puts this into
# the list as a int.
def find_dice_to_keep(dice: Optional[int]) -> Optional[list[int]]:
    if dice:
        return [int(d) for d in str(dice)]
    return None
