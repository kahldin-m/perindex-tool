# core.py
# IMPORTS
# from rich.console import Console # 14.3.3
import os

import yaml
from rich import box, print
from rich.panel import Panel

# CONSTANTS
VERSION = 1
DEBUG_MODE = 0
DIRECTORY_TEST = "data/test"

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
  - [red]Red[/] ([bold red]bold[/])             - [magenta]Magenta[/]
  - [yellow]Yellow[/] ([bold yellow]bold[/])    - [black on white]Black[/]
  - [green]Green[/] ([bold green]bold[/])       - [white]White[/]
  - [cyan]Cyan[/]([bold cyan]bold[/])           - [bold black on white]Panda
  - [blue on black]Blue[/] ([bold blue on black]bold[/])
"""

AVAILABLE_COLORS = {
    "red",
    "yellow",
    "green",
    "cyan",
    "blue",
    "magenta",
    "black on white",
    "white",
    "bold red",
    "bold yellow",
    "bold green",
    "bold cyan",
    "bold blue",
    "bold magenta",
    "bold black on white",
    "bold white",
}

LOAD_START = """
  Enter a name for the card you would like to load.
  Partial names are allowed.
"""

AC_TEXT = """
[black on red]_Testificate[/]
[black on yellow]Alex[/]
[black on green]Baron[/]
[black on blue]Charlie[/]
[black on magenta]Vecna[/]
"""


# UTILS
# console = Console()
def capatalize_keys(data):
    new_data = {}
    for key, value in data.items():
        new_key = key.replace("_", " ").title()
        new_data[new_key] = value
    return new_data


# CLI TOOLS
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
        os.system("cls" if os.name == "nt" else "clear")
        print(Panel.fit(CREATE_END, title="CHARACTER CREATOR", box=box.DOUBLE))
        color_choice = input("Card color: ").lower()
        if color_choice in AVAILABLE_COLORS:
            new_char["card_color"] = color_choice
            color_picking = False
        else:
            print(
                f"\n  '{color_choice}' is an invalid option. Please choose from the available colors listed above."
            )
            input("Press Enter to continue...")

    save_character_yaml(new_char, DIRECTORY_TEST)


def load_character_yaml():
    searching = True
    file_path = ""

    while searching:
        char_files = os.listdir(DIRECTORY_TEST)
        print(Panel.fit(LOAD_START, box=box.DOUBLE))
        name = input(">> ").lower()

        # Normalizing search key
        search_key = "_".join(name.split())
        matches = []
        for char in char_files:
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


def display_character_card(char_data):
    panel_style = f"{char_data['card_color']}"
    left = [
        f'Name: {char_data["first_name"]} {char_data["middle_name"]} {char_data["last_name"]}',
        f'Title: {char_data["title"]}',
        f'Role: {char_data["role"]}',
        f'Race: {char_data["race"]}',
        f'Hair: {char_data["hair"]}',
    ]

    right = [
        f'Gender: {char_data["gender"]}',
        f'Style: {char_data["card_color"]}',
        f'World: {char_data["world"]}',
        f'Skin: {char_data["skin"]}',
        f'Eye: {char_data["eye"]}',
    ]
    
    lines = []
    for l, r in zip(left, right):
        lines.append(f"{l:<30} {r}")
    tags_str = ", ".join(char_data["tags"])
    lines.append(f"Tags: {tags_str}")
    
    # Previously: LOAD_CARD = yaml.dump(capatalize_keys(char_data), sort_keys=False)
    LOAD_CARD = "\n".join(lines)
    print(
        Panel.fit(
            LOAD_CARD,
            style=panel_style,
            title=f"[{char_data['card_color']}]{char_data['first_name']}'s CHARACTER CARD",
            safe_box=True,
            box=box.DOUBLE,
        )
    )


def plain_list():
    print(Panel.fit(AC_TEXT, title="CHARACTER CREATION PANEL", box=box.DOUBLE))
