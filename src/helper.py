import json
import os
from typing import MutableMapping
from models import game_data, round_data, meta_data


def create_folder_structure(path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)


def define_save_path(file_name: str, filename) -> str:
    return os.path.join(
        os.path.dirname(__file__), "..", file_name, f"game_data_{filename}.json"
    )


def load_game_data(game_id: int) -> game_data:
    """
    Load game data from a JSON file.
    """

    # Define the path to the JSON file
    json_file_path = define_save_path("games", game_id)

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
    json_file_path = define_save_path("games", game_id)
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
    json_file_path = define_save_path("rounds", f"{game_id}_{round_id}")
    create_folder_structure(json_file_path)

    # Save the JSON data
    with open(json_file_path, "w") as file:
        json.dump(round_json, file, indent=4)


    """
    Load meta roll data from a JSON file.
    """

    # Define the path to the JSON file
    json_file_path = define_save_path('meta', 'rolls')
    create_folder_structure(json_file_path)

    # Load the JSON data
    with open(json_file_path, 'r') as file:
        loaded_data = json.load(file)

    return loaded_data

def save_meta_roll(roll: dict) -> None:
    """
    Save meta roll data to a JSON file.
    """

    # Define the path to the JSON file
    json_file_path = define_save_path('meta', 'rolls')
    create_folder_structure(json_file_path)

    # Save the JSON data
    with open(json_file_path, 'w') as file:
        json.dump(roll, file, indent=4)