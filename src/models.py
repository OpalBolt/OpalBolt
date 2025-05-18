from dataclasses import dataclass


@dataclass
class game_data:
    game_score_player: int
    game_score_opponent: int
    game_ended: bool = False


@dataclass
class turn_data:
    avalible_dice: list
    next_roll_dice: int
    score: int
    used_dice: int


@dataclass
class round_data:
    player: str
    round_score: int
    turn: list
    rolls: list
    dice_left: int


@dataclass
class meta_data:
    game_id: int
    round_id: int
    turn_id: int
