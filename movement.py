"""Modul för spelarrörelse till Phöz Rooms."""

import failsafe
import generation
import scoreboard

class Start():
    """Klass för spelarens start position"""
    def __init__(self, game_map) -> None:
        """Initialiserande metod för att hämta
        spelarens start position.
            Argument:
                game_map(list): spelkartan
            Retunerar:
                None"""
        self.game_map = game_map
        self.start_position = self.start()

    def start(self) -> tuple[int, int]:
        """Hämtar rummet där spelaren börjar.
            
            Retunerar:
                row_index(int): Rad positionen
                col_index(int): Kolumn positionen"""
        for row_index, col in enumerate(self.game_map):  #  går igenom varje item sant index
            if "S" in col:
                col_index = col.index("S")
                return (row_index, col_index)
        return None

class Movement():
    """Huvudklass som sköter alla spelarrörelser och lite annat."""
    def __init__(self, game_map: list, mapsize: int, admin: bool, diff: str) -> None:
        """Initialiserande metod som hämtar variabler för att
        kunna användas i andra metoder i klassen.
            Argument:
                game_map(list): spelkartan
                mapsize(int): spelkartans storlek
                admin(bool): spelarens admin status
            Retunerar:
                None"""
        self.start = Start(game_map)
        self.mapsize = mapsize
        self.game_map = game_map
        self.current_row, self.current_col = \
        self.start.start_position if self.start.start_position else (None, None)
        self.admin = admin
        self.diff = diff

    def start_move(self, admin: bool) -> tuple[int, int]:
        """Hämtar startpositionen för spelaren.
            Argument:
                admin(bool): spelarens admin status
            Retunerar:
                self.current_col(int): spelarens rad position
                self.current_row(int): spelarens kolumn position"""
        if self.current_row is not None and self.current_col is not None:
            self.overwrite(self.current_row, self.current_col)
            room(self.current_row, self.current_col, self.mapsize)
            if admin:
                print(f"DEBUGG: Current position: Row {self.current_row + 1}, Comlumn {self.current_col + 1}")
            self.ask_direction()
            return self.current_col, self.current_row
        else:
            print("Start position not found")
    
    def overwrite(self, row: int, col: int) -> None:
        """Skriver över ett rum med en nolla för att
        markera att rummet är nu tomt.
            Argument:
                row(int): rummets rad värde
                col(int): rummets kolumn värde
            Retunerar:
                None"""
        self.game_map[row][col] = 0
    
    def ask_direction(self) -> None:
        """Frågar användaren om vilket håll de vill gå.
            Retunerar:
                None"""
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
        
    def set_cords(self, new_row: int, new_col: int) -> None:
        """Uppdaterar spelarens nuvarande position och
        adderar +1 till spelarens poäng.
            Argument:
                new_row(int): den nya rad positionen
                new_col(int): den nya kolumn positionen
            Retunerar:
                None"""
        self.current_col = new_col
        self.current_row = new_row
        if self.admin:
            print("DEBUGG: Setting new cordinates!")
            print(f"DEBUGG: New cordinates: Y: {new_row}, X: {new_col}")
        room(new_row, new_col, self.mapsize)  #  Meddelar om det nya rummet
        scoreboard.counter(self.admin)

    def move(self, goto: str) -> None:
        """Flyttar spelaren till det nya rummet.

            Argument:
                goto(str): Riktningen som spelaren vill flytta sig till
                
            Retunernar:
                None"""
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
            failsafe.is_item(self, self.game_map, new_row, new_col, self.mapsize, self.admin, self.diff)
        
        elif goto == "M":
            self.ask_direction()
        else:
            print("Something went wrong...")
            return

#(3,1) = rum 17
def room(row_index: int, col_index: int, mapsize: int) -> int:
    """Informerar spelaren om vilket rum de befinner sig i.
        Argument:
            row_index(int): rad värde
            col_index(int): kolumn värde
            mapsize(int): spelkarts storleken
        Retunerar:
            current_room(int): Det nuvarande rummet"""
    current_room = (row_index + 1)*mapsize + (col_index + 1 - mapsize)
    print("-----------------------------")
    print(f"Currently in room: {current_room}")
    return current_room

def item_init(new_row: int, new_col: int, game_map: list[list[str]], mapsize: int, \
              item: str, admin: bool, diff: str, old_row=None, old_col=None) -> None:
    """initialiserare för kartobjekten. Överskrider vissa kordinater
    och uppdaterar spelarens position. Kan också skapa en till Phöz.
    Efter detta så frågas spelaren igen vart de vill gå.
        Argument:
            new_row(int): Det nya rad värdet
            new_col(int): Det nya kolumn värdet
            gane_map(list): Spelkartan
            mapsize(int): Spelkarts storleken
            item(str): kartobjektet
            admin(bool): Spelarens admin status
            diff(str): svårighetsgraden
            old_row(int): Det gamla rad värdet
            old_col(int): Det gamla kolumn värdet
        Retunrerar:
            None"""
    if admin:
        print("DEBUGG: Running item_init")
    movement_instance = Movement(game_map, mapsize, admin, diff)
    if item == "B":
        movement_instance.overwrite(old_row, old_col)
        movement_instance.set_cords(new_row, new_col)
    if item == "P":
        movement_instance.overwrite(old_row, old_col)
        movement_instance.set_cords(new_row, new_col)
        generation.spawn_phoz(game_map, mapsize, 1)
    if item == "T":
        movement_instance.overwrite(old_row, old_col)
    movement_instance.ask_direction()
