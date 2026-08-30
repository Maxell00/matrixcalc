from __future__ import annotations
import json
import os
import re
import tempfile
from pathlib import Path
from matrixcalc.matrix import Matrix, MatrixValue
from collections.abc import KeysView

# Constants
WORKSPACE_NAME_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,63}$")

def validate_workspace_name(workspace_name: str) -> None:
    if not WORKSPACE_NAME_RE.fullmatch(workspace_name):
        raise ValueError(
            "Workspace name must be 1–64 characters and contain only "
            "letters, numbers, '-' or '_'; it must start with a letter or number."
        )

def validate_matrix_name(matrix_name: str) -> str:
    if len(matrix_name) != 1:
        raise ValueError("Matrix name must be 1 character")
    if not matrix_name.isalpha() or not matrix_name.isascii():
        raise ValueError("Matrix name must be an ASCII letter")
    return matrix_name.upper()

class Workspace:
    _variables: dict[str, Matrix]

    def __init__(self, name: str = "untitled") -> None:
        validate_workspace_name(name)
        self.name = name
        self._variables = {}
        self.dirty = False

    def rename(self, name: str) -> None:
        # TODO add name validation
        self.name = name
        self.dirty = True

    def labels(self) -> KeysView[str]:
        return self._variables.keys()

    def set(self, name: str, value: Matrix) -> None:
        name = validate_matrix_name(name)
        self._variables[name] = value
        self.dirty = True

    def set_cell(
        self,
        name: str, 
        index: tuple[int, int], 
        value: MatrixValue,
    ) -> None:
        self._variables[name][index] = value
        self.dirty = True

    def get(self, name: str) -> Matrix:
        return self._variables[name]
    
    def delete(self, name: str) -> None:
        del self._variables[name]
        self.dirty = True

    def contains(self, name: str) -> bool:
        return name in self._variables

    def save(
            self,
            directory: Path,
            *,
            name: str | None = None,
        ) -> None:
        if name is None:
            name = self.name

        validate_workspace_name(name)

        target_path = directory / f"{name}.json"

        data = {
            label: matrix.to_list()
            for label, matrix in self._variables.items()
        }

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=directory,
            delete=False,
        ) as file:
            json.dump(data, file)
            temp_path = Path(file.name)

        os.replace(temp_path, target_path)

        self.dirty = False

    def save_as(self, directory: Path, name: str) -> None:
        self.save(directory, name=name)
        self.name = name

        self.dirty = False

    @classmethod
    def load(cls, directory: Path, name: str) -> Workspace:
        path = Path(directory) / f"{name}.json"
        
        with path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        workspace = cls(name)

        for label, matrix_data in data.items():
            workspace.set(label, Matrix.from_list(matrix_data))
        workspace.dirty = False

        return workspace

