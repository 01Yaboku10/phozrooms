import failsafe
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class Heineken():
    def __init__(self, player_x: int, player_y: int, gui: object, mapsize: int, phoz: object):
        self.player_row = player_x
        self.player_col = player_y
        self.mapsize = mapsize
        self.gui = gui
        self.current_shot_x = player_x
        self.current_shot_y = player_y
        self.shot_directions = []
        self.shots = 1
        self.phoz = phoz

    def ask_direction(self):
        west, east, north, south = failsafe.is_inbounce(self.current_shot_x, self.current_shot_y, self.mapsize)
        return west, east, north, south
    
    def shoot(self, direction: str):
        directions = {
            "W": (0, -1),
            "E": (0, 1),
            "S": (1, 0),
            "N": (-1, 0)
        }
        row, col = directions[direction]
        self.current_shot_x += row
        self.current_shot_y += col
        self.shot_directions.append((self.current_shot_x, self.current_shot_y))
        self.shots += 1
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Registered Shot [{self.current_shot_y, self.current_shot_x}]")
        if self.shots <= 3:
            self.gui.shoot_directions(self, self.shots)
        else:
            self.bukkake()

    def bukkake(self):
        for i in self.phoz.location():
            phoz_row, phoz_col = i
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Phöz in {phoz_row, phoz_col}.")
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Player in {self.player_row, self.player_col}.")
            for i in self.shot_directions:
                col, row = i
                print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Shot: {row, col}.")
                if row == self.player_col and col == self.player_row:
                    print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} You killed yourself.")
                    return
                if row == phoz_row and col == phoz_col:
                    print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Phöz Killed.")
                    self.gui.phoz_hit(True, self.phoz, phoz_col, phoz_row)
                    return
        self.gui.phoz_hit(False, self.phoz)
