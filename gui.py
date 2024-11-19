# https://docs.python.org/3/library/tkinter.html
# https://www.pygame.org/docs/ref/mixer.html

from PIL import Image, ImageTk
import tkinter as tk
import colorama
from colorama import Fore, Style
import pygame
import admin
import scoreboard
import difficulty
import failsafe
import map
import movement
import phoz
import weapon

colorama.init(autoreset=True)
pygame.mixer.init() # Init pygame sound mixer

class Gui(tk.Tk):
    def __init__(self):
        super().__init__()
        self.get_admin = admin.Admin()
        self.admin = self.get_admin.is_admin
        self.get_admin.set_admin(False)
        self.title("Phöz Rooms")
        self.geometry("1920x1080")
        self.main_menu()
    
    def set_title(self, text: str):
        self.title_text = tk.Label(self, text=text, font=("Helvetica", 36))
        self.title_text.pack(pady=20)
    
    def cont_button(self, command: str):
        self.continue_bt = tk.Button(self, text="Continue", width=15, command = command, font=("Helvetica", 18))
        self.continue_bt.place(relx=0.5, rely=0.9, anchor="s")

    def set_button(self, command: str, name: str, posy: int = 20, width: int = 20):
        self.button = tk.Button(self, text=name, width=width, command = command, font=("Helvetica", 18))
        self.button.pack(pady=posy)

    def set_render(self, render: str, x_pos: float = 0.5, y_pos: float = 0.65):
        if self.get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Setting render to {render}")
        image = Image.open(f"renders/render{render}.png")
        self.re_image = ImageTk.PhotoImage(image.resize((960, 540)))
        self.photo = tk.Label(self, image=self.re_image)
        self.photo.place(relx=x_pos, rely=y_pos, anchor="s")
    
    def set_message(self, message: str, ypos: float = 0.8):
        self.message = tk.Label(self, text=message, font=("Helvetica", 26))
        self.message.place(relx=0.5, rely=ypos, anchor="s")

    def play_sound(self, sound: str, volume: float = 0.2):
        if self.get_admin.is_admin:
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Playing audio: {sound}")
        audio = pygame.mixer.Sound(f"audio/{sound}.mp3")
        pygame.mixer.Sound.play(audio)
        pygame.mixer.Sound.set_volume(audio, volume)
    
    def stop_sound(self):
        pygame.mixer.stop()

    def file_menu(self):
        menu = tk.Menu(self)
        self.config(menu=menu)
        self.filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=self.filemenu)
        self.filemenu.add_command(label="Back to Main Menu", command=self.main_menu)
        self.filemenu.add_command(label="Run as Admin", command=lambda: self.get_admin.set_admin(True))
        self.filemenu.add_separator()
        self.filemenu.add_command(label="Exit", command=self.quit)

    def clear_screen(self):
        for i in self.winfo_children(): # winfo_children: list of widgets
            widget = i.winfo_class()
            if widget != "Menu":
                i.destroy()
            
    def main_menu(self):
        self.clear_screen()
        self.stop_sound()
        self.file_menu()
        
        e_score = scoreboard.get_score("e", self.get_admin)
        n_score = scoreboard.get_score("n", self.get_admin)
        h_score = scoreboard.get_score("h", self.get_admin)
        f_score = scoreboard.get_score("f", self.get_admin)

         # File menu
        self.file_menu()

         # Sound
        self.play_sound("phoz_maintheme")

         # Title
        self.set_title("Välkommen till Phöz mindre urusla spel")

         # Images
        image = Image.open("renders/render22.png")
        self.re_image = ImageTk.PhotoImage(image.resize((760, 640)))
        self.photo1 = tk.Label(self, image=self.re_image)
        self.photo2 = tk.Label(self, image=self.re_image)
        self.photo1.place(relx=0.1, rely=0.75, anchor="s")
        self.photo2.place(relx=0.9, rely=0.75, anchor="s")

         # Buttons
        self.new_game_button = tk.Button(self, text="New Game", width=20, font=("Helvetica", 18), command=self.name_menu)
        self.exit_button = tk.Button(self, text="Exit", width=20, font=("Helvetica", 18), command=self.quit)

         # Place Buttons
        self.new_game_button.place(relx=0.5, rely=0.2, anchor="s")
        self.exit_button.place(relx=0.5, rely=0.3, anchor="s")

         # Scoreboard Title
        self.scores_label = tk.Label(self, text="Top 10 Minst Urusla Spelare", font=("Helvetica", 24, "bold"))
        self.scores_label.place(relx=0.5, rely=0.4, anchor="s")

         # Scoreboard Frame
        self.scoreboard_frame = tk.Frame(self)
        self.scoreboard_frame.place(relx=0.5, rely=0.75, anchor="s")

         # Top 10 scores for each difficulty
        self.difficulties_scores = {
        "Easy": [(e_score[i] if i < len(e_score) else None) for i in range(10)],
        "Normal": [(n_score[i] if i < len(n_score) else None) for i in range(10)],
        "Hard": [(h_score[i] if i < len(h_score) else None) for i in range(10)],
        "Fadder": [(f_score[i] if i < len(f_score) else None) for i in range(10)]
    }

         # Display scores
        column = 0
        for difficulty, scores in self.difficulties_scores.items():
             # Title
            difficulty_label = tk.Label(self.scoreboard_frame, text=difficulty, font=("Helvetica", 20, "bold"))
            difficulty_label.grid(row=0, column=column, padx=20)

             # Display scores
            for i, score in enumerate(scores, start=1):
                name = score.name if score is not None else "N/A"
                highscore = score.score if score is not None else "N/A"
                if score is not None:
                    score_label = tk.Label(self.scoreboard_frame, text=f"{i}. {name}: {highscore} pts", font=("Helvetica", 16))
                    score_label.grid(row=i, column=column, padx=20, pady=5)

            column += 1  # Move to the next column for the next difficulty

    def name_menu(self):
        self.clear_screen()
        self.set_title("Vad är Nollans namn, Nollan?")
        self.cont_button(self.name_menu_2)
        
        # Text Input
        self.name = tk.Text(self, heigh = 5, width = 60)
        self.name.place(relx=0.5, rely=0.5, anchor="s")
        self.name.bind("<Return>", self.enter)
    
    def enter(self, key):
        self.name_menu_2()

    def name_menu_2(self):
        self.continue_bt.destroy() # Ta bort knappen
        name = self.name.get(1.0, "end-1c").capitalize().strip()
        if name == "Nollan":
            self.playername = name
            self.name.destroy()
            self.difficulty_menu()

        elif name == "Fadder":
            self.playername = name
            self.set_render("22", 0.5, 0.8)
            self.set_title("Ska Fadder visa Nollan hur man spelar Phöz Rooms, Fadder?")
            self.set_title("Mindre uruselt...")
        
        else:
            self.playername = "Nollan"
            self.set_title("KNAPPAST TROLIGT")
            self.set_title("Nollan heter givetvis Nollan, Nollan.")

        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Playername set to: {self.playername}")
        self.name.destroy()
        self.cont_button(self.difficulty_menu)

    def difficulty_menu(self):
        self.clear_screen()
        self.set_title(f"Givetvis {self.playername} välja svårighetsgrad, {self.playername}")

        # Buttons
        self.set_button(lambda: self.set_diff("E"), "Easy")
        self.set_button(lambda: self.set_diff("N"), "Normal")
        self.set_button(lambda: self.set_diff("H"), "Hard")
        self.set_button(lambda: self.set_diff("F"), "Fadder")
    
    def difficulty_menu_2(self):
        self.clear_screen()
        self.set_render("22", 0.5, 0.8)
        self.set_title("KNAPPAST TROLIGT")
        self.set_title("Givetvis ska Fadder köra på Fadder svårighetsgraden, Fadder!")

        self.cont_button(self.game_window)

    def set_diff(self, diff):
        if self.playername == "Fadder" and diff != "F":
            self.difficulty = "F"
            self.set_difficulty = difficulty.fadder
            self.difficulty_menu_2()
        else:
            self.difficulty = diff
            self.set_difficulty = failsafe.set_diff(diff)
            self.game_window()
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Difficulty set to: {self.difficulty}")

    def game_window(self):
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Game Window started...")
        self.clear_screen()
        self.stop_sound()
        self.play_sound("theme1")

        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Creating Game_map...")
        self.game_map_inst = map.Game_map(self.set_difficulty, self.get_admin)
        self.game_map = self.game_map_inst.game_map
        self.mapsize = self.game_map_inst.mapsize
        self.filemenu.add_command(label="Print Map", command=lambda: self.game_map_inst.generate_map())

        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Starting movement...")
        self.phoz = phoz.Phoz(self.game_map, self.get_admin, self.mapsize, self)
        self.movement_inst = movement.Movement(self.game_map, self.mapsize, self.difficulty, self.get_admin, self.game_map_inst, self.phoz)
        self.ask_directions()

    def ask_directions(self):
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Asking for directions...")
        self.clear_screen()
        self.set_title(f"Current room: {self.movement_inst.current_room}")
        self.set_render(failsafe.is_render(self.movement_inst.current_row,
        self.movement_inst.current_col, self.movement_inst.mapsize,
        str(self.game_map[self.movement_inst.current_row][self.movement_inst.current_col])))
        west, east, north, south = self.movement_inst.ask_direction()
        if north:
            self.button_n = tk.Button(self, text="North", width=15, command=lambda: self.movement_inst.move("N", self))
            self.button_n.place(relx=0.5, rely=0.8, anchor="s")
        if west:
            self.button_w = tk.Button(self, text="West", width=15, command=lambda: self.movement_inst.move("W", self))
            self.button_w.place(relx=0.425, rely=0.85, anchor="s")
        if east:
            self.button_e = tk.Button(self, text="East", width=15, command=lambda: self.movement_inst.move("E", self))
            self.button_e.place(relx=0.575, rely=0.85, anchor="s")
        if south:
            self.button_s = tk.Button(self, text="South", width=15, command=lambda: self.movement_inst.move("S", self))
            self.button_s.place(relx=0.5, rely=0.9, anchor="s")

    def phoz_near(self, weapon, shots):
        self.clear_screen()
        self.set_title(f"Current room: {self.movement_inst.current_room}")
        self.set_message("Du kan höra grymtningar och rosslingar...", 0.75)
        self.set_render(failsafe.is_render(self.movement_inst.current_row,
        self.movement_inst.current_col, self.movement_inst.mapsize,
        str(self.game_map[self.movement_inst.current_row][self.movement_inst.current_col])))
        self.cont_button(lambda: self.shoot_directions(weapon, shots))

    def phoz_hit(self, hit, phoz, phoz_row = 0, phoz_col = 0):
        self.clear_screen()
        self.set_title(f"Current room: {self.movement_inst.current_room}")
        self.set_render(failsafe.is_render(self.movement_inst.current_row,
        self.movement_inst.current_col, self.movement_inst.mapsize,
        str(self.game_map[self.movement_inst.current_row][self.movement_inst.current_col])))
        if hit:
            self.set_message("Heineken träffade phöz!", 0.75)
            self.movement_inst.overwrite(phoz_row, phoz_col)
            print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Checking Phöz Status...")
            if phoz.is_alive():
                self.cont_button(self.ask_directions)
            else:
                self.cont_button(self.victory)
        else:
            self.set_message("Du missade phöz...", 0.75)
            self.cont_button(self.ask_directions)

    def shoot_directions(self, weapon: object, shots):
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Asking for shoot directions...")
        self.clear_screen()
        self.set_title(f"Current room: {self.movement_inst.current_room}")
        self.set_message(f"Throw {shots} / 3", 0.75)
        self.set_render(failsafe.is_render(self.movement_inst.current_row,
        self.movement_inst.current_col, self.movement_inst.mapsize,
        str(self.game_map[self.movement_inst.current_row][self.movement_inst.current_col])))
        west, east, north, south = weapon.ask_direction()
        if north:
            self.button_n = tk.Button(self, text="North", width=15, command=lambda: weapon.shoot("N"))
            self.button_n.place(relx=0.5, rely=0.8, anchor="s")
        if west:
            self.button_w = tk.Button(self, text="West", width=15, command=lambda: weapon.shoot("W"))
            self.button_w.place(relx=0.425, rely=0.85, anchor="s")
        if east:
            self.button_e = tk.Button(self, text="East", width=15, command=lambda: weapon.shoot("E"))
            self.button_e.place(relx=0.575, rely=0.85, anchor="s")
        if south:
            self.button_s = tk.Button(self, text="South", width=15, command=lambda: weapon.shoot("S"))
            self.button_s.place(relx=0.5, rely=0.9, anchor="s")
    
    def gameover(self, message):
        self.clear_screen()
        self.stop_sound()
        self.set_message(message)
        self.set_render("21")
        self.play_sound("dead")
        self.cont_button(self.main_menu)
    
    def victory(self):
        self.clear_screen()
        self.stop_sound()
        self.set_message("Phöz är elimenerad, för nu...")
        scoreboard.set_score(self.difficulty, scoreboard.final_score(), self.playername)