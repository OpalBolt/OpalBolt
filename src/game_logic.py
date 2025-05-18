import random
from collections import Counter
from models import turn_data, game_data


def calculate_score_roll(
    dice: list, turn: turn_data, dice_to_keep: list = []
) -> turn_data:
    print(f"Dice rolled: {dice}")
    _keep = False

    if dice_to_keep:
        for die in dice_to_keep:
            if die not in dice:
                _keep = True

    if _keep:
        print("Invalid keep dice. Keeping all dice.")
        counts = Counter(dice_to_keep)
    else:
        counts = Counter(dice)

    values = list(counts.values())
    unique_numbers = set(dice)
    turn.score = 0

    if len(unique_numbers) == 6:
        turn.next_roll_dice = 6
        turn.score = 1500
        return turn

    if len(dice) == 6 and values.count(2) == 3:
        turn.next_roll_dice = 6
        turn.score = 1000
        return turn

    # Count each number
    for num in counts:
        count = counts[num]

        if count >= 3:
            base_score = 1000 if num == 1 else num * 100
            multiplier = 2 ** (count - 3)  # 3 of a kind = x1, 4 = x2, 5 = x4, 6 = x8
            turn.score += base_score * multiplier
            turn.next_roll_dice -= count
            count -= 3  # Remove the three used for the set

        # Singles of 1s or 5s after sets
        if num == 1:
            print("1")
            turn.score += count * 100
            turn.next_roll_dice -= count

        elif num == 5:
            print("5")
            turn.score += count * 50
            turn.next_roll_dice -= count

    return turn


def roll_dice(num_dice: int) -> list:
    return [random.randint(1, 6) for _ in range(num_dice)]


def check_game_end(game: game_data) -> game_data:
    if game.game_score_player >= 10000 or game.game_score_opponent >= 10000:
        game.game_ended = True

    return game
