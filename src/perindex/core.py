# core.py
# IMPORTS
# from rich.console import Console # 14.3.3
import math
import os
import shutil
from copy import deepcopy
from datetime import datetime

import yaml
from rich import box, print
from rich.panel import Panel
from rich.table import Table


# CONSTANTS
VERSION = 1.0
DEBUG_MODE = 0
DIRECTORY_CHARS = "data/characters"
# DIRECTORY_TEST = "data/test"  # Dev test character folder
os.makedirs(DIRECTORY_CHARS, exist_ok=True)

CARD_TEMPLATE = {
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
        "date_created": "",
    }

WELCOME_TEXT = """
  Welcome to the Perindex character archival tool.
  Enter a number or command from the list below:
======================================================================
    [1] CREATE Character Card
    [2] LOAD/EDIT Character Card
    [3] VIEW Character Archive
    [4] LIST Archive Stats (# of characters, most common world, etc)
    [5] EXIT
"""  # was 63 '-' , 5 text 5 || 5 |

CREATE_START = """
  Type the desired information and press Enter to continue.
  You may edit a card later. The following fields will appear in order:
======================================================================
  1. Name               6. Race/Species     11. Card Color
  2. Title              7. Skin Color
  3. Gender             8. Hair Color
  4. Class/Role         9. Eye Color
  5. World/Setting      10. Tags
"""

CREATE_END = """
  Enter the name of a color from the list below that you would like
  to set as the Card Color for this character.
  Brighter colors are available by adding 'bold' before the color name.
  Examples: [yellow]yellow[/], [bold yellow]bold yellow[/], [blue]blue[/], etc
======================================================================
  - [red]Red[/] ([bold red]bold[/])           - [magenta]Magenta[/] ([bold magenta]bold[/])
  - [yellow]Yellow[/] ([bold yellow]bold[/])        - [white]White[/] ([bold white]bold[/]) (default)
  - [green]Green[/] ([bold green]bold[/])         - [black on white]Black[/] ([bold black on white]bold[/])
  - [cyan]Cyan[/] ([bold cyan]bold[/])
  - [blue]Blue[/] ([bold blue]bold[/])
"""

AVAILABLE_COLORS = [
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
]

# 9AM - 2PM BOLD
WELCOME_COLORS = [
    "red",
    "yellow",
    "green",
    "cyan",
    "blue",
    "magenta",
    "red",
    "yellow",
    "green",
    "bold cyan",
    "bold blue",
    "bold magenta",
    "bold red",
    "bold yellow",
    "bold green",
    "cyan",
    "blue",
    "magenta",
    "red",
    "yellow",
    "green",
    "cyan",
    "blue",
    "magenta",
]

LOAD_START = """
  Enter the First or partial name of the character you would like to LOAD.
  You may EDIT a card once loaded. Enter nothing to return to the Main Menu.
"""

UPDATE_OPTIONS = """
  Enter the NUMBER for the field you wish to edit.
  Enter nothing to go back.
======================================================================
  1. Name               6. Race/Species     11. Card Color
  2. Title              7. Skin Color       12. Delete Character
  3. Gender             8. Hair Color
  4. Class/Role         9. Eye Color
  5. World/Setting      10. Tags
"""

ARCHIVE_START = """
  Enter the NUMBER for the sorting method you wish to use.
  Enter nothing to return to the Main Menu.
  -------------------------------------------------
  Sort by:
  1. First Name             6. Race/Species
  2. Last Name              7. Tags
  3. Gender                 8. Card Color
  4. Class/Role             9. Date Created
  5. World/Setting
"""

DEV_TOOL_TEXT = """
  Edit which field?
======================================================================
  1. Version
  2. BACK
"""

# UTILS
def get_hourly_color():
    hour_24 = datetime.now().hour  # % 12) or 12
    # idx = hour_12 % 12
    return WELCOME_COLORS[hour_24]
    
def dbm_return():
    print("[bold red]\n  ERROR: DEV TOOL COMMANDS CURRENTLY DISABLED")
    return

# Clean up the terminal space
def clear():
    os.system("cls" if os.name == "nt" else "clear")


