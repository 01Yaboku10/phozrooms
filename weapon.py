import failsafe
import movement

class Weapon():
    def __init__(self, current_row: int, current_col: int, mapsize: int, phoz_row: int, phoz_col: int, admin: bool, movement, game_map: list[list[str]]) -> None:
        self.current_row = current_row
        self.current_col = current_col
        self.mapsize = mapsize
        self.phoz_row = phoz_row
        self.phoz_col = phoz_col
        self.admin = admin
        self.movement = movement
        self.map = game_map

    def aim(self) -> None:
        directions = {  #  Innehåller riktningarna med dess värden
            "W": (0, -1),
            "E": (0, 1),
            "S": (1, 0),
            "N": (-1, 0)
        }
        direction = []
        aimed_row = self.current_row
        aimed_col = self.current_col

        print("Vart vill du skjuta?")

        for i in range(3):
            west, east, north, south = failsafe.is_inbounce(aimed_col, aimed_row, self.mapsize)
            print("-----------------------------")
            print(f"Tile {i+1} / 3")
            if west:
                print("[W]est")
            if east:
                print("[E]ast")
            if south:
                print("[S]outh")
            if north:
                print("[N]orth")
            aimed = input("Skjut: ").upper().strip()
            while True:
                if aimed == "W" and west \
                    or aimed == "E" and east \
                    or aimed == "S" and south \
                    or aimed == "N" and north:
                    row, col = directions[aimed]
                    aimed_row += row
                    aimed_col += col
                    direction.append([aimed_row, aimed_col])
                    break
                else:
                    aimed = input("Invalid Direction\nSkjut: ").upper().strip()
        self.shoot(direction)

    # direction = [["row1", "col1"], ["row2", "col2"], ["row3", "col3"]]
    def shoot(self, direction: list[list[int]]) -> None:
        for i in direction:
            row = i[0]
            col = i[1]
            if self.is_phoz_shot(row, col):
                self.killed()
                return
        print("-----------------------------")
        print("Phoz was not hit by your attack!")
        # Check the three cells for phoz, if phoz call killed

    def killed(self) -> None:
        print("-----------------------------")
        print("Phoz killed!")
        self.movement.overwrite(self.phoz_row, self.phoz_col)

    def is_phoz_shot(self, row: int, col: int) -> bool:
        if row == self.phoz_row and col == self.phoz_col:
            return True
        else:
            return False