# Perindex‑Tool — Design Notes (v0.1 Planning)

## Project Identity
Perindex‑tool is a terminal‑based character archival utility designed for worldbuilders and writers. It focuses on structured data storage, clean organization, and a future‑friendly architecture that can later support a full UI (Perindex‑app).

## High‑Level Goals
- Provide a CLI interface for creating, editing, and browsing character files.
- Store characters in a human‑readable format inside a predictable folder structure.
- Maintain a clean, modular codebase that can evolve into a GUI application later.
- Present a professional, industry‑standard project layout suitable for a portfolio.

## Project Structure
- src layout
- Modern Python packaging convention.
- Keeps code isolated from project root.
- Modular package structure
- `cli.py` for command handling
- `core.py` for main logic
- `models.py` for data structures
- `utils.py` for helpers
- Data directory
- Stores character files
- Includes sample data for demonstration
- Tests directory
- Even minimal tests show professionalism
- Ensures CLI and core logic behave correctly
- pyproject.toml
- Defines dependencies and metadata
- Enables future installation via `pip`
- Supports entry points for a `perindex` command

## Planned Folder Layout
```
perindex-tool/
│
├── src/
│   └── perindex/
│       ├── init.py
│       ├── cli.py
│       ├── core.py
│       ├── models.py
│       └── utils.py
│
├── data/
│   └── samples/
│
├── tests/
│   └── test_basic.py
│
├── README.md
├── pyproject.toml
├── .gitignore
└── LICENSE
```

## Data Format
- YAML or JSON for structured, readable character files.
- Must support:
  - name
  - role/class
  - description
  - notes
  - tags

## CLI Scope for v0.1
- Basic command parser
- Create new character
- List characters
- View a character file
Future versions may include editing, searching, tagging, and UI integration.

## Future Expansion (Perindex‑app)
- Full graphical interface
- Interactive character creation
- Rich browsing and filtering
- Integration with the CLI backend