# DEV TOOL FUNCTION (be careful using this, as it overwrites ALL cards)
def update_char_data(char, field, new_data):
    if char not in os.listdir(DIRECTORY_CHARS):
        input(f"[bold red]'{char}' not found! Continue...[/]")
        return
    char_path = os.path.join(DIRECTORY_CHARS, char)
    char_dict = {}
    with open(char_path, "r") as file:
        char_dict = yaml.safe_load(file)
    with open(char_path, "w") as file:
        char_dict[field] = new_data
        yaml.dump(char_dict, file, sort_keys=False)
    print(f"[bold green]Successfully updated {char} file[/]")

# ==================================================
# 
# 
# 
# 
# CLI TOOLS
# -----SOLUTION FOR DOPPELGANGERS-----
def doppelganger(first, last, directory):
    base_fname = first.strip().replace(" ", "_").lower()
    base_lname = last.strip().replace(" ", "_").lower()
    
    if base_lname:
        base = f"{base_fname}_{base_lname}"
    else:
        base = base_fname
    
    # Try base.yaml, then base_01.yaml, base_02.yaml, etc...
    filename = f"{base}.yaml"
    path = os.path.join(directory, filename)
    if not os.path.exists(path):
        return filename
        
    # Increment until we find a free slot
    counter = 1
    while True:
        filename = f"{base}_{counter:02}.yaml"
        path = os.path.join(directory, filename)
        if not os.path.exists(path):
            return filename
        counter += 1
    
# -----SAVE FUNCTION-----
def save_character_yaml(char_data, directory, new_char=True, old_file=None):
    # Normalize name
    safe_fname = char_data["first_name"].strip().replace(" ", "_").lower()
    safe_lname = char_data["last_name"].strip().replace(" ", "_").lower()
    
    # Build the base filename
    if safe_lname:
        base_file = f"{safe_fname}_{safe_lname}.yaml"
    else:
        base_file = f"{safe_fname}.yaml"

    # Prevent accidental overrites with incrementation
    if new_char:
        # Character is new , always check for duplicates
        if os.path.exists(os.path.join(directory, base_file)):
            print(f"\n  [red]A file with this name already exists: '{base_file}'\n  Dealing with the new doppelganger! (incrementing filename)[/]")
        file_name = doppelganger(char_data["first_name"], char_data["last_name"], directory)
    elif old_file and old_file != base_file:
        # Name changed , ensure uniqueness
        if os.path.exists(os.path.join(directory, base_file)):
            print(f"\n  [red]A file with this name already exists: '{base_file}'\n  Dealing with the new doppelganger![/] (incrementing filename)")
        file_name = doppelganger(char_data["first_name"], char_data["last_name"], directory)
    else:
        # Name did NOT change , keep same filename
        file_name = base_file
    full_path = os.path.join(directory, file_name)

    # Write YAML character card and ensure date_created exists
    if DEBUG_MODE:
        print(f"  [yellow]DEBUG absolute path: {os.path.abspath(full_path)}[/]")
    if not char_data.get("date_created"):
        char_data["date_created"] = datetime.now().strftime("%b %d %Y (%H:%M)")
    with open(full_path, "w", encoding="utf-8") as file:
        yaml.dump(char_data, file, sort_keys=False)

    # ----Delete old file if renaming-----
    if old_file and old_file != file_name:
        old_path = os.path.join(directory, old_file)
        if os.path.exists(old_path):
            try:
                os.remove(old_path)
                print(f"  [yellow]Removed old character file:[/] {old_file}")
            except OSError as e:
                print(f"  [bold red]Failed to delete old file:[/]  {e}")

    if new_char:
        print(f"  [green]Saved character to archive:[/] '{full_path}'\n  On {char_data.get('date_created', 'Now')}")
    else:
        print(f"  [green]Updated character at archive:[/] '{full_path}'")

    return file_name


