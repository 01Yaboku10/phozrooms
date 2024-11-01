"""Modul för Phöz Rooms som genererar och placerar kartobjekt på spelbanan"""

import random
import failsafe
import movement

class Generation():
    
    def __init__(self, spawn: str, spawns: int) -> None:
        """Init funktion som hämtar variablar för att de sedan ska kunna
        användas runt om i klassen
            Argument:
                spawn(str): Typ av kartobjekt
                spawns(int): Antal kartobjekt av en typ"""
        self.spawn = spawn
        self.spawns = spawns

    def random_cord(self, map, mapsize: int) -> tuple[int, int]:
        """Genererar kordinater till ett slumpmässigt rum.
            Argument:
                map(list): spelkartan
                mapsize(int): spelkartans storlek
            Retunerar:
                rand_x(int): Slumpmässigt kolumn värde
                rand_y(int): Slumpmässigt rad värde"""
        i = 0
        while i < 1:
            rand_x = random.randint(0, mapsize - 1)
            rand_y = random.randint(0, mapsize - 1)
            if failsafe.map_is_empty(map, rand_x, rand_y):
                i += 1
        return rand_x, rand_y

    def generate(self, map, mapsize: int) -> None:
        """Lägger till alla kartobjekt till kartan i slumpmässiga rum.
            Argument:
                map(list): spelkartan
                mapsize(int): spelkartans storlek
            Retunerar:
                None"""
        i = 0
        while i < self.spawns:
            rand_x, rand_y = self.random_cord(map, mapsize)
            map[rand_x][rand_y] = self.spawn
            i += 1

class Hole(Generation):
    """Klass för hål kartobjektet"""
    def init_h(self) -> None:
        """initialiserande metod för hål"""
        print("-----------------------------")
        print("You fell into a hole -- falling to your demise!")

class Phoz(Generation):
    """Klass för phöz kartobjektet"""
    def init_p(self, map, mapsize: int, old_row: int, old_col: int, admin: bool, diff: str) -> bool:
        """initialiserande metod för phöz. Kastar spelaren iväg till ett slumpmässigt
        rum ifall spelaren har en skatt på sig och tar då bort skattan, om spelaren
        inte har en skatt så dör spelaren.
            Argument:
                map(list): spelkartan
                mapsize(int): spelkartans storlek
                old_row(int): phöz rad position
                old_col(int): phöz kolumn position
                admin(bool): användarens admin status
            Retunerar:
                found_treasure(bool): updaterar statusen av skatten"""
        global found_treasure
        print("-----------------------------")
        print("You enter a room and is quickly greeted by that which is holy...")
        print("NOOOOOOOOLLLLLLLAAAAAAAAAAAANN!")
        print("VAD GÖR NOLLAN HÄÄR NOLLAN?!")
        print("TRODDE NOLLAN ATT NOLLAN SKULLE SLIPPA PHÖZ NOLLAN?!")
        print("KNAPPAST TROOOLIGT")
        if found_treasure:
            found_treasure = False
            print("HMMMMM... VAD HAR NOLLAN DÄRRR NOLLAN?!")
            print("HAR NOLLAN EN GYLLENDE BÄSK NOLLAN?!")
            print("MINDRE URUSELT, GIVETVIS...")
            print("Phöz walks up to you and rips the Gyllende Bäsk from your hands.")
            print("HÖPP HÖPP, ÅTERGÅÅÅ NOLLAN")
            print("-----------------------------")
            print("Phöz grabs you by the shirt and throws you away!")
            rand_x, rand_y = self.random_cord(map, mapsize)
            movement.item_init(rand_x, rand_y, map, mapsize, "P", admin, diff, old_row, old_col)
            return found_treasure
        else:
            print("-----------------------------")
            print("Phöz slowly walks up to you and smashes your head with Phözner, killing you instantly.")
        if admin:
            print(f"DEBUGG: Treasure set to: {found_treasure}")

class Start(Generation):
    """Klass för start"""
    pass

class Treasure(Generation):
    """Klass för skatten"""
    def init_t(self, map, mapsize: int, old_row: int, old_col: int, admin: bool, diff: str) -> bool:
        """initialiserande metod för skatten.
            Argument:
                map(list): spelkartan
                mapsize(int): spelkartans storlek
                old_row(int): skattens rad position
                old_col(int): skattens kolumn position
                admin(bool): spelarens admin status
            Retunerar:
                found_treasure(bool): updaterar skatt statusen"""
        global found_treasure
        found_treasure = True
        if admin:
            print(f"DEBUGG: Treasure set to: {found_treasure}")
        print("-----------------------------")
        print("You enter a room a find a chest!")
        print("Upon inspection, you find a golden Bäska Droppar.\nPerhaps it could prove useful...")
        movement.item_init(None, None, map, mapsize, "T", admin, diff, old_row, old_col)
        return found_treasure

class Bats(Generation):
    """Klass för fladdermöss"""
    def init_b(self, map, mapsize: int, old_row: int, old_col: int, admin: bool, diff: str) -> None:
        """initialiserande metod för fladdermössen. Flyger spelaren till
        ett slumpmässigt rum.
            Argument:
                map(list): spelkartan
                mapsize(int): spelkartans storlek
                old_row(int): fladdermössens rad position
                old_col(int): fladdermössens kolumn position
                admin(bool): spelarens admin status
            Retunerar:
                None"""
        rand_x, rand_y = self.random_cord(map, mapsize)
        print("-----------------------------")
        print("You enter a room filled with bats!")
        print("They grab you and fly you away to another room...")
        movement.item_init(rand_x, rand_y, map, mapsize, "B", admin, diff, old_row, old_col)
      
def spawner(map, mapsize: int, start: int, phoz: int, hole: int, treasure: int, bats: int, admin: bool) -> None:
    """Genererar X antal kartobjekt för varje kartobjekt.
        Argument:
            map(list): spelkartan
            mapsize(int): spelkartans storlek
            start(int): mängd startpunkter
            phoz(int): mängd phöz
            hole(int): mängd hål
            treasure(int): mängd skatt
            bats(int): mängd fladdermöss
            admin(bool): spelarens admin status
        Retunerar:
            None"""
    global found_treasure
    found_treasure = False
    start = Start("S", start)
    start.generate(map, mapsize)
    spawn_phoz(map, mapsize, phoz)
    hole = Hole("H", round(hole * 0.01 * mapsize**2))
    hole.generate(map, mapsize)
    treasure = Treasure("T", treasure)
    treasure.generate(map, mapsize)
    bats = Bats("B", round(bats * 0.01 * mapsize**2))
    bats.generate(map, mapsize)
    print(f"A procedurally generated map with the size {mapsize}*{mapsize} has been generated.")
    if admin:
            print(f"DEBUGG: Treasure set to: {found_treasure}")

def spawn_phoz(map, mapsize: int, phoz: int) -> None:
    """Genererar Phöz på kartan"""
    phoz = Phoz("P", phoz)
    phoz.generate(map, mapsize)
