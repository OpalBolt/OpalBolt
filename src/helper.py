import json
import os
from typing import MutableMapping, Optional, Any
from functools import singledispatch

from click.shell_completion import _resolve_incomplete
from models import game_data, round_data, meta_data, turn_data


def create_folder_structure(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def define_save_path(file_name: str, filename: str) -> str:
    return os.path.join(os.path.dirname(__file__), "..", file_name, f"{filename}.json")


def load_game_data(game_id: int) -> game_data:
    """
    Load game data from a JSON file.
    """

    # Define the path to the JSON file
    json_file_path = define_save_path("games", f"game_data_{game_id}")

    if not os.path.exists(json_file_path):
        return game_data(
            game_score_player=0,
            game_score_opponent=0,
        )

    # Load the JSON data
    with open(json_file_path, "r") as file:
        loaded_data = json.load(file)

    game = game_data(
        game_score_player=loaded_data["game_score_player"],
        game_score_opponent=loaded_data["game_score_opponent"],
    )

    return game


def save_game_data(game: game_data, game_id: int) -> None:
    """
    Save game data to a JSON file.
    """

    # Convert the game data to a dictionary
    game_json = {
        "game_score_player": game.game_score_player,
        "game_score_opponent": game.game_score_opponent,
    }

    # Define the path to the JSON file
    json_file_path = define_save_path("games", f"game_data_{game_id}")
    create_folder_structure(json_file_path)

    # Save the JSON data
    with open(json_file_path, "w") as file:
        json.dump(game_json, file, indent=4)


def save_round_data(round: round_data, game_id: int, round_id: int) -> None:
    """
    Save round data to a JSON file.
    """

    turns = []
    for turn in round.rolls:
        turns.append(
            {
                "avalible_dice": turn.avalible_dice,
                "score": turn.score,
                "dice_left": turn.dice_left,
            }
        )

    round_json = {
        "next_roll_dice": round.next_roll_dice,
        "player": round.player,
        "rolls": turns,
        "round_score": round.round_score,
        "dice_left": round.dice_left,
        "end": round.end,
    }

    # Define the path to the JSON file
    json_file_path = define_save_path("rounds", f"round_data_{game_id}_{round_id}")
    create_folder_structure(json_file_path)

    # Save the JSON data
    with open(json_file_path, "w") as file:
        json.dump(round_json, file, indent=4)


def load_round_data(game_id, round_id) -> round_data:
    # Define the path to the JSON file
    json_file_path = define_save_path("round", f"round_data_{game_id}_{round_id}")

    if not os.path.exists(json_file_path):
        return round_data(
            next_roll_dice=6,
            player="none",
            round_score=0,
            rolls=[],
            dice_left=0,
            end=False,
        )

    # Load the JSON data
    with open(json_file_path, "r") as file:
        loaded_data = json.load(file)

    rolls = []
    for turn in loaded_data.rounds:
        rolls.append(
            turn_data(
                avalible_dice=turn["avalible_dice"],
                score=turn["score"],
                dice_left=turn["dice_left"],
            )
        )

    round = round_data(
        next_roll_dice=loaded_data["next_roll_dice"],
        player=loaded_data["player"],
        round_score=loaded_data["round_score"],
        rolls=loaded_data["rolls"],
        dice_left=loaded_data["round_dice_left"],
        end=loaded_data["end"],
    )

    return round


def load_meta() -> meta_data:
    """
    Load meta data from a JSON file.
    """

    # Define the path to the JSON file
    json_file_path = define_save_path("meta", "meta_data")

    if not os.path.exists(json_file_path):
        return meta_data(
            game_id=0,
            round_id=0,
            turn_id=0,
        )

    # Load the JSON data
    with open(json_file_path, "r") as file:
        loaded_data = json.load(file)

    meta = meta_data(
        game_id=loaded_data["game_id"],
        round_id=loaded_data["round_id"],
        turn_id=loaded_data["turn_id"],
    )

    return meta


def save_meta(meta: meta_data) -> None:
    """
    Save meta data to a JSON file.
    """

    # Convert the meta data to a dictionary
    meta_json = {
        "game_id": meta.game_id,
        "round_id": meta.round_id,
        "turn_id": meta.turn_id,
    }

    # Define the path to the JSON file
    json_file_path = define_save_path("meta", "meta_data")
    create_folder_structure(json_file_path)

    # Save the JSON data
    with open(json_file_path, "w") as file:
        json.dump(meta_json, file, indent=4)


def load_turn_data(meta: meta_data) -> turn_data:
    """
    Load turn data to a dataclass
    """

    # Define the path to the JSON file
    json_file_path = define_save_path(
        "turn", f"turn_data_{meta.game_id}_{meta.round_id}_{meta.turn_id}"
    )

    if not os.path.exists(json_file_path):
        return turn_data(
            avalible_dice=[],
            score=0,
            dice_left=6,
        )

    # Load the JSON data
    with open(json_file_path, "r") as file:
        loaded_data = json.load(file)

    turn = turn_data(
        avalible_dice=loaded_data["avalible_dice"],
        score=loaded_data["score"],
        dice_left=loaded_data["used_dice"],
    )

    return turn


@singledispatch
def pydantic_saver(thing):
    pass


@pydantic_saver.register(meta_data, None)
def _(metadata: meta_data) -> None:
    json_file_path = define_save_path("meta_test", "meta_data")
    save_data(metadata, json_file_path)


@pydantic_saver.register(round_data)
def _(rounddata: round_data, metadata: meta_data) -> None:
    json_file_path = define_save_path(
        "rounds", f"round_data_{metadata.game_id}_{metadata.round_id}"
    )
    save_data(rounddata, json_file_path)


@pydantic_saver.register(turn_data)
def _(turndata: turn_data, metadata: meta_data) -> None:
    json_file_path = define_save_path(
        "turn", f"turn_data_{metadata.game_id}_{metadata.round_id}_{metadata.turn_id}"
    )
    save_data(turndata, json_file_path)


def save_data(data, json_file_path) -> None:
    create_folder_structure(json_file_path)
    with open(json_file_path, "w") as file:
        file.write(data.model_dump_json())


@singledispatch
def pydantic_loader(thing) -> Any:
    pass


@pydantic_loader.register(meta_data)
def _(metadata: meta_data) -> meta_data:
    json_file_path = define_save_path("meta", "meta_data")

    if not os.path.exists(json_file_path):
        return metadata

    # Load the JSON data
    with open(json_file_path, "r") as file:
        dict_data = json.load(file)

    loaded_data = meta_data.model_validate(dict_data)

    return loaded_data


@pydantic_loader.register(game_data)
def _(gamedata: game_data, metadata: meta_data) -> game_data:
    json_file_path = define_save_path("games", f"game_data_{metadata.game_id}")
    json_data = check_and_load_data(json_file_path)
    if json_data:
        return gamedata

    loaded_data = game_data.model_validate(json_data)

    return loaded_data


def check_and_load_data(filepath: str) -> bool | dict:
    if not os.path.exists(filepath):
        return False

    with open(filepath, "r") as file:
        dict_data = json.load(file)
    return dict_data


def p_load_meta() -> meta_data:
    json_file_path = define_save_path("meta", "meta_data")

    if not os.path.exists(json_file_path):
        return meta_data()

    # Load the JSON data
    with open(json_file_path, "r") as file:
        dict_data = json.load(file)

        loaded_data = meta_data.model_validate(dict_data)

    return loaded_data


def p_load_data(
    datatype: str, metadata: meta_data
) -> game_data | round_data | turn_data | None:
    if datatype == "game_data":
        return None
    if datatype == "round_data":
        return None
    if datatype == "turn_data":
        return None

    pass
