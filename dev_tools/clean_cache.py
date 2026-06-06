from pathlib import Path
import subprocess

cache_file = Path("data/cache/pokemon_names_databank.json")
cache_file_2 = Path("data/cache/pokemon_types_databank.json")

if cache_file.exists():
    cache_file.unlink()

if cache_file_2.exists():
    cache_file_2.unlink()

subprocess.run(["python", "main.py"])