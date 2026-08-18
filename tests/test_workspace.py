from matrixcalc.workspace import Workspace
import pytest

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
