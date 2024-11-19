import colorama
from colorama import Fore, Style

colorama.init(autoreset=True)

class Admin():
    def __init__(self):
        self.is_admin = False

    def set_admin(self, status):
        self.is_admin = status
        print(f"{Fore.BLUE}[DEBUGG]{Style.RESET_ALL} Admin set to ", end = "")
        if status:
            print(f"{Fore.BLUE}True{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}False{Style.RESET_ALL}")