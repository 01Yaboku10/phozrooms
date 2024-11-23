import failsafe
import random
import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class Game_map():
    def __init__(self, diff: object, get_admin: object) -> None:
        self.mapsize, self.phoz, self.exam, self.treasure, self.drunkard = diff.diff_attrib()
        self.get_admin = get_admin
        global found_treasure
        found_treasure = False
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Treasure set to {found_treasure}")
        self.game_map = [[0 for _ in range(self.mapsize)] for _ in range(self.mapsize)]
        self.spawner()

    def generate_map(self) -> None:
        if failsafe.is_spawn_limit(self.mapsize, 1, self.phoz, self.exam, self.treasure, self.drunkard):
            if self.get_admin.is_admin:
                for row in self.game_map:
                    print(row)
            else:
                print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Cannot print map -- Missing Admin privileges.")
        else:
            print(f"{Fore.RED}[ERROR]{Style.RESET_ALL} Spawn items exceeds that of available spawn points.")
    
    def spawn_phoz(self):
        phoz = Phoz("P", self.phoz, self.game_map, self.mapsize, self.get_admin)
        phoz.generate()
    
    def spawner(self):
        start = Start("S", 1, self.game_map, self.mapsize, self.get_admin)
        start.generate()
        self.spawn_phoz()
        exam = Exam("E", round(self.exam * 0.01 * self.mapsize**2), self.game_map, self.mapsize, self.get_admin)
        exam.generate()
        treasure = Treasure("T", self.treasure, self.game_map, self.mapsize, self.get_admin)
        treasure.generate()
        drunkard = Drunkard("D", round(self.drunkard * 0.01 * self.mapsize**2), self.game_map, self.mapsize, self.get_admin)
        drunkard.generate()
        if self.get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} A procedurally generated map with the size {self.mapsize}*{self.mapsize} has been generated.")
        self.generate_map()


class Generation():
    def __init__(self, spawn: str, spawns: int, game_map: list[list[str]], mapsize: int, get_admin: object) -> None:
        self.spawn = spawn
        self.spawns = spawns
        self.game_map = game_map
        self.mapsize = mapsize
        self.get_admin = get_admin

    def random_cord(self, game_map: list[list[str]], mapsize: int) -> tuple[int, int]:
        i = 0
        while i < 1:
            rand_x = random.randint(0, mapsize - 1)
            rand_y = random.randint(0, mapsize - 1)
            if failsafe.slot_is_empty(game_map, rand_x, rand_y):
                i += 1
        return rand_x, rand_y
    
    def generate(self, ranx: int = 0, rany: int = 0, mode: str = "D") -> None:
        i = 0
        while i < self.spawns:
            if mode == "D":
                rand_x, rand_y = self.random_cord(self.game_map, self.mapsize)
            else:
                rand_x, rand_y = ranx, rany
            self.game_map[rand_x][rand_y] = self.spawn
            if self.get_admin.is_admin and self.spawn == "P":
                print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Phöz spawned in [{rand_y}, {rand_x}]")
            i += 1

class Start(Generation):
    pass