# -----CARD COLOR PICKER-----
def card_color_picker(current_color="white"):
    color_picking = True
    chosen = current_color
    
    while color_picking:
        clear()
        hc = get_hourly_color()
        print(Panel.fit(CREATE_END, title="[CHARACTER CREATOR]", box=box.DOUBLE, style=hc))
        
        color_choice = input("  Card color: ").strip().lower()
        
        if color_choice in AVAILABLE_COLORS:
            if color_choice == "black":
                chosen = "black on white"
            elif color_choice == "bold black":
                chosen = "bold black on white"
            else:
                chosen = color_choice
            color_picking = False

        elif color_choice == "":
            chosen = "white"
            color_picking = False

        else:
            print(f"\n  '{color_choice}' is an invalid option")
            input("  Press Enter to continue...")
    
    return chosen
    
# -----TAG EDITOR-----
def tag_editor(existing_tags):
    tags = existing_tags[:]  # Copying to avoid original mutating :(
    
    print("[green]  Enter a tag name to add it.[/]")
    print("[green]  Enter a tag name prefixed with a minus to remove the tag\n  for example, enter -tall to remove tall.[/]")
    print("[green]  Press Enter with no text to finish.\n[/]")
    
    while True:
        t = input("  Tag editor: ").strip()
        if t == "":
            break
        # REMOVE TAG
        if t.startswith("-"):
            tag_to_remove = t[1:].strip()
            if tag_to_remove in tags:
                tags.remove(tag_to_remove)
                print(f"  Remove tag: {tag_to_remove}\n")
            else:
                print(f"  '{tag_to_remove}' not found\n")
            continue
        # ADD TAG
        if t not in tags:
            tags.append(t)
            print(f"  Added tag: {t}\n")
        else:
            print(f"  Tag '{t}' already exists\n")
            
    return tags

# -----CREATE FUNCTION-----
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
        "date_created": "",
    }
    hc = get_hourly_color()
    print(
        Panel.fit(CREATE_START, title="[CHARACTER CREATOR]", box=box.DOUBLE, style=hc)
    )
    new_char["first_name"] = input("  First name: ").strip()
    new_char["middle_name"] = input("\n  Middle name: ").strip()
    new_char["last_name"] = input("\n  Last name: ").strip()
    new_char["title"] = input("\n  Title: ").strip()
    new_char["gender"] = input("\n  Gender: ").strip()
    new_char["role"] = input("\n  Class or role (wizard, acrobat, monk): ").strip()
    new_char["world"] = input("\n  World or setting the character is from: ").strip()
    new_char["race"] = input("\n  Race or species: ").strip()
    new_char["skin"] = input("\n  Skin color or tone (peach, dark, purple): ").strip()
    new_char["hair"] = input("\n  Hair color: ").strip()
    new_char["eye"] = input("\n  Eye color: ").strip()
    print("""\n  Add and remove tags here. Tags act as short notes and extra descriptors.
  Example tags: tall, chef, evil, eyepatch, robot arm, mute
""")
    new_char["tags"] = tag_editor([])
    new_char["card_color"] = card_color_picker()

    new_fname = save_character_yaml(new_char, DIRECTORY_CHARS)
    new_char["_file_name"] = new_fname

