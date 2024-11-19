import saveloader
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)
count = 0

class Scoreboards():
    def __init__(self, diff: str, score: int, name: str) -> None:
        self.diff = diff.lower()
        self.score = score
        self.name = name

def set_score(diff: str, score: int, name: str) -> None:
    scoreboard = Scoreboards(diff, score, name)
    saveloader.is_save() # Check för sparfiler
    saveloader.save_score(scoreboard)

def counter():
    global count
    count +=1
    print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Current score: {count}")
    return count

def final_score():
    return count-1

def get_score(diff: str, get_admin: object):
    global is_admin
    is_admin = get_admin.is_admin
    score = saveloader.load_score(diff)
    return score