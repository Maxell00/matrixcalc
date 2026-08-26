import json
from pathlib import Path
from matrixcalc.matrix import Matrix

class Workspace:
    def __init__(self, name: str = "untitled"):
        self.name = name
        self._variables = {}
        self.dirty = False

    def rename(self, name: str):
        # TODO add name validation
        self.name = name
        self.dirty = True

    def labels(self):
        return self._variables.keys()

    def set(self, name: str, value: Matrix):
        self._variables[name] = value
        self.dirty = True

    def set_cell(
        self,
        name: str, 
        index: tuple[int, int], 
        value: Matrix,
    ):
        self._variables[name][index] = value
        self.dirty = True

    def get(self, name: str):
        return self._variables[name]
    
    def delete(self, name: str):
        del self._variables[name]
        self.dirty = True

    def contains(self, name: str):
        return name in self._variables

    def save(
            self,
            directory: Path,
            *,
            name: str | None = None
        ):
        if name is None:
            name = self.name

        path = Path(directory) / f"{name}.json"

        data = {
            label: matrix.to_list()
            for label, matrix in self._variables.items()
        }

        with path.open("w", encoding="utf-8") as file:
            json.dump(data, file)

        self.dirty = False

    def save_as(self, directory: Path, name: str):
        self.save(directory, name=name)
        self.name = name

        self.dirty = False

    @classmethod
    def load(cls, directory: Path, name: str):
        path = Path(directory) / f"{name}.json"
        
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        workspace = cls(name)

        for label, matrix_data in data.items():
            workspace.set(label, Matrix(matrix_data))
        workspace.dirty = False

        return workspace

