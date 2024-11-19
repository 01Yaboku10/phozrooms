import failsafe
import scoreboard
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class Movement():
    def __init__(self, game_map: list[list[str]], mapsize: int, diff: str, get_admin: object, game_map_inst: object, phoz: object) -> None:
        self.game_map = game_map
        self.game_map_inst = game_map_inst
        self.mapsize = mapsize
        self.diff = diff
        self.get_admin = get_admin
        self.current_room = 0
        self.start_pos = self.start_position()
        self.current_row, self.current_col = self.start_pos
        self.phoz = phoz

    def start_position(self) -> tuple[int, int]:
        for col_index, row in enumerate(self.game_map):
            if "S" in row:
                row_index = row.index("S")
                self.overwrite(col_index, row_index) # Remove start pos from map
                self.current_room = self.get_room(col_index, row_index)
                if self.get_admin.is_admin:
                    print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Spawn Y: {col_index}. Spawn X: {row_index}")
                return (col_index, row_index)
        return None
    
    def overwrite(self, row: int, col: int) -> None:
        self.game_map[row][col] = 0

    def get_room(self, row: int, col: int):
        current_room = (row + 1) * self.mapsize + (col + 1 - self.mapsize)
        if self.get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Current room: {current_room}")
        return current_room
    
    def set_cords(self, row: int, col: int, mode: str = "Default") -> None:
        if mode == "Default":
            self.current_row = self.current_row + row
            self.current_col = self.current_col + col
        elif mode == "Update":
            self.current_row = row
            self.current_col = col
        if self.get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Cordinates updated to ({self.current_row}, {self.current_col})")
        self.current_room = self.get_room(self.current_row, self.current_col)
    
    def ask_direction(self) -> tuple[bool, bool, bool, bool]:
        west, east, north, south = failsafe.is_inbounce(self.current_row, self.current_col, self.mapsize)
        return west, east, north, south
    
    def move(self, goto: str, gui: object) -> None:
        scoreboard.counter()
        directions = {
            "W": (0, -1),
            "E": (0, 1),
            "S": (1, 0),
            "N": (-1, 0)
        }
        row_value, col_value = directions[goto]
        new_row = self.current_row + row_value
        new_col = self.current_col + col_value
        self.set_cords(row_value, col_value)
        failsafe.is_item(self.get_admin, self.game_map, new_row, new_col, self.mapsize, gui, self, self.game_map_inst, self.phoz)