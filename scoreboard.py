"""Modul för poängtavlan till Phöz Rooms"""
import saveloader

count = 0

class Scoreboards():
    def __init__(self, diff: str, score: int, name: str) -> None:
        self.diff = diff
        self.score = score
        self.name = name

def set_score(diff: str, score: int, name: str) -> None:
    """Set the score"""
    scoreboard = Scoreboards(diff, score, name)
    saveloader.is_save() # Check för sparfiler
    saveloader.save_score(scoreboard)

def counter(admin):
    """Räknar poäng"""
    global count
    count +=1
    if admin:
        print(f"DEBUGG: Current score: {count}")
    return count

def final_score():
    """Hämtar slutpoäng"""
    return count-1