# ==================================================
# 
# 
# 
# 
# -----UPDATE FUNCTION-----
def update_character_yaml(char_data):
    old_file = char_data.get("_file_name")

    clear()
    updated_char = deepcopy(char_data)
    updating = True

    while updating:
        hc = get_hourly_color()
        print(Panel.fit(UPDATE_OPTIONS, title="[Character Editor]", box=box.DOUBLE, style=hc))
        choice = input(">> ").strip()
        
        match choice:
            case "1":
                name_parts = [
                    updated_char.get("first_name", "").strip(),
                    updated_char.get("middle_name", "").strip(),
                    updated_char.get("last_name", "").strip(),
                ]
                ould_name = " ".join(p for p in name_parts if p)
                print(f'\n  Old Name: {ould_name}\n')
                updated_char["first_name"] = input("  New First name: ").strip()
                updated_char["middle_name"] = input("  New Middle name: ").strip()
                updated_char["last_name"] = input("  New Last name: ").strip()
            case "2":
                print(f'\n  Old Title: {updated_char.get("title", "")}\n')
                updated_char["title"] = input("  New Title: ").strip()
            case "3":
                print(f'\n  Old Gender: {updated_char.get("gender", "")}\n')
                updated_char["gender"] = input("  New Gender: ").strip()
            case "4":
                print(f'\n  Old Class/Role: {updated_char.get("role", "")}\n')
                updated_char["role"] = input("  New Class/Role (wizard, acrobat, monk): ").strip()
            case "5":
                print(f'\n  Old World/Setting: {updated_char.get("world", "")}\n')
                updated_char["world"] = input("  New World/Setting: ").strip()
            case "6":
                print(f'\n  Old Race: {updated_char.get("race", "")}\n')
                updated_char["race"] = input("  New Race/Species: ").strip()
            case "7":
                print(f'\n  Old Skin: {updated_char.get("skin", "")}\n')
                updated_char["skin"] = input("  New Skin color/tone: ").strip()
            case "8":
                print(f'\n  Old Hair: {updated_char.get("hair", "")}\n')
                updated_char["hair"] = input("  New Hair color: ").strip()
            case "9":
                print(f'\n  Old Eye: {updated_char.get("eye", "")}\n')
                updated_char["eye"] = input("  New Eye color: ").strip()
            case "10":
                print(f"  Old tags: {', '.join(updated_char.get('tags', [])) or 'None'}\n")
                updated_char["tags"] = tag_editor(updated_char.get("tags", []))
            case "11":
                print(f"  Old Card Color: {updated_char.get('card_color', 'white')}")
                updated_char["card_color"] = card_color_picker(updated_char.get("card_color", "white"))
            case "12":
                print("  --- [bold red]Are you sure you wish to delete this character? Type DELETE to confirm.[/] ---")
                confirmation = input(">> ").strip().upper()
                if confirmation == "DELETE":
                    try:
                        os.remove(os.path.join(DIRECTORY_CHARS, old_file))
                        print(f"  [bold red]Character deleted:[/] {old_file}")
                    except OSError as e:
                        print(f"  [bold red]Failed to delete character file:[/] {e}")
                    # Exit the editor immediately. Nothing left to save :(
                    return None
                else:
                    print("  [yellow]Delete cancelled.\n")
            case "":
                updating = False
            case _:
                print("  Invalid option. Please enter a valid number (1-12)\n")

    if updated_char is None:
        return None
    clear()
    new_fname = save_character_yaml(updated_char, DIRECTORY_CHARS, False, old_file)
    if new_fname:
        updated_char["_file_name"] = new_fname
        
    return updated_char


# -----YAML VALIDATION-----
def validate_character_yaml(char_data):
    fixed = False
    validated = dict(char_data)
    
    for key, default in CARD_TEMPLATE.items():
        # Missing data
        if key not in validated:
            if key == "version":
                validated[key] = VERSION
            elif key == "date_created":
                validated[key] = datetime.now().strftime("%b %d %Y (%H:%M)")
            else:
                validated[key] = default
            fixed = True
            print(f"\n  Updated '{key}' field")
        else:
            value = validated[key]
            if key == "version":
                if value != VERSION:
                    validated[key] = VERSION
                    fixed = True
            elif key == "tags" and not isinstance(value, list):
                validated[key] = []
                fixed = True
                print(f"\n  Updated '{key}' field")
            elif key == "date_created" and not value:
                validated[key] = datetime.now().strftime("%b %d %Y (%H:%M)")
                fixed = True
                print(f"\n  Updated '{key}' field")
            # Otherwise keep validated key as-is

    return validated, fixed

