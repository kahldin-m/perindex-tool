# cli.py
import os
import sys

# CONSTANTS
WELCOME_TEXT = """\n>>> WELCOME TO PERINDEX CHARACTER ARCHIVAL TOOL <<<

   OPTIONS 1-4:
    [1] CREATE Character Card
    [2] LOAD Character Card
    [3] VIEW Character Archive
    [4] EXIT
"""


def clear():
    os.system("cls" if os.name == "nt" else "clear")

def main():
    clear()
    print(WELCOME_TEXT)
    input(":<  ")


if __name__ == "__main__":
    main()
