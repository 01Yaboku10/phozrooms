import failsafe
import generation

class Start():
    def __init__(self, game_map):
        self.game_map = game_map
        self.start_position = self.start()

    def start(self):
        for row_index, row in enumerate(self.game_map):  #  går igenom varje item sant index
            if "S" in row:
                col_index = row.index("S")
                return (row_index, col_index)  
        return None

class Movement():
    def __init__(self, game_map, mapsize, admin):
        self.start = Start(game_map)
        self.mapsize = mapsize
        self.game_map = game_map
        self.current_row, self.current_col = \
        self.start.start_position if self.start.start_position else (None, None)
        self.admin = admin

    def start_move(self):
        if self.current_row is not None and self.current_col is not None:
            self.overwrite(self.current_row, self.current_col)
            room(self.current_row, self.current_col, self.mapsize)
            print(f"Current position: Row {self.current_row + 1}, Comlumn {self.current_col + 1}")
            self.ask_direction()
            return self.current_col, self.current_row
        else:
            print("Start pos not found")
    
    def overwrite(self, row, col):
        self.game_map[row][col] = 0
    
    def ask_direction(self):
        west, east, north, south = failsafe.is_inbounce(self.current_col, self.current_row, self.mapsize)
        print("You can go:")
        if west:
            print("[W]est")
        if east:
            print("[E]ast")
        if south:
            print("[S]outh")
        if north:
            print("[N]orth")
        goto = failsafe.is_valid_direction(west, east, north, south, self.admin)
        self.move(goto)
        
    def set_cords(self, new_row, new_col):
        self.current_col = new_col
        self.current_row = new_row
        if self.admin:
            print("DEBUGG: Setting new cordinates!")
            print(f"DEBUGG: New cordinates: Y: {new_row}, X: {new_col}")
        room(new_row, new_col, self.mapsize)  #  Meddelar om det nya rummet
        failsafe.is_phoz(new_row, new_col, self.game_map, self.admin)

    def move(self, goto):
        """Flyttar spelaren till det nya rummet.

            Argument:
                goto(str): Riktningen som spelaren vill flytta sig till
                
            Retunernar:
            current_col(int): Uppdaterar värdet
            current_row(int): Uppdaterar värdet"""
        directions = {  #  Innehåller riktningarna med dess värden
           "W": (0, -1),
           "E": (0, 1),
           "S": (1, 0),
           "N": (-1, 0)
       }
        if goto in directions:
            row_value, col_value = directions[goto]
            new_row = self.current_row + row_value
            new_col = self.current_col + col_value
            self.set_cords(new_row, new_col)
            failsafe.is_item(self, self.game_map, new_row, new_col, self.mapsize)
        
        elif goto == "M":
            self.ask_direction()
        else:
            print("Something went wrong...")
            return

#(3,1) = rum 17
def room(row_index, col_index, mapsize):
    current_room = (row_index + 1)*mapsize + (col_index + 1 - mapsize)
    print("-----------------------------")
    print(f"Currently in room: {current_room}")
    return current_room

def item_init(new_row, new_col, game_map, mapsize, item, admin, old_row=None, old_col=None):
    if admin:
        print("DEBUGG: Running item_init")
    movement_instance = Movement(game_map, mapsize, admin)
    if item == "B":
        movement_instance.overwrite(old_row, old_col)
        movement_instance.set_cords(new_row, new_col)
    if item == "P":
        movement_instance.overwrite(old_row, old_col)
        movement_instance.set_cords(new_row, new_col)
        generation.spawn_phoz(game_map, mapsize, 1)
    if item == "T":
        movement_instance.overwrite(old_row, old_col)
        movement_instance.set_cords(old_row, old_col)
    movement_instance.ask_direction()