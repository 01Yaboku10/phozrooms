import weapon
import scoreboard

def is_phoz(current_row: int, current_col: int, game_map: list, admin: bool, mapsize: int, instance) -> None:
    if admin:
        print("DEBUGG: Running is_phoz")
    for row_i, slot in enumerate(game_map):
        if "P" in slot:
            col_i = slot.index("P")
            if admin:
                print(f"DEBUGG: Phöz is in {row_i, col_i}")
                print(f"DEBUGG: checked {abs(current_row - row_i)}, {abs(current_col - col_i)}")
            if 0 <= abs(current_row - row_i) < 2 and 0 <= abs(current_col - col_i) < 2:
                print("Du kan höra gtymtningar och rosslingar...")
                weapon_inst = weapon.Weapon(current_row, current_col, mapsize, row_i, col_i, admin, instance, game_map)
                weapon_inst.aim()

def is_phoz_dead(game_map: list[list[str]]) -> bool:
    for col in game_map:
        if "P" in col:
            return False
    return True

def game_over(difficulty):
    print("-------------=+=-------------")
    print("Phöz är elimenrad ...för nu.")
    scoreboard.set_score(difficulty, scoreboard.final_score(), "Nollan")