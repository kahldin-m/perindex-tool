# cli.py
# IMPORTS
import sys
import perindex.core as core

from rich import print
from rich.panel import Panel
from rich import box


# UTILS
def close():
    print("\n>> Exiting Perindex-Tool")
    sys.exit(0)

def welcome_screen():
    hourly_color = core.get_hourly_color()
    print(Panel(core.WELCOME_TEXT, expand=False, title="[Main Menu]", box=box.DOUBLE, style=hourly_color))
    return input(">>  ").strip().upper()

# MAIN
def main():
    try:
        core.clear()
        # choice branches
        while True:
            
            n = welcome_screen()
            if n in {"1", "CREATE"}:
                core.clear()
                core.create_character()
            elif n in {"2", "LOAD", "UPDATE", "EDIT"}:
                core.clear()
                loading = True
                while loading:
                    card_data = core.load_character_yaml()
                    if card_data is None:
                        loading = False
                        continue
                    core.display_character_card(card_data)
                    continue
            elif n in {"3", "VIEW"}:
                core.clear()
                core.archive_select_mode()
            elif n in {"4", "LIST"}:
                core.clear()
                core.overview_display()
            elif n in {"5", "EXIT"}:
                core.clear()
                close()
            elif n == "LASKO":
                core.clear()
                core.dev_tool()
            elif n == "CLEAN":
                core.clear()
                core.clean_yamls()
            else:
                print("\nInvalid selection. Select from 1-5 or type CREATE/LOAD/VIEW/LIST/EXIT.")
            core.clear()
    except KeyboardInterrupt:
        close()
    except Exception as e:
        print(f"\n  [bold red]An error has occured:[/]\n  - {e}")
        close()


if __name__ == "__main__":
    main()
