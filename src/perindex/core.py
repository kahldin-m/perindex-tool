# core.py
# IMPORTS
# from rich.console import Console # 14.3.3
import os
import math
import yaml
import shutil

from rich import box, print
from rich.panel import Panel


# CONSTANTS
VERSION = 1
DEBUG_MODE = 0
DIRECTORY_TEST = "data/test"
CHAR_FILES = os.listdir(DIRECTORY_TEST)

CREATE_START = """
  Follow the prompts below to complete the character creation process.
  The following fields will appear in order:
======================================================================
  1. Name               6. Race/Species
  2. Title              7. Skin Color
  3. Gender             8. Hair Color
  4. Class/Role         9. Eye Color
  5. World/Setting      10. Tags
"""

CREATE_END = """
  Finally, what color from the list below would you like
  to be associated with this character in the archive systems?
  Brighter variants are also available: Bold Red, Bold Green, etc..
======================================================================
  - [red]Red[/] ([bold red]bold[/])           - [magenta]Magenta[/] ([bold magenta]bold[/])
  - [yellow]Yellow[/] ([bold yellow]bold[/])        - [white]White[/] ([bold white]bold[/])
  - [green]Green[/] ([bold green]bold[/])         - [black on white]Black[/] ([bold black on white]bold[/])
  - [cyan]Cyan[/] ([bold cyan]bold[/])
  - [blue]Blue[/] ([bold blue]bold[/])
"""

AVAILABLE_COLORS = {
    "red",
    "yellow",
    "green",
    "cyan",
    "blue",
    "magenta",
    "black",
    "white",
    "bold red",
    "bold yellow",
    "bold green",
    "bold cyan",
    "bold blue",
    "bold magenta",
    "bold black",
    "bold white",
}

LOAD_START = """
  Enter a name for the card you would like to load.
  Partial names are allowed.
"""

ARCHIVE_START = """
  Please select a sort method:
  (Sorted alphabetically by default)
======================================================================
  1. First Name             6. Race/Species
  2. Last Name              7. Tags
  3. Gender
  4. Class/Role
  5. World/Setting
"""


# UTILS

# Clean up the terminal space
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# console = Console()
def capatalize_keys(data):
    new_data = {}
    for key, value in data.items():
        new_key = key.replace("_", " ").title()
        new_data[new_key] = value
    return new_data


# CLI TOOLS
# SAVE FUNCTION
def save_character_yaml(char_data, directory):
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)

    # Noramlize filename to lowercase and spaces to underscores
    # then build the full path safely.
    safe_fname = char_data["first_name"].strip().replace(" ", "_").lower()
    if char_data["last_name"] != "":
        safe_lname = char_data["last_name"].strip().replace(" ", "_").lower()
        file_name = f"{safe_fname}_{safe_lname}.yaml"
    else:
        file_name = f"{safe_fname}.yaml"
    full_path = os.path.join(directory, file_name)

    # Prevent accidental overrites
    if os.path.exists(full_path):
        print(
            f"\n[red]File '{file_name}' already exists. Creating incremented character.[/]"
        )
        if char_data["last_name"] != "":
            safe_lname = char_data["last_name"].strip().replace(" ", "_").lower()
            file_name = f"{safe_fname}_{safe_lname}_01.yaml"
        else:
            file_name = f"{safe_fname}_01.yaml"
        full_path = os.path.join(directory, file_name)

    # Write YAML character card!
    if DEBUG_MODE:
        print(f"[yellow]DEBUG absolute path: {os.path.abspath(full_path)}[/]")
    with open(full_path, "w", encoding="utf-8") as file:
        yaml.dump(char_data, file, sort_keys=False)

    print(f"[bold green]Saved character to archive at:[/] '{full_path}'")
    return True

