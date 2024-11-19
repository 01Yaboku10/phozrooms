import os
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)
DIRECTORY = "saves"

class Score():
    def __init__(self, score: int, name: str):
        self.score = int(score)
        self.name = name

    def __repr__(self):
        return f"{self.score}, {self.name}"

    def __lt__(self, other):
        return self.score > other.score

def is_save(saves: list = ["e", "n", "h", "f"]) -> None:
    print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Looking for saves folder...")
    if not os.path.exists(DIRECTORY):
        print(f"{Fore.RED}[DEBUGG] No saves folder found...\nCreating new saves folder...")
        os.makedirs(DIRECTORY)
        print(f"A new directory called {DIRECTORY} has been created.")
    else:
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Save folder found!")

    for diff in saves:
        file_path = os.path.join(DIRECTORY, f"save_{diff}.txt")
        if not os.path.exists(file_path):
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} No save file found for difficulty [{diff}]\nCreating new save...")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("")
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Save created!")
        else:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Save save_{diff} found!")


def save_score(score: object) -> None:
    """Saves the score to respective save file"""
    file_path = os.path.join(DIRECTORY, f"save_{score.diff}.txt")
    try:
        with open(file_path, "a", encoding="utf-8") as save:
            save.write(f"{score.score}\n")
            save.write(f"{score.name}\n")
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Score has been saved.")
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Final score: {score.score}")
    except IOError as error:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {file_path} seems to be open in another program, please close the program.")
        print(f"{error}")

def load_score(diff: str) -> list[object]:
    is_save(diff)
    file_path = os.path.join(DIRECTORY, f"save_{diff}.txt")
    score_list = []
    try:
        with open(file_path, "r", encoding="utf-8") as save:
            score = save.readline().strip()
            while score != "":
                name = save.readline().strip()
                score_list.append(Score(score, name))
                score = save.readline().strip()
    except IOError as error:
        print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} {file_path} seems to be open in another program, please close the program.")
        print(f"{error}")
    return sorted(score_list, reverse=True)