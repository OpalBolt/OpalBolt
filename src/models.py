from pydantic import BaseModel, Field
from pathlib import Path
import json


class persistableJson(BaseModel):
    save_path: str = Field(default="", repr=False)

    def _file_path(self, additional_values: str = "") -> Path:
        return (
            Path(__file__).parent.parent
            / self.save_path
            / f"{self.save_path}_data{additional_values}.json"
        )

    def save(self, additional_values: str = ""):
        file = (
            self._file_path(additional_values)
            if additional_values
            else self._file_path()
        )
        file.parent.mkdir(parents=True, exist_ok=True)
        data = self.model_dump()
        data.pop("save_path", None)
        data.pop("save_file_name", None)
        file.write_text(json.dumps(data, ensure_ascii=False))

    @classmethod
    def load(cls, additional_values: str = ""):
        inst = cls()
        file = (
            inst._file_path(additional_values)
            if additional_values
            else inst._file_path()
        )
        # print(f"trying to load {file}")  # DEBUG
        # print(file.read_text())
        if file.exists():
            return cls.model_validate_json(file.read_text())
        return cls()


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
