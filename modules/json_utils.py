import json

def dict_to_json(data, file_path):
      file_path.parent.mkdir(parents=True, exist_ok=True)

      with open(file_path, "w") as file:
            json.dump(data, file, indent=4)