# CREATE FUNCTION
def create_character():
    new_char = {
        "version": VERSION,
        "first_name": "",
        "middle_name": "",
        "last_name": "",
        "title": "",
        "gender": "",
        "role": "",
        "world": "",
        "race": "",
        "skin": "",
        "hair": "",
        "eye": "",
        "tags": [],
        "card_color": "",
    }

    print(Panel.fit(CREATE_START, title="CHARACTER CREATOR", box=box.DOUBLE))
    new_char["first_name"] = input("First name: ")
    new_char["middle_name"] = input("Middle name: ")
    new_char["last_name"] = input("Last name: ")
    new_char["gender"] = input("Gender: ")
    new_char["role"] = input("Class or role (wizard, acrobat, monk): ")
    new_char["world"] = input("World or setting the character is from: ")
    new_char["race"] = input("Race or species: ")
    new_char["skin"] = input("Skin color or tone (peach, dark, purple): ")
    new_char["hair"] = input("Hair color: ")
    new_char["eye"] = input("Eye color: ")
    tags = True
    print("""\n>> Add additional tags (press Enter with no text to finish).
   Example tags: tall, chef, evil, eyepatch, robot arm, mute
""")
    while tags:
        choice = input("Tag to add: ")
        if choice != "":
            new_char["tags"].append(choice)
            continue
        tags = False
    color_picking = True
    while color_picking:
        clear()
        print(Panel.fit(CREATE_END, title="CHARACTER CREATOR", box=box.DOUBLE))
        color_choice = input("Card color: ").lower()
        if color_choice in AVAILABLE_COLORS:
            if color_choice == "black":
                new_char["card_color"] = "black on white"
            elif color_choice == "bold black":
                new_char["card_color"] = "bold black on white"
            else:
                new_char["card_color"] = color_choice
            color_picking = False
        else:
            print(
                f"\n  '{color_choice}' is an invalid option. Please choose from the available colors listed above."
            )
            input("Press Enter to continue...")

    save_character_yaml(new_char, DIRECTORY_TEST)

# LOAD FUNCTION
def load_character_yaml():
    searching = True
    file_path = ""

    while searching:
        print(Panel.fit(LOAD_START, box=box.DOUBLE))
        name = input(">> ").lower()

        # Normalizing search key
        search_key = "_".join(name.split())
        matches = []
        for char in CHAR_FILES:
            lower_name = char.lower()
            if search_key in lower_name:
                matches.append(char)

        if len(matches) == 0:
            print(f"\n  Unable to locate character card for '{name}'.")
            input("\nPress Enter to continue...")
            continue

        if len(matches) == 1:
            file_path = matches[0]
            print(
                f"\n  Match found for '{name}' {file_path}! Loading character card..."
            )
            input("\nPress Enter to continue...")
            searching = False
            continue

        if len(matches) > 1:
            print(f"\n  Multiple matches found for '{name}'")
            for i, f in enumerate(matches, 1):
                print(f"    {i}. {f}")
            idx = input("\nSelect a character by number: ").strip()
            if not idx.isdigit():
                print("\n  Please enter a valid number.")
                continue

            selection = int(idx)
            if selection < 1 or selection > len(matches):
                print(f"\n  That number is out of range: (1-{len(matches)})")
                continue

            # Valid selection
            file_path = matches[selection - 1]
            print(f"\n  Loading character card: ({file_path})")
            input("\nPress Enter to continue...")
            searching = False

    # Load YAML
    card_path = os.path.join(DIRECTORY_TEST, file_path)
    with open(card_path, "r") as file:
        char_card = yaml.safe_load(file)
        return char_card

# DISPLAY FUNCTION
def display_character_card(char_data):
    panel_style = f"{char_data['card_color']}"
    name_parts = [char_data.get("first_name", ""), char_data.get("middle_name", ""), char_data.get("last_name", "")]
    name_full = " ".join(p for p in name_parts if p)
    left = [
        f'Name: {name_full}',
        f'Title: {char_data.get("title")}',
        f'Role: {char_data.get("role")}',
        f'Race: {char_data.get("race")}',
        f'Hair: {char_data.get("hair")}',
    ]

    right = [
        f'Gender: {char_data.get("gender")}',
        f'Style: {char_data.get("card_color")}',
        f'World: {char_data.get("world")}',
        f'Skin: {char_data.get("skin")}',
        f'Eye: {char_data.get("eye")}',
    ]
    
    lines = []
    for l, r in zip(left, right):
        lines.append(f"{l:<30} {r}")
    tags_str = ", ".join(char_data.get("tags", ""))
    lines.append(f"Tags: {tags_str}")
    
    # Previously: LOAD_CARD = yaml.dump(capatalize_keys(char_data), sort_keys=False)
    LOAD_CARD = "\n".join(lines)
    print(
        Panel.fit(
            LOAD_CARD,
            style=panel_style,
            title=f"[{char_data.get('card_color', 'white')}]{char_data['first_name']}'s CHARACTER CARD",
            safe_box=True,
            box=box.DOUBLE,
        )
    )

