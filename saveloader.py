"""Modul för filhantering"""

import os

DIRECTORY = "saves"

def is_save() -> None:
    """Checks for saves"""

    if not os.path.exists(DIRECTORY):
        print("No saves folder found...\nCreating new saves folder...")
        os.makedirs(DIRECTORY)
        print(f"A new directory called {DIRECTORY} has been created.")

    for diff in ("e", "n", "h", "f"):
        file_path = os.path.join(DIRECTORY, f"save_{diff}.txt")
        if not os.path.exists(file_path):
            print(f"No save file found for difficulty [{diff}]\nCreating new save...")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("")
            print("Save created!")

def save_score(score: object) -> None:
    """Saves the score to respective save file"""
    file_path = os.path.join(DIRECTORY, f"save_{score.diff}.txt")
    try:
        with open(file_path, "a", encoding="utf-8") as save:
            save.write(f"{score.score}\n")
            save.write(f"{score.name}\n")
            print("Score has been saved.")
            print(f"Final score: {score.score}")
    except IOError as error:
        print(f"ERROR: {file_path} seems to be open in another program \
              please close the program.")
        print(f"{error}")