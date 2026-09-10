from pathlib import Path
from matrixcalc.matrix import Matrix, MatrixCellValue
from matrixcalc.workspace import Workspace
from matrixcalc.symlgc import Monomial, Polynomial
from matrixcalc.parse import parse, AssignmentCommand, NamedCommand, OperationCommand, Command, MatrixReference
from matrixcalc.workspace import validate_workspace_name, Workspace

# TODO: Double check: are these necessary?
from collections.abc import Callable
from typing import Any

# pyright: reportExplicitAny=false
# pyright: reportAny=false

# Constants

OPERATIONS: dict[str, Operation] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "@": lambda a, b: a @ b,
    "/": lambda a, b: a / b,
}

# Sets savefile path
# Hardcoded to ~/.matrixcalc/workspaces
WORKSPACE_DIR = Path.home() / ".matrixcalc" / "workspaces"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

LAST_WORKSPACE = WORKSPACE_DIR / ".last_workspace"

MATRIX_NOT_FOUND_MSG = "Matrix not found: " # NOTE: Unused!

# Helper functions

def update_last_workspace(workspace: Workspace) -> None:
    _ = LAST_WORKSPACE.write_text(workspace.name, encoding="utf-8")

def confirm(prompt: str) -> bool:
    response = input(f"{prompt} [y/N] ").strip().lower()
    return response in ("y", "yes")

def resolve_matrix_reference(
    active_workspace: Workspace,
    matrix_reference: MatrixReference,
) -> Matrix:
    if matrix_reference.name not in active_workspace:
        raise ValueError(f"No matrix '{matrix_reference.name}' in workspace")
    return active_workspace[matrix_reference.name]

# NOTE: Func not needed for delete(), slated for deletion
# def ws_file_exists(workspace_dir: Path, workspace_name: str) -> bool:
#     return (workspace_dir / f"{workspace_name}.json".is_file()

# NamedCommand helper functions
def clearall(workspace: Workspace) -> Workspace:
    return Workspace(workspace.name)

def clear(workspace: Workspace, args: list[MatrixReference]) -> Workspace:
    for matrix_reference in args:
        if matrix_reference.name not in workspace:
            print(f"No matrix '{matrix_reference.name}' in workspace")
            return workspace

    for matrix_reference in args:
        workspace.delete_matrix(matrix_reference.name)
    
    return workspace

def clearscreen():
    print("\033[2J\033[H", end="")

def delete(workspace_names: list[str]) -> None:
    for name in workspace_names:
        try:
            Workspace.delete_workspace_file(WORKSPACE_DIR, name)
            print(f"Workspace {name} deleted successfully")
        except (ValueError, PermissionError) as error:
            print(error)

def listall(workspace: Workspace) -> None:
    for label in sorted(workspace.labels()):
        print(f"{label}:")
        print(workspace[label])
        print("")

def list(workspace: Workspace) -> None:
    for label in sorted(workspace.labels()):
        print(label)

def load(active_workspace: Workspace, workspace_to_load: str) -> Workspace
    if not active_workspace.dirty or confirm("Discard changes and load?"):
        print(f"Loading {workspace_to_load}.json... ", end="")
        try:
            active_workspace = Workspace.load(WORKSPACE_DIR, workspace_to_load)
        except ValueError as error:
            print("ERROR")
            print(error)
        else:
            print("Done")

    return active_workspace

def name(active_workspace: Workspace) -> None:
    print(f"Current workspace name: {active_workspace.name}")

def new(active_workspace: Workspace, name: str | None) -> Workspace:
    if not active_workspace.dirty or confirm("Discard unsaved changes and open new workspace?"):
        if name is None:
            return Workspace()
        else:
            return Workspace(name)
    else:
        return active_workspace

def rename(workspace: Workspace, name: str | None) -> Workspace:
    if name is None:
        name = input("New name for current workspace: ").strip()
    try:
        validate_workspace_name(name)
    except ValueError as error:
        print error
        return workspace

    # No validation necessary if receiving str name as argument
    workspace.rename(name)
    return workspace

def save(workspace: Workspace) -> Workspace:
    workspace.save()
    return workspace

def saveas(workspace: Workspace, name: str) -> Workspace:
    workspace.save_as(name)
    return workspace

def set(
    workspace: Workspace,
    matrix_ref: MatrixReference,
    row: int,
    col: int,
    value: MatrixCellValue,
) -> Workspace:
    if matrix_ref.name not in workspace:
        print(f"No matrix '{matrix_ref.name}' in workspace")
        return workspace

    target_matrix = resolve_matrix_reference(workspace, matrix_ref)
    target_matrix_rows, target_matrix_cols = target_matrix.shape
    if row > target_matrix_rows or col > target_matrix_cols:
        print(f"Cell ({row}, {col}) out of range")
    workspace.set_cell(matrix_ref.name, (row, col), value)
    print(workspace.get(matrix_ref.name))

    return workspace

def workspaces() -> None:
    names = sorted(
        path.stem
        for path in WORKSPACE_DIR.iterdir()
        if path.suffix == ".json"
    )

    for name in names:
        print(name)

# Command execution functions
def exec_assignmentcommand(active_workspace: Workspace, command: NamedCommand) -> Workspace:
    pass

def exec_assignmentcommand(active_workspace: Workspace, command: NamedCommand) -> Workspace:
    pass

def exec_operationcommand(active_workspace: Workspace, command: NamedCommand) -> Workspace:
    pass

def exec_command(active_workspace: Workspace, command: Command) -> Workspace:
    if isinstance(command, AssignmentCommand):
        return exec_assignmentcommand(active_workspace, command)

    if isinstance(command, NamedCommand):
        return exec_namedcommand(active_workspace, command)

    if isinstance(command, OperationCommand):
        return exec_operationcommand(active_workspace, command)

    raise TypeError("Unknown command type")

# Main function
def main() -> None:
    active_workspace = Workspace()

    # Auto-load
    # TODO: Add option to disable with flag
    if not LAST_WORKSPACE.is_file():
        print("Autoload failed.")
    else:
        name = LAST_WORKSPACE.read_text(encoding="utf-8").strip()
        try:
            print(f"Loading {name}.json... ", end="")
            active_workspace = Workspace.load(WORKSPACE_DIR, name)
            print("Done")
        except Exception:
            print("\nAutoload failed.")

    # Main REPL
    while True:
        command_line = input("> ")
        
        # Quit logic outside do_command for easier break
        if command_line in ("quit", "exit", "q"):
            if not active_workspace.dirty or confirm("Quit with unsaved changes?"):
                # TODO Disable if autosave flag off
                update_last_workspace(active_workspace)
                print("Goodbye!")
                break

        commands = parse(command_line)

        for command in commands:
            active_workspace = do_command(
                command.strip(),
                active_workspace
            )
        

if __name__ == "__main__":
    main()