# ARCHIVE HELPER
def build_display(card, attr_name):
    # Build base name
    fn = card.get("first_name", "")
    ln = card.get("last_name", "")
    if fn and ln:
        base_name = f"{fn} {ln}"
    else:
        base_name = fn or ln or "zUnknown Name"
    
    # NAME SORT MODES
    if attr_name == "first_name":
        return base_name
    elif attr_name == "last_name":
        if ln and fn:
            return f"{fn} ({ln})"
        if ln:
            return ln
        return fn
        
    # ATTRBUTE SORT MODE
        
    # Take an attribute: "gender", "world", "role" etc.
    attr_value = card.get(f"{attr_name}", "")
    if isinstance(attr_value, list):
        attr_value = ", ".join(tag.lower() for tag in attr_value)
    attr_part = f"({attr_value})" if attr_value else ""

    return f"{base_name} {attr_part}".strip()

# ARCHIVE DISPLAY
def archive_display_cards(cards):
    height = shutil.get_terminal_size().lines
    twidth = shutil.get_terminal_size().columns
    wresize = 72 if twidth > 72 else twidth
    usable = height - 6  # Adjusting for panel borders, title, padding
    
    # Using a paging loop to ensure readability if the archive is bigger than 10 cards
    current_page = 1
    total_cards = len(cards) # Actually total_cards ...
    total_pages = max(1, math.ceil(total_cards / usable))
    index = 0
    
    while index < total_cards:
        page = cards[index:index + usable]
        clear()
        print(Panel("\n".join(page), title=f"Page {current_page}/{total_pages}", box=box.DOUBLE, width=wresize, padding=1))
        index += usable
        current_page += 1
        if index < total_cards:
            input("\nPress Enter to go to next page >>")


# SORT LOGIC
def archive_sort_cards(sort_type):
    cards = []
    for f in CHAR_FILES:
        with open(os.path.join(DIRECTORY_TEST, f), "r") as file:
            card = yaml.safe_load(file)
            cards.append(card)

    match sort_type:
        case "1":
            print("[green]OPTION 1: First Name[/]")
            sorted_cards = sorted(cards, key=lambda c: c.get("first_name", ""))
            display = [build_display(c, "first_name") for c in sorted_cards]
            archive_display_cards(display) 
        case "2":
            print("[blue]OPTION 2: Last Name[/]")
            sorted_cards = sorted(cards, key=lambda c: c.get("last_name", ""))
            display = [build_display(c, "last_name") for c in sorted_cards]
            archive_display_cards(display) 
        case "3":
            print("[red]OPTION 3: Gender[/]")
            sorted_cards = sorted(cards, key=lambda c: c.get("gender", ""))
            display = [build_display(c, "gender") for c in sorted_cards]
            archive_display_cards(display) 
        case "4":
            print("[green]OPTION 4: Role[/]")
            sorted_cards = sorted(cards, key=lambda c: c.get("role", ""))
            display = [build_display(c, "role") for c in sorted_cards]
            archive_display_cards(display) 
        case "5":
            print("[blue]OPTION 5: World[/]")
            sorted_cards = sorted(cards, key=lambda c: c.get("world", ""))
            display = [build_display(c, "world") for c in sorted_cards]
            archive_display_cards(display) 
        case "6":
            print("[red]OPTION 6: Race[/]")
            sorted_cards = sorted(cards, key=lambda c: c.get("race", ""))
            display = [build_display(c, "race") for c in sorted_cards]
            archive_display_cards(display) 
        case "7":
            print("[green]OPTION 7: Tags[/]")
            sorted_cards = sorted(cards, key=lambda c: ', '.join(tag.lower() for tag in c.get("tags", [])))
            display = [build_display(c, "tags") for c in sorted_cards]
            archive_display_cards(display) 
        case _:
            print("Invalid sort type/out of option range (1-10)")

# SORT DISPLAY
def archive_select_mode():
    print(Panel.fit(ARCHIVE_START, box=box.DOUBLE))
    choice = input("Sort type number:  ")
    clear()
    archive_sort_cards(choice)