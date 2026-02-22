# cli.py
# IMPORTS
import os
import sys
import perindex.core as core

# CONSTANTS
WELCOME_TEXT = """
--------------------------------------------------------------
||                                                    ||     |
||    WELCOME TO PERINDEX CHARACTER ARCHIVAL TOOL     ||     |
||                                                    ||     |
--------------------------------------------------------------
|| OPTIONS 1-4:                                       ||     |
||   [1] CREATE Character Card                        ||     |
||   [2] LOAD Character Card                          ||     |
||   [3] VIEW Character Archive                       ||     |
||   [4] EXIT                                         ||     |
--------------------------------------------------------------
"""

# UTILS
def close():
    print("\n>> Exiting Perindex-Tool")
    sys.exit(0)
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def welcome_screen():
    print(WELCOME_TEXT)
    return input(">>  ").strip().upper()

# MAIN
def main():
    try:
        clear()
        # choice branches
        while True:
            
            n = welcome_screen()
            if n in {"1", "CREATE"}:
                core.create_character()
            elif n in {"2", "LOAD"}:
                core.load_character()
            elif n in {"3", "VIEW"}:
                core.plain_list()
            elif n in {"4", "EXIT"}:
                close()
            else:
                print("\nInvalid option. Select 1-4 or type CREATE/LOAD/VIEW/EXIT.")
            input("\nPress Enter to continue...")
    except KeyboardInterrupt:
        close()


if __name__ == "__main__":
    main()
