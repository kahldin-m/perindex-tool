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

# from rich.padding import Padding


# CONSTANTS
VERSION = 0.1
DEBUG_MODE = 0
DIRECTORY_CHARS = "data/characters"
DIRECTORY_TEST = "data/test"

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
  Welcome to Perindex character archival tool. Type a number
  or action from the list below:

======================================================================
    [1] CREATE Character Card
    [2] LOAD/UPDATE Character Card
    [3] VIEW Character Archive
    [4] LIST Archive Metadata (# of characters, most common world, etc)
    [5] EXIT
"""  # was 63 '-' , 5 text 5 || 5 |

CREATE_START = """
  Type the desired information and press Enter to continue.
  You may edit a card later. The following fields will appear in order:
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
  Type the First or partial name of the character you would like to load.
  You may EDIT a card once loaded. Leave empty to return to Main Menu.
"""

UPDATE_OPTIONS = """
  Enter the NUMBER for the field you wish to edit.
  Enter nothing to go back.
======================================================================
  1. Name               6. Race/Species
  2. Title              7. Skin Color
  3. Gender             8. Hair Color
  4. Class/Role         9. Eye Color
  5. World/Setting      10. Tags
"""

ARCHIVE_START = """
  Enter a sort method below:
  Enter nothing to go back.
  -------------------------------------------------
  1. First Name             6. Race/Species
  2. Last Name              7. Tags
  3. Gender
  4. Class/Role
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


# console = Console()      !! UNUSED / REMOVE this punk !!
# def capatalize_keys(data):
#     new_data = {}
#     for key, value in data.items():
#         new_key = key.replace("_", " ").title()
#         new_data[new_key] = value
#     return new_data


# DEV TOOL FUNCTION (be careful using this, as it overwrites ALL cards)
def update_char_data(char, field, new_data):
    if char not in os.listdir(DIRECTORY_TEST):
        input(f"[bold red]'{char}' not found! Continue...[/]")
        return
    char_path = os.path.join(DIRECTORY_TEST, char)
    char_dict = {}
    with open(char_path, "r") as file:
        char_dict = yaml.safe_load(file)
    with open(char_path, "w") as file:
        char_dict[field] = new_data
        yaml.dump(char_dict, file, sort_keys=False)
    print(f"[bold green]Successfully updated {char} file[/]")


# CLI TOOLS
# -----SAVE FUNCTION-----
def save_character_yaml(char_data, directory, new_char=True):
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

    # Prevent accidental overrites  -- TO DO: Add confirmation of overwrite, OR incrementing name-tag
    if new_char and os.path.exists(full_path):
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
    if "date_created" not in char_data:
        char_data["date_created"] = datetime.now().strftime("%b %d %Y (%H:%M)")
    with open(full_path, "w", encoding="utf-8") as file:
        yaml.dump(char_data, file, sort_keys=False)

    if new_char:
        print(
            f"[bold green]Saved character to archive:[/] '{full_path}'\nOn {char_data.get('date_created', 'Now')}"
        )
    else:
        print(f"[bold green]Updated character at archive:[/] '{full_path}'")
    return True


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
    new_char["first_name"] = input("First name: ").strip()
    new_char["middle_name"] = input("\nMiddle name: ").strip()
    new_char["last_name"] = input("\nLast name: ").strip()
    new_char["title"] = input("\nTitle: ").strip()
    new_char["gender"] = input("\nGender: ").strip()
    new_char["role"] = input("\nClass or role (wizard, acrobat, monk): ").strip()
    new_char["world"] = input("\nWorld or setting the character is from: ").strip()
    new_char["race"] = input("\nRace or species: ").strip()
    new_char["skin"] = input("\nSkin color or tone (peach, dark, purple): ").strip()
    new_char["hair"] = input("\nHair color: ").strip()
    new_char["eye"] = input("\nEye color: ").strip()
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
        hc = get_hourly_color()
        print(
            Panel.fit(CREATE_END, title="[CHARACTER CREATOR]", box=box.DOUBLE, style=hc)
        )
        color_choice = input("Card color: ").strip().lower()
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


# -----UPDATE FUNCTION-----
def update_character_yaml(char_data):
    clear()
    updated_char = deepcopy(char_data)
    updating = True
    while updating:
        hc = get_hourly_color()
        print(
            Panel.fit(UPDATE_OPTIONS, title="[Character Editor]", box=box.DOUBLE, style=hc)
        )
        choice = input(">> ").strip()
        match choice:
            case "1":
                print(f'\n  Current Name: {updated_char.get("first_name", "")} {updated_char.get("middle_name", "")} {updated_char.get("last_name", "")}\n')
                updated_char["first_name"] = input("  New First name: ").strip()
                updated_char["middle_name"] = input("  New Middle name: ").strip()
                updated_char["last_name"] = input("  New Last name: ").strip()
            case "2":
                print(f'\n  Current Title: {updated_char.get("title", "")}\n')
                updated_char["title"] = input("  New Title: ").strip()
            case "3":
                print(f'\n  Current Gender: {updated_char.get("gender", "")}\n')
                updated_char["gender"] = input("  New Gender: ").strip()
            case "4":
                print(f'\n  Current Class/Role: {updated_char.get("role", "")}\n')
                updated_char["role"] = input("  New Class or role (wizard, acrobat, monk): ").strip()
            case "5":
                print(f'\n  Current World/Setting: {updated_char.get("world", "")}\n')
                updated_char["world"] = input("  New World or setting the character is from: ").strip()
            case "6":
                print(f'\n  Current Race: {updated_char.get("race", "")}\n')
                updated_char["race"] = input("  New Race or species: ").strip()
            case "7":
                print(f'\n  Current Skin: {updated_char.get("skin", "")}\n')
                updated_char["skin"] = input("  New Skin color or tone (peach, dark, purple): ").strip()
            case "8":
                print(f'\n  Current Hair: {updated_char.get("hair", "")}\n')
                updated_char["hair"] = input("  New Hair color: ").strip()
            case "9":
                print(f'\n  Current Eye: {updated_char.get("eye", "")}\n')
                updated_char["eye"] = input("  New Eye color: ").strip()
            case "10":  # TAGS stub
                pass
            case _:
                updating = False

    save_character_yaml(updated_char, DIRECTORY_TEST, False)
    return updated_char


# -----YAML VALIDATION-----
def validate_character_yaml(char_data):
    fixed = False
    validated = {}
    
    for key, default in CARD_TEMPLATE.items():
        # Missing data
        if key not in char_data:
            if key == "version":
                validated[key] = VERSION
            elif key == "date_created":
                validated[key] = datetime.now().strftime("%b %d %Y (%H:%M)")
            else:
                validated[key] = default
            fixed = True
            print(f"\n  Updated '{key}' field")
        else:
            value = char_data[key]
            if key == "version":
                if char_data["version"] != VERSION:
                    validated[key] = VERSION
                    fixed = True
            elif key == "tags" and not isinstance(value, list):
                validated[key] = []
                fixed = True
                print(f"\n  Updated '{key}' field")
            else:
                validated[key] = value

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
        for char in os.listdir(DIRECTORY_TEST):
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
                print(f"\n>> Please enter a number")
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
    card_path = os.path.join(DIRECTORY_TEST, file_path)
    with open(card_path, "r") as file:
        char_card = yaml.safe_load(file)
        if not isinstance(char_card, dict):
            print(f"  [bold red]YAML file is invalid or empty.[/]")
            return None
        validated, fixed = validate_character_yaml(char_card)
        
        if fixed:
            print(f"\n  [bold green]Validated missing data field(s) for: {file_path}[/]\n")
            with open(card_path, "w", encoding="utf-8") as file:
                yaml.dump(validated, file, sort_keys=False)
                
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

    # lines = []    # OLD LINES BUILDING
    # for lefto, righto in zip(left, right):
    #     lines.append(f"{lefto:<30} {righto}")
    # lines.append(f"Created: {char_data.get('date_created', 'The day after tomorrow\'s yesterday')}")
    # tags_str = ", ".join(char_data.get("tags", ""))
    # lines.append(f"Tags: {tags_str}")

    # Previously: LOAD_CARD = yaml.dump(capatalize_keys(char_data), sort_keys=False)
    # LOAD_CARD = "\n".join(lines)
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
    print("  [bold white]Update character card?  yes/No[/]")
    choice = input(">> ").strip()
    if choice in {"y", "ye", "yes", "yep", "oui"}:
        new_data = update_character_yaml(char_data)
        if new_data:
            char_data = new_data
        

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


# -----SORT LOGIC-----
def archive_sort_cards(sort_type):
    cards = []
    for f in os.listdir(DIRECTORY_TEST):
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
            sorted_cards = sorted(
                cards, key=lambda c: ", ".join(tag.lower() for tag in c.get("tags", []))
            )
            display = [build_display(c, "tags") for c in sorted_cards]
            archive_display_cards(display)
        case "":
            return
        case _:
            print("Invalid sort type/out of option range (1-10)")
            archive_select_mode()
    input("\n>> ")

# -----SORT DISPLAY-----
def archive_select_mode():
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
        


# -----OVERVIEW HELPERS-----
def overview_helper_counter(field):
    result = 0
    for f in os.listdir(DIRECTORY_TEST):
        with open(os.path.join(DIRECTORY_TEST, f), "r") as file:
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
    for f in os.listdir(DIRECTORY_TEST):
        with open(os.path.join(DIRECTORY_TEST, f), "r") as file:
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


# A counter → total characters
# A list → all tags
# A set → unique tags
# A dict → counts per world
# A dict → counts per race
# A dict → counts per role
# A list → creation dates (if you want earliest/latest)


# -----BUILD ARCHIVE DATA-----
def overview_display():
    hc = get_hourly_color()
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
        f"Total Characters: {len(os.listdir(DIRECTORY_TEST))}",
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
        lines.append(f"  {lefto:<34} {righto}")
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

# -----DEV TOOL HELPER-----
def dev_helper(field, data):
    confirmation = (
        input(
            f"Are you sure you wish to update the '{field}' of all cards to '{data}' ?  yes/no\n>>  "
        )
        .strip()
        .lower()
    )
    if confirmation in {"y", "ye", "yes"}:
        for f in os.listdir(DIRECTORY_TEST):
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
    
    for filename in os.listdir(DIRECTORY_TEST):
        path = os.path.join(DIRECTORY_TEST, filename)
        
        # FILENAME CLEANING
        clean_name = sanitize_filename(filename)
        if clean_name != filename:
            new = os.path.join(DIRECTORY_TEST, clean_name)
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

