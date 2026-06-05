from pathlib import Path
import subprocess

cache_file = Path("data/cache/pokemon_types_databank.json")

if cache_file.exists():
    cache_file.unlink()

subprocess.run(["python", "main.py"])