# -----LOAD FUNCTION-----
def load_character_yaml():
    searching = True
    file_path = ""

    while searching:
        hc = get_hourly_color()
        print(
            Panel.fit(LOAD_START, title="[Character Loader]", box=box.DOUBLE, style=hc)
        )
        name = input(">> ").strip().lower()
        if name.strip() == "":
            break

        # Normalizing search key
        search_key = "_".join(name.split())
        matches = []
        for char in os.listdir(DIRECTORY_CHARS):
            lower_name = char.lower()
            if search_key in lower_name:
                matches.append(char)

        if len(matches) == 0:
            clear()
            print(f"\n>>  No matches found for '{name}'")
            continue

        if len(matches) == 1:
            file_path = matches[0]
            clear()
            print(f"\n  Match found for '{name}': {file_path}")
            # input("\n>> Press Enter to continue...")
            searching = False
            continue

        if len(matches) > 1:
            clear()
            print(f"\n  Multiple matches found for '{name}'")
            for i, f in enumerate(matches, 1):
                print(f"    {i}. {f}")
            idx = input("\nEnter a character by number: ").strip()
            if not idx.isdigit():
                clear()
                print("\n>> Please enter a number")
                continue

            selection = int(idx)
            if selection < 1 or selection > len(matches):
                clear()
                print(f"\n>> That number is out of range: (1-{len(matches)})")
                continue

            # Valid selection
            file_path = matches[selection - 1]
            print(f"\n  Loading character card: ({file_path})")
            searching = False

    if file_path.strip() == "":
        return None
        
    # Load YAML
    card_path = os.path.join(DIRECTORY_CHARS, file_path)
    with open(card_path, "r") as file:
        char_card = yaml.safe_load(file)
        if not isinstance(char_card, dict):
            print("  [bold red]YAML file is invalid or empty.[/]")
            return None
        validated, fixed = validate_character_yaml(char_card)
        
        if fixed:
            print(f"\n  [green]Validated missing data field(s) for: {file_path}[/]\n")
            with open(card_path, "w", encoding="utf-8") as file:
                yaml.dump(validated, file, sort_keys=False)
        # Attaching the real filename so update/save can use it... no more accidental deletions
        validated["_file_name"] = file_path
        
        return validated


# -----DISPLAY FUNCTION-----
def display_character_card(char_data):
    panel_style = f"{char_data['card_color']}"
    name_parts = [
        char_data.get("first_name", ""),
        char_data.get("middle_name", ""),
        char_data.get("last_name", ""),
    ]
    name_full = " ".join(p for p in name_parts if p)
    left = [
        f"Name: {name_full}",
        f"Title: {char_data.get('title')}",
        f"Role: {char_data.get('role')}",
        f"Race: {char_data.get('race')}",
        f"Hair: {char_data.get('hair')}",
    ]

    right = [
        f"Gender: {char_data.get('gender')}",
        f"Style: {char_data.get('card_color')}",
        f"World: {char_data.get('world')}",
        f"Skin: {char_data.get('skin')}",
        f"Eye: {char_data.get('eye')}",
    ]

    display_t = Table.grid(padding=(0, 4))
    display_t.add_column(no_wrap=True)
    display_t.add_column()

    for lefto, righto in zip(left, right):
        display_t.add_row(lefto, righto)

    display_t.add_row(
        f"Created on:{' .' * 8}",
        char_data.get("date_created", "The day after tomorrow's yesterday"),
    )
    tags_str = ", ".join(char_data.get("tags", []))
    display_t.add_row(f"Tags:{' .' * 11}", tags_str)


    print(
        Panel(
            display_t,
            style=panel_style,
            title=f"[[{char_data.get('card_color', 'white')}]{char_data['first_name']}'s Character Card (v{char_data.get('version', '??')})]",
            safe_box=True,
            box=box.DOUBLE,
            width=72,
        )
    )
    print("  [bold white]Update character card?  1. Yes | 2. No[/]")
    choice = input(">> ").strip()
    if choice in {"1", "y", "ye", "yes", "yep", "oui"}:
        new_data = update_character_yaml(char_data)
        if new_data:
            char_data = new_data
        
# ==================================================
# 
# 
# 
# 
# -----ARCHIVE HELPER-----
def build_display(card, attr_name):
    # Build base name
    fn = card.get("first_name", "")
    ln = card.get("last_name", "")
    if fn and ln:
        base_name = f"{fn} {ln}"
    else:
        base_name = fn or ln or "Unknown"

    # NAME SORT MODES
    if attr_name == "first_name":
        return base_name
    elif attr_name == "last_name":
        if ln and fn:
            return f"{fn} ({ln})"
        if ln:
            return ln
        return fn

    # DATE SORT MODE
    if attr_name == "date_created":
        date_str = card.get("date_created", "Unknown date")
        return f"{base_name} ({date_str})"

    # ATTRBUTE SORT MODE
    # Take an attribute: "gender", "world", "role" etc.
    attr_value = card.get(f"{attr_name}", "")
    if isinstance(attr_value, list):
        attr_value = ", ".join(tag.lower() for tag in attr_value)
    attr_part = f"({attr_value})" if attr_value else ""

    return f"{base_name} {attr_part}".strip()