class Phoz(Generation):
    def init_p(self, gui: object, movement_inst: object, game_map_inst) -> None:
        self.gui = gui
        self.movement_inst = movement_inst
        self.game_map_inst = game_map_inst

        self.gui.clear_screen()
        self.gui.set_render("26")
        self.gui.play_sound("phoz1", 1.0)
        self.gui.set_message("Du blir bemött av det som är heligt...")

        self.gui.cont_button(self.page2)

    def page2(self):
        self.gui.clear_screen()
        self.gui.play_sound("phoz1", 1.0)
        self.gui.set_render("28")
        self.gui.set_message("NOOOOOOOOLLLLLLLAAAAAAAAAAAANN!!!")

        self.gui.cont_button(self.page3)

    def page3(self):
        self.gui.clear_screen()
        self.gui.play_sound("phoz1", 1.0)
        self.gui.set_render("29")
        self.gui.set_message("TRODDE NOLLAN ATT NOLLAN SKULLE SLIPPA PHÖZ NOLLAN?!")
        self.gui.set_message("KNAPPAST TROOOLIGT", 0.85)
        if found_treasure:
            self.gui.cont_button(self.page4)
        else:
            self.gui.cont_button(self.page6)
    
    def page4(self):
        self.gui.clear_screen()
        self.gui.play_sound("phoz1", 1.0)
        self.gui.set_render("25")
        self.gui.set_message("HMMMMM... VAD HAR NOLLAN DÄRRR NOLLAN?!")
        self.gui.set_message("HAR NOLLAN EN GYLLENDE BÄSK NOLLAN?!", 0.85)

        self.gui.set_button(self.page5, "Ge Phöz den Gyllende bäsken", width = 40)
    
    def page5(self):
        global found_treasure
        self.gui.clear_screen()
        self.gui.play_sound("phoz1", 1.0)
        self.gui.set_render("27")
        self.gui.set_message("MINDRE URUSELT, GIVETVIS...")
        self.gui.set_message("HÖPP HÖPP, ÅTERGÅÅÅ NOLLAN", 0.85)
        found_treasure = False
        rand_x, rand_y = self.random_cord(self.game_map, self.mapsize)
        self.movement_inst.overwrite(self.movement_inst.current_row, self.movement_inst.current_col)
        self.movement_inst.set_cords(rand_x, rand_y, "Update")
        self.relocate_phoz()

        self.gui.cont_button(lambda: self.gui.ask_directions())

    def page6(self):
        self.gui.play_sound("phoz1", 1.0)
        self.gui.clear_screen()
        self.gui.set_render("30")
        self.gui.set_message("Phöz går långsamt upp till dig...")

        self.gui.cont_button(lambda: self.gui.gameover("Med ett slag blir du dräpt av Phöz's Phözner..."))

    def relocate_phoz(self):
        phoz = Phoz("P", 1, self.game_map, self.mapsize, self.get_admin)
        i = 0
        while i < 1:
            rand_x = random.randint(0, self.mapsize - 1)
            rand_y = random.randint(0, self.mapsize - 1)
            if failsafe.slot_is_empty(self.game_map, rand_x, rand_y, "P", self.movement_inst):
                i += 1
        phoz.generate(rand_x, rand_y, "P")

class Treasure(Generation):
    def init_t(self, gui: object, movement_inst: object) -> bool:
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Running Treasure.")
        global found_treasure
        found_treasure = True
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Treasure set to True")
        self.gui = gui
        self.movement_inst = movement_inst
        self.gui.clear_screen()
        self.gui.set_render(failsafe.is_render(self.movement_inst.current_row,
        self.movement_inst.current_col, self.movement_inst.mapsize,
        str(self.game_map[self.movement_inst.current_row][self.movement_inst.current_col])))
        self.movement_inst.overwrite(self.movement_inst.current_row, self.movement_inst.current_col)
        self.gui.set_message("Du går in i ett rum med en kista...")

        self.gui.cont_button(self.page2)
    
    def page2(self):
        self.gui.clear_screen()
        self.gui.play_sound("chest", 1.0)
        self.gui.set_render("13")
        self.gui.set_message("Du hittade en Gyllende Bäsk! Den kanske kan vara användbar...")
        
        self.gui.cont_button(lambda: self.gui.ask_directions())

class Exam(Generation):
    def init_e(self, gui: object, movement_inst: object) -> None:
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Running Exam.")
        gui.clear_screen()
        gui.set_render(failsafe.is_render(movement_inst.current_row,
        movement_inst.current_col, movement_inst.mapsize,
        str(self.game_map[movement_inst.current_row][movement_inst.current_col])))
        gui.set_message("Du går in i ett rum med en Tillämpad Termodynamik tenta...")

        gui.cont_button(lambda: gui.gameover("Du hade inte pluggat tillräckligt för den..."))
        
class Drunkard(Generation):
    def init_d(self, gui: object, movement_inst: object) -> None:
        self.gui = gui
        self.movement_inst = movement_inst
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Running Drunkard.")
        self.gui.clear_screen()
        self.gui.set_render(failsafe.is_render(self.movement_inst.current_row,
        self.movement_inst.current_col, self.movement_inst.mapsize,
        str(self.game_map[self.movement_inst.current_row][self.movement_inst.current_col])))
        self.gui.set_message("Du går in i ett rum med några märkbart påverkade studenter...")

        self.gui.cont_button(self.page2)
    
    def page2(self):
        self.gui.clear_screen()
        self.gui.set_render("23")
        self.gui.set_message("Tjena mannen! Va fan gör du här nere?")

        self.gui.cont_button(self.page3)

    def page3(self):
        self.gui.clear_screen()
        self.gui.set_render("24")
        self.gui.set_message("Kom! Vi går på en promenad!")
        rand_x, rand_y = self.random_cord(self.game_map, self.mapsize)
        self.movement_inst.overwrite(self.movement_inst.current_row, self.movement_inst.current_col)
        self.movement_inst.set_cords(rand_x, rand_y, "Update")
        self.gui.cont_button(lambda: self.gui.ask_directions())

