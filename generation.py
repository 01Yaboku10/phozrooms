import random
import failsafe
import movement

class Generation():
    
    def __init__(self, spawn, spawns, movement_inst=None):
        self.spawn = spawn
        self.spawns = spawns
        self.movement_inst = movement_inst

    def random_cord(self, map, mapsize):
        i = 0
        while i < 1:
            rand_x = random.randint(0, mapsize - 1)
            rand_y = random.randint(0, mapsize - 1)
            if failsafe.map_is_empty(map, rand_x, rand_y):
                i += 1
        return rand_x, rand_y

    def generate(self, map, MAPSIZE):
        """Lägger till alla kartobjekt till kartan i slumpmässiga rum."""
        i = 0
        while i < self.spawns:
            rand_x, rand_y = self.random_cord(map, MAPSIZE)
            map[rand_x][rand_y] = self.spawn
            i += 1

class Hole(Generation):
    def init_h(self):
        print("-----------------------------")
        print("You fell into a hole -- falling to your demise!")

class Phoz(Generation):
    def init_p(self, map, mapsize, old_row, old_col, admin):
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
            movement.item_init(rand_x, rand_y, map, mapsize, "P", admin, old_row, old_col)
            return found_treasure
        else:
            print("-----------------------------")
            print("Phöz slowly walks up to you and smashes your head with Phözner, killing you instantly.")
        if admin:
            print(f"DEBUGG: Treasure set to: {found_treasure}")

class Start(Generation):
    pass

class Treasure(Generation):
    def init_t(self, map, mapsize, old_row, old_col, admin):
        global found_treasure
        found_treasure = True
        if admin:
            print(f"DEBUGG: Treasure set to: {found_treasure}")
        print("-----------------------------")
        print("You enter a room a find a chest!")
        print("Upon inspection, you find a golden Bäska Droppar.\nPerhaps it could prove useful...")
        movement.item_init(None, None, map, mapsize, "T", admin, old_row, old_col)
        return found_treasure

class Bats(Generation):
    def init_b(self, map, mapsize, old_row, old_col, admin):
        rand_x, rand_y = self.random_cord(map, mapsize)
        print("-----------------------------")
        print("You enter a room filled with bats!")
        print("They grab you and fly you away to another room...")
        movement.item_init(rand_x, rand_y, map, mapsize, "B", admin, old_row, old_col)
      
def spawner(map, MAPSIZE, START, PHOZ, HOLE, TREASURE, BATS, admin):
    """Genererar X antal kartobjekt för varje kartobjekt"""
    global found_treasure
    found_treasure = False
    start = Start("S", START)
    start.generate(map, MAPSIZE)
    spawn_phoz(map, MAPSIZE, PHOZ)
    hole = Hole("H", round(HOLE * 0.01 * MAPSIZE**2))
    hole.generate(map, MAPSIZE)
    treasure = Treasure("T", TREASURE)
    treasure.generate(map, MAPSIZE)
    bats = Bats("B", round(BATS * 0.01 * MAPSIZE**2))
    bats.generate(map, MAPSIZE)
    print(f"A procedurally generated map with the size {MAPSIZE}*{MAPSIZE} has been generated.")
    if admin:
            print(f"DEBUGG: Treasure set to: {found_treasure}")

def spawn_phoz(map, MAPSIZE, PHOZ):
    phoz = Phoz("P", PHOZ)
    phoz.generate(map, MAPSIZE)