# -----ARCHIVE DISPLAY-----
def archive_display_cards(cards):
    height = shutil.get_terminal_size().lines
    twidth = shutil.get_terminal_size().columns
    wresize = 72 if twidth > 72 else twidth
    usable = height - 6  # Adjusting for panel borders, title, padding

    # Using a paging loop to ensure readability if the archive is bigger than 10 cards
    current_page = 1
    total_cards = len(cards)  # Actually total_cards ...
    total_pages = max(1, math.ceil(total_cards / usable))
    index = 0

    while index < total_cards:
        page = cards[index : index + usable]
        clear()
        hc = get_hourly_color()
        print(
            Panel(
                "\n".join(page),
                title=f"[Page {current_page}/{total_pages}]",
                box=box.DOUBLE,
                width=wresize,
                padding=1,
                style=hc,
            )
        )
        index += usable
        current_page += 1
        if index < total_cards:
            input("\nPress Enter to go to next page >>")


# -----DATE CREATED PARSER-----
def parse_by_dates(card):
    raw = card.get("date_created", "")
    try:
        return datetime.strptime(raw, "%b %d %Y (%H:%M)")
    except Exception:
        # If somehow invalid... just push it to the bottom
        return datetime.min

# -----SORT LOGIC-----
def archive_sort_cards(sort_type):
    cards = []
    for f in os.listdir(DIRECTORY_CHARS):
        with open(os.path.join(DIRECTORY_CHARS, f), "r") as file:
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
            sorted_cards = sorted(cards, key=lambda c: (c.get("last_name", ""), c.get("first_name", "")))
            display = [build_display(c, "last_name") for c in sorted_cards]
            archive_display_cards(display)
        case "3":
            print("[red]OPTION 3: Gender[/]")
            sorted_cards = sorted(cards, key=lambda c: (c.get("gender", ""), c.get("first_name", "")))
            display = [build_display(c, "gender") for c in sorted_cards]
            archive_display_cards(display)
        case "4":
            print("[green]OPTION 4: Role[/]")
            sorted_cards = sorted(cards, key=lambda c: (c.get("role", ""), c.get("first_name", "")))
            display = [build_display(c, "role") for c in sorted_cards]
            archive_display_cards(display)
        case "5":
            print("[blue]OPTION 5: World[/]")
            sorted_cards = sorted(cards, key=lambda c: (c.get("world", ""), c.get("first_name", "")))
            display = [build_display(c, "world") for c in sorted_cards]
            archive_display_cards(display)
        case "6":
            print("[red]OPTION 6: Race[/]")
            sorted_cards = sorted(cards, key=lambda c: (c.get("race", ""), c.get("first_name", "")))
            display = [build_display(c, "race") for c in sorted_cards]
            archive_display_cards(display)
        case "7":
            print("[green]OPTION 7: Tags[/]")
            sorted_cards = sorted(
                cards, key=lambda c: ", ".join(tag.lower() for tag in c.get("tags", []))
            )
            display = [build_display(c, "tags") for c in sorted_cards]
            archive_display_cards(display)
        case "8":
            print("[white]OPTION 8: Card Colors[/]")
            sorted_cards = sorted(cards, key=lambda c: (c.get("card_color", ""), c.get("first_name", "")))
            display = [build_display(c, "card_color") for c in sorted_cards]
            archive_display_cards(display)
        case "9":
            print("[white]OPTION 9: Date Created[/]")
            sorted_cards = sorted(cards, key=lambda c: (parse_by_dates(c), c.get("first_name", "")))
            display = [build_display(c, "date_created") for c in sorted_cards]
            archive_display_cards(display)
        case "":
            return
        case _:
            print("Invalid sort type/out of option range (1-10)")
            archive_select_mode()
    input("\n>> ")

