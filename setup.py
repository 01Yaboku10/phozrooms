import os
import sys
import subprocess

def initializer(module):
    print(f"DEBUGG: Running Initializer for {module}")
    try:
        __import__(module)
    except ImportError:
        print(f"DEBUGG: {module} not found.\n Installing module...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", module]) # hjälp från StackOverflow
    print(f"DEBUGG: {module} found.")

def is_save(saves: list = ["e", "n", "h", "f"]) -> None:
    print("[DEBUGG] Looking for saves folder...")
    if not os.path.exists("saves"):
        print("[DEBUGG] No saves folder found...\nCreating new saves folder...")
        os.makedirs("saves")
        print("A new directory called saves has been created.")
    else:
        print("[DEBUGG] Save folder found!")

    for diff in saves:
        file_path = os.path.join("saves", f"save_{diff}.txt")
        if not os.path.exists(file_path):
            print(f"[DEBUGG] No save file found for difficulty [{diff}]\nCreating new save...")
            with open(file_path, "w", encoding="utf-8") as file:
                file.write("")
            print("[DEBUGG] Save created!")
        else:
            print(f"[DEBUGG] Save save_{diff} found!")

if __name__ == "__main__":
    initializer("Pillow")
    initializer("pygame")
    initializer("colorama")
    is_save()
    print("DEBUGG: Installation Complete")