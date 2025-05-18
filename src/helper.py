import json
import os
from typing import MutableMapping
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

    if round.round_score == 0:
        _lost = True
    else:
        _lost = False

    turn_count = 0
    if hasattr(round, "turn"):
        if isinstance(round.turn, list):
            turn_count = len(round.turn)
        else:
            print(f"Warning: round.turn is not a list, it's a {type(round.turn)}")

    round_json = {
        "round_id": round_id,
        "round_player": round.player,
        "round_rolls": len(round.rolls),
        "round_lost": _lost,
        "round_score": round.round_score,
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
            player="none",
            round_score=0,
            turn=[],
            rolls=[],
            dice_left=0,
        )

    # Load the JSON data
    with open(json_file_path, "r") as file:
        loaded_data = json.load(file)

    round = round_data(
        player=loaded_data[""],
        round_score=loaded_data[""],
        turn=loaded_data[""],
        rolls=loaded_data[""],
        dice_left=loaded_data[""],
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
            next_roll_dice=0,
            score=0,
            used_dice=0,
        )

    # Load the JSON data
    with open(json_file_path, "r") as file:
        loaded_data = json.load(file)

    turn = turn_data(
        avalible_dice=loaded_data["avalible_dice"],
        next_roll_dice=loaded_data["next_roll_dice"],
        score=loaded_data["score"],
        used_dice=loaded_data["used_dice"],
    )

    return turn