# -----SORT DISPLAY-----
def archive_select_mode():
    # Safety if the character archive is EMPTY
    if not os.listdir(DIRECTORY_CHARS):
        hc = get_hourly_color()
        print(
            Panel(
                "Gasp! There are currently no characters in the archive!\n"
                "Come back after you've created a few character cards.",
                title="[Archive Overview]",
                box=box.DOUBLE,
                style=hc,
                width=72,
            )
        )
        input(">> ")
        return
    viewing = True
    while viewing:
        hc = get_hourly_color()
        print(Panel.fit(ARCHIVE_START, box=box.DOUBLE, style=hc))
        choice = input("Sort type number:  ").strip()
        if choice == "":
            viewing = False
            clear()
            break
        clear()
        archive_sort_cards(choice)
        clear()
        
# ==================================================
# 
# 
# 
# 
# -----OVERVIEW HELPERS-----
def overview_helper_counter(field):
    result = 0
    for f in os.listdir(DIRECTORY_CHARS):
        with open(os.path.join(DIRECTORY_CHARS, f), "r") as file:
            char_data = yaml.safe_load(file)
            if field != "tags":
                if char_data.get(field):
                    result += 1
            else:
                if char_data.get(field):
                    result += len(char_data.get("tags", []))
    return result


def overview_helper_dict(field):
    result = {}
    for f in os.listdir(DIRECTORY_CHARS):
        with open(os.path.join(DIRECTORY_CHARS, f), "r") as file:
            char_data = yaml.safe_load(file)
            value = char_data.get(field)
            if not value:
                continue

            match field:
                case "gender":
                    v = value.strip().lower()
                    if v.startswith("m"):
                        key = "Male"
                    elif v.startswith("f"):
                        key = "Female"
                    else:
                        key = "Other"
                    result[key] = result.get(key, 0) + 1

                case "first_name":
                    v = value[0].strip().upper()
                    result[v] = result.get(v, 0) + 1

                case "tags":
                    for tag in value or []:
                        result[tag] = result.get(tag, 0) + 1
                case _:
                    result[value] = result.get(value, 0) + 1

    return result


def overview_helper_common(dict):
    total = 0
    counter = 0
    common = ""
    for d in dict:
        total += 1
        if dict[d] > counter:
            counter = dict[d]
            common = d
    return total, common


# -----BUILD ARCHIVE DATA-----
def overview_display():
    hc = get_hourly_color()
    # Safety if the character archive is EMPTY
    if not os.listdir(DIRECTORY_CHARS):
        print(
            Panel(
                "Gasp! There are currently no characters in the archive!\n"
                "Go create a few character cards, then come back for some fun stats!",
                title="[Archive Overview]",
                box=box.DOUBLE,
                style=hc,
                width=72,
            )
        )
        input(">> ")
        return
    count_tags = overview_helper_dict("tags")
    count_letters = overview_helper_dict("first_name")
    count_worlds = overview_helper_dict("world")
    count_races = overview_helper_dict("race")
    count_roles = overview_helper_dict("role")
    count_genders = overview_helper_dict("gender")
    total_tags, common_tag = overview_helper_common(count_tags)
    _, common_letter = overview_helper_common(count_letters)
    total_worlds, common_world = overview_helper_common(count_worlds)
    total_races, common_race = overview_helper_common(count_races)
    total_roles, common_role = overview_helper_common(count_roles)

    left = [
        f"Total Characters: {len(os.listdir(DIRECTORY_CHARS))}",
        f"Total Worlds: {total_worlds}",
        f"Total Races: {total_races}",
        f"Total Roles: {total_roles}",
        f"Total Unique Tags: {total_tags}",
    ]

    right = [
        f"Most Common First Initial: {common_letter}",
        f"Most Common World: {common_world}",
        f"Most Common Race: {common_race}({count_races[common_race]})",
        f"Most Common Role: {common_role}({count_roles[common_role]})",
        f"Most Common Tag: {common_tag}({count_tags[common_tag]})",
    ]

    lines = []
    for lefto, righto in zip(left, right):
        lines.append(f"  {lefto:<28} {righto}")
    lines.append(f"  {'Characters per World:':<34} {'Gender Split:'}")
    lines_worlds = []
    for world in count_worlds:
        lines_worlds.append(f"    - {world}: {count_worlds[world]}")
    lines_genders = []
    for gen in count_genders:
        lines_genders.append(f"    - {gen}: {count_genders[gen]}")

    # HANDLE UNORDERED LISTS
    max_len = max(len(lines_worlds), len(lines_genders))
    for i in range(max_len):
        # Worlds column
        world = lines_worlds[i] if i < len(lines_worlds) else ""
        # Genders column
        gender = lines_genders[i] if i < len(lines_genders) else ""
        # Mash em together...
        lines.append(f"  {world:<34} {gender}")

    # Previously: LOAD_CARD = yaml.dump(capatalize_keys(char_data), sort_keys=False)
    LOAD_CARD = "\n".join(lines)
    print(
        Panel(
            LOAD_CARD,
            title="[Archive Overview]",
            safe_box=True,
            box=box.DOUBLE,
            width=72,
            style=hc,
        )
    )
    input(">> ")

