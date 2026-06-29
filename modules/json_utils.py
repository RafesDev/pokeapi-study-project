import json

def dict_to_json(data, file_name):
      file_name.parent.mkdir(parents=True, exist_ok=True)

      with open(file_name, "w") as file:
            json.dump(data, file, indent=4)