import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class Phoz():
    def __init__(self, game_map: list[list[str]], get_admim: object, mapsize, gui):
        self.life_status = True
        self.game_map = game_map
        self.get_admin = get_admim
        self.mapsize = mapsize
        self.gui = gui
        self.shots_taken = 0

    def is_alive(self) -> bool:
        for i in self.location():
            phoz_col, phoz_row = i
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Checked [{phoz_row, phoz_col}].")
            if phoz_col == 44 and phoz_row == 44:
                self.life_status = False
                if self.get_admin.is_admin:
                    print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Phöz's life status: {self.life_status}")
                return self.life_status
        self.life_status = True
        if self.get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Phöz's life status: {self.life_status}")
        return self.life_status
    
    def is_near(self, player_x: int, player_y: int) -> bool:
        for i in self.location():
            phoz_col, phoz_row = i
            if 0 <= abs(player_x - phoz_row) < 2 and 0 <= abs(player_y - phoz_col) < 2:
                return True
        return False
    
    def location(self) -> list[tuple[int, int]]:
        locations = []
        for row_i, col in enumerate(self.game_map):
            if "P" in col:
                col_i = col.index("P")
                locations.append((col_i, row_i))
        if locations:
            return locations # Life value
        else:
            return [(44, 44)] # Death value
