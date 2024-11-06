"""GUI för Phöz Rooms"""
from PIL import Image, ImageTk
import tkinter as tk

class Gui(tk.Tk):
    def __init__(self):
        super().__init__(self)
        self.title("Phöz Rooms")

    def hide(self, entity):
        entity.destroy()

    def game_gui(self):
        root = tk.Tk()
        root.title("Phöz Rooms")

        # Menu
        menu = tk.Menu(root)
        root.config(menu=menu)
        filemenu = tk.Menu(menu)
        menu.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Back to Main Menu")
        filemenu.add_command(label="Run as Admin")
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=root.quit)

        # Buttons
        self.button1 = tk.Button(root, text="Button 1", width=15)
        self.button2 = tk.Button(root, text="Button 2", width=15)
        self.button3 = tk.Button(root, text="Button 3", width=15)
        self.button4 = tk.Button(root, text="Button 4", width=15, command=lambda: self.hide(self.button4))

        # Image
        image = Image.open("Capture6.png")
        re_image = ImageTk.PhotoImage(image.resize((960, 540)))

        self.image = tk.Label(root, image=re_image)

        # Place
        self.button1.place(x=900, y=800)
        self.button2.place(x=780, y=830)
        self.button3.place(x=1020, y=830)
        self.button4.place(x=900, y=860)
        self.image.place(x=475, y=100)


        tk.mainloop()

gui = Gui()
gui.game_gui()
