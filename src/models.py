from pydantic import BaseModel, Field







class game_data(persistableJson):
    save_path: str = Field(default="game", repr=False)
    game_score_player: int = Field(default=0)
    game_score_opponent: int = Field(default=0)
    game_ended: bool = Field(default=False)


class turn_data(persistableJson):
    save_path: str = Field(default="turn", repr=False)
    avalible_dice: list = Field(default=[])
    score: int = Field(default=0)
    dice_left: int = Field(default=0)


class round_data(persistableJson):
    save_path: str = Field(default="round", repr=False)
    next_roll_dice: int = Field(default=6)
    player: str = Field(default="")
    round_score: int = Field(default=0)
    rolls: list = Field(default=[])
    dice_left: int = Field(default=0)
    end: bool = Field(default=False)


class meta_data(persistableJson):
    save_path: str = Field(default="meta", repr=False)
    game_id: int = Field(default=0)
    round_id: int = Field(default=0)
    turn_id: int = Field(default=0)
    avalible_dice: list = Field(default=[])
