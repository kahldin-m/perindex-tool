# Perindex‑Tool — v1.1.1 🍐
## About (Pear-what-now?)
Perindex-Tool is a terminal‑based character archival tool I built for keeping track of my many characters across multiple fictional worlds and settings.
It provides a fast and easy way to create, sort and retrieve locally stored character cards in a stable, human-readable format.

Here's an example of a card:
![Character Card](assets/robin_hood.png)

And here's an example of what an overview of the archive—or collection of character cards—could look like:
![Archive Overview](assets/overview.png)


## Requirements
- Python 3.10+ (You can check your python version with this: )
```
python --version
```
- pip
(Most Python installations already include pip. If your system doesn't have it, you can install/upgrade it with: )
```
python -m pip install --upgrade pip
```
Note: If *python* doesn't work in the console, try *python3* in its place

## How To Use
Starting in your preferred terminal:
1. Clone the repo
```
git clone https://github.com/kahldin-m/perindex-tool.git
```
2. Enter the project folder
```
cd perindex-tool
```
3. Install perindex as a package (editable mode)
```
pip install -e .
```
4. Run the tool
```
perindex
```

If you ever need to update the tool, use the following command while in /perindex-tool:
```
git pull
```
This will update the code while preserving your character archive in /data/characters

### Third-Party Libraries Used
  - PyYAML
  - Rich

### Possibilities
- Add richer archive visualisations or statistics
- Explore decoupling UI, operations, repository and storage layers (repository pattern)
- Alternative storage backends (SQLite)
- Expand metadata analysis (relationships, world summaries, etc)