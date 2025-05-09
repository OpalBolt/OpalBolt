from dataclasses import dataclass

@dataclass
class game_data:
    game_score_player: int
    game_score_opponent: int
    game_ended: bool = False

@dataclass
class turn_data:
    """
    Represents a player's turn in the game.
    """
    avalible_dice: int
    next_roll_dice: int
    score: int
    used_dice: int

@dataclass
class round_data:
    player: str
    round_score: int
    turn: list
    rolls: list