# core.py
# IMPORTS
# from rich.console import Console # 14.3.3
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich import print
import yaml
import os

# CONSTANTS
DEBUG_MODE = 0
DIRECTORY_TEST = "data/test"

CC_NAME = """
  Follow the prompts below to complete the character creation process.
  The following fields will appear in order:
======================================================================
  1. Name               6. Race/Species
  2. Title              7. Skin Color
  3. Gender             8. Hair Color
  4. Class/Role         9. Eye Color
  5. World/Setting      10. Tags
"""

LC_TEXT = "[bold green]CHARACTER DATA:[/]\nName: _Testificate\nRole: Samurai\nWorld: [bold blue]WoW[/]\ntags:\n - warrior\n - [bold green]elf[/]\n - [bold magenta]*[/]swordsman\n"
 
AC_TEXT = """
[black on red]_Testificate[/]
[black on yellow]Alex[/]
[black on green]Baron[/]
[black on blue]Charlie[/]
[black on magenta]Vecna[/]
"""

# UTILS
# console = Console()

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
        print(f"\n[red]File '{file_name}' already exists. Creating incremented character.[/]")
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
        "eyes": "",
        "tags": [],
    }
    print(Panel.fit(CC_NAME, title="CHARACTER CREATOR", box=box.DOUBLE))
    new_char["first_name"] = input("First name: ")
    new_char["middle_name"] = input("Middle name: ")
    new_char["last_name"] = input("Last name: ")
    new_char["gender"] = input("Gender: ")
    new_char["role"] = input("Class or role (wizard, acrobat, monk): ")
    new_char["world"] = input("World or setting the character is from: ")
    new_char["race"] = input("Race or species: ")
    new_char["skin"] = input("Skin color or tone (peach, dark, purple): ")
    new_char["hair"] = input("Hair color: ")
    new_char["eyes"] = input("Eye color: ")
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
    save_character_yaml(new_char, DIRECTORY_TEST)

def load_character():
    # Test example attributes of character from stored card, not used in LC_TEXT
    name = "_Testificate"
    char_color = "magenta"
    world = "WoW"
    tags = ["warrior", "elf", "swordsman"]
    print(Panel.fit(LC_TEXT, title=f"[{char_color}]{name}'s CHARACTER CARD", box=box.DOUBLE))


def plain_list():
    print(Panel.fit(AC_TEXT, title="CHARACTER CREATION PANEL", box=box.DOUBLE))