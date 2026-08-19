from matrixcalc.workspace import Workspace
from matrixcalc.matrix import Matrix
import pytest
import json

def test_workspace_starts_empty():
    workspace = Workspace()

    assert not workspace.contains("A")


def test_workspace_set_and_get():
    workspace = Workspace()
    value = object()

    workspace.set("A", value)

    assert workspace.get("A") is value


def test_workspace_stores_multiple_values():
    workspace = Workspace()
    A = object()
    B = object()

    workspace.set("A", A)
    workspace.set("B", B)

    assert workspace.get("A") is A
    assert workspace.get("B") is B


def test_workspace_set_replaces_existing_value():
    workspace = Workspace()
    A = object()
    B = object()

    workspace.set("A", A)
    workspace.set("A", B)

    assert workspace.get("A") is B


def test_workspace_delete():
    workspace = Workspace()
    A = object()

    workspace.set("A", A)
    workspace.delete("A")

    assert not workspace.contains("A")


def test_workspace_contains():
    workspace = Workspace()
    A = object()

    workspace.set("A", A)

    assert workspace.contains("A")
    assert not workspace.contains("B")


def test_workspace_get_missing_name():
    workspace = Workspace()

    with pytest.raises(KeyError):
        workspace.get("A")


def test_workspace_delete_missing_name():
    workspace = Workspace()

    with pytest.raises(KeyError):
        workspace.delete("A")

def test_save_empty_workspace(tmp_path):
    workspace = Workspace("test")

    workspace.save(tmp_path)

    path = tmp_path / "test.json"

    assert path.exists()

def test_save_workspace(tmp_path):
    workspace = Workspace("test")
    workspace.set("A", Matrix([[1, 2], [3, 4]]))
    workspace.set("B", Matrix([[5, 6], [7, 8]]))

    workspace.save(tmp_path)

    path = tmp_path / "test.json"

    with path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    assert data == {
        "A": [[1, 2], [3, 4]],
        "B": [[5, 6], [7, 8]],
    }

def test_load_workspace(tmp_path):
    workspace = Workspace("test")
    workspace.set("A", Matrix([[1, 2], [3, 4]]))
    workspace.set("B", Matrix([[5, 6], [7, 8]]))

    workspace.save(tmp_path)

    loaded = Workspace.load("test", tmp_path)

    assert loaded.name == "test"
    assert loaded.get("A") == Matrix([[1, 2], [3, 4]])
    assert loaded.get("B") == Matrix([[5, 6], [7, 8]])








