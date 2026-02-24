# cli.py
# IMPORTS
import os
import sys
import perindex.core as core

from rich import print
from rich.panel import Panel
from rich import box

# CONSTANTS
WELCOME_TEXT = """
  Welcome to Perindex character archival tool. Type a number
  or action from the list below:
        
======================================================================
    [1] CREATE Character Card
    [2] LOAD Character Card
    [3] VIEW Character Archive
    [4] EXIT
""" # was 63 '-' , 5 text 5 || 5 |

# UTILS
def close():
    print("\n>> Exiting Perindex-Tool")
    sys.exit(0)
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def welcome_screen():
    print(Panel(WELCOME_TEXT, expand=False, box=box.DOUBLE))
    return input(">>  ").strip().upper()

# MAIN
def main():
    try:
        clear()
        # choice branches
        while True:
            
            n = welcome_screen()
            if n in {"1", "CREATE"}:
                clear()
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
