import json
from pathlib import Path

class Workspace:
    def __init__(self, name="untitled"):
        self.name = name
        self._variables = {}

    def set(self, name, value):
        self._variables[name] = value

    def get(self, name):
        return self._variables[name]
    
    def delete(self, name):
        del self._variables[name]

    def contains(self, name):
        return name in self._variables

    def save(self, directory):
        path = Path(directory) / f"{self.name}.json"

        data = {
            name: matrix.to_list()
            for name, matrix in self._variables.items()
        }

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file)

    #def save_as(self, name):
        #PLACEHOLDER

    #@classmethod
    #def load(cls, filename):
        #PLACEHOLDER