# ==================================================
# 
# 
# 
# 
# -----DEV TOOL HELPER-----
def dev_helper(field, data):
    confirmation = input(f"Are you sure you wish to update the '{field}' of all cards to '{data}' ?  yes/No\n>>  ").strip().lower()
    if confirmation in {"y", "ye", "yes"}:
        for f in os.listdir(DIRECTORY_CHARS):
            print(f"Replacing {f}'s {field} data with {data}")
            # Load character cards and overwrite their data in the field
            update_char_data(f, field, data)
    else:
        return


# -----DEV UPDATER TOOL-----
def dev_tool():
    if not DEBUG_MODE:
        dbm_return()
    print(
        Panel.fit(DEV_TOOL_TEXT, title="[DEV TOOL]", box=box.ASCII, style="bold yellow")
    )
    d_field = input(">> ")

    match d_field:
        case "1":
            d_data = input("Replace data with what: ").lower().strip()
            dev_helper("version", d_data)
        case _:
            print("Invalid field selection!")


# CLEAN FILENAME HELPER
def sanitize_filename(text):
    # Remove bad unicode characters
    return text.replace("\uDCD0", "").replace("\uDCD1", "").replace("\uFFFD", "")
    
# -----DEV CLEAN YAMLS-----
def clean_yamls():
    if not DEBUG_MODE:
        dbm_return()
    
    for filename in os.listdir(DIRECTORY_CHARS):
        path = os.path.join(DIRECTORY_CHARS, filename)
        
        # FILENAME CLEANING
        clean_name = sanitize_filename(filename)
        if clean_name != filename:
            new = os.path.join(DIRECTORY_CHARS, clean_name)
            os.rename(path, new)
            print(f"  [bold yellow]Renamed: {filename} -> {clean_name}")
            path = new

        # YAML CONTENT CLEANING
        with open(path, "r", encoding="utf-8") as file:
            data = yaml.safe_load(file)
        
        changed = False # Track if anything changed
        
        for key, value in data.items():
            # Clean strings of the annoying emoji code...
            if isinstance(value, str):
                cleaned = value.replace("\uDCD0", "").replace("\uDCD1", "").replace("\uFFFD", "")
                if cleaned != value:
                    data[key] = cleaned
                    changed = True

            # And list items if they're strings
            elif isinstance(value, list):
                new_list = []
                for item in value:
                    if isinstance(item, str):
                        cleaned_item = item.replace("\uDCD0", "").replace("\uDCD1", "").replace("\uFFFD", "")
                        if cleaned_item != item:
                            changed = True
                        new_list.append(cleaned_item)
                    else:
                        new_list.append(item)
                data[key] = new_list
                
        if changed:        
            with open(path, "w", encoding="utf-8") as file:
                yaml.dump(data, file, sort_keys=False)
            print(f"  [bold yellow]Cleaned bad characters in file: {clean_name}")

