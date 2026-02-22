# core.py
# IMPORTS
# from rich.console import Console # 14.3.3
from rich.panel import Panel
from rich.text import Text
from rich import box
from rich import print


# CONSTANTS
CC_TEXT = (
"[red]Character creation in progress...[/]\n"
"[green]Placeholder instructions.[/]\n"
"Placeholder options.\n"
"skipping user input during test.\n"
)

LC_TEXT = "[bold green]CHARACTER DATA:[/]\nName: _Testificate\nRole: Samurai\nWorld: WoW\ntags:\n - warrior\n - elf\n - swordsman\n"
 
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
def create_character():
    print(Panel.fit(CC_TEXT, title="CHARACTER CREATION PANEL", box=box.DOUBLE))


def load_character():
    print(Panel.fit(LC_TEXT, title="[magenta]CHARACTER CREATION PANEL", box=box.DOUBLE))


def plain_list():
    print(Panel.fit(AC_TEXT, title="CHARACTER CREATION PANEL", box=box.DOUBLE))