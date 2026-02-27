# Perindex‑Tool — v0.1 (Planning)

## About (Pear-what-now?)
Perindex-Tool is a terminal‑based character archival utility for worldbuilders and writers. It provides a simple way to create, sort and retrieve locally stored character cards in a stable, human-readable format.

## To-Do
- Day 1: CLI Initialization ✔
  - Menu, routing, loop, placeholder functions.
- Day 2: Character Creation ✔
  - Prompt user -> build YAML -> save file.
- Day 3: Load Character ✔
  - Load character cards by smart-name search from saved yaml file.
- Day 4: Sorting ✔
  - Sort by name, world, ~~creation date~~, etc.
- Day 5: Tag‑based Search
  - Search by one tag, multiple tags, or tag combinations.
- Day 6: Archive Overview
  - List all characters, basic metadata.
- Day 7: Schema Validation + Data Integrity
  - Ensure every character file is valid, consistent and complete.

- Alt-User Instructions:
  - Cloning the tool
  - Running the tool
  - CLI quick guide

- Third-Party Libraries Used
  - (To be determined)

## Stub Directories/Files
Empty directories and files for possible future use:
- data/samples
- src/perindex/persona (possible interface personality changer?)
- tests/

### Card Schema (t = optional)
- version
- name
- gender
- world (t)
- hair color (t)
- eye color (t)
- skin color(complexion or tone perhaps?)
- tags (require at least 1)
