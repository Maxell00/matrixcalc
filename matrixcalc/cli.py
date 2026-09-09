from pathlib import Path
from matrixcalc.matrix import Matrix, MatrixCellValue
from matrixcalc.workspace import Workspace
from matrixcalc.symlgc import Monomial, Polynomial
from matrixcalc.parse import parse, AssignmentCommand, NamedCommand, OperationCommand, Command

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

# Helper functions

def update_last_workspace(workspace: Workspace) -> None:
    _ = LAST_WORKSPACE.write_text(workspace.name, encoding="utf-8")

def confirm(prompt: str) -> bool:
    response = input(f"{prompt} [y/N] ").strip().lower()
    return response in ("y", "yes")

def clear_screen():
    print("\033[2J\033[H", end="")

def exec_namedcommand(active_workspace: Workspace, command: NamedCommand)
def exec_namedcommand(active_workspace: Workspace, command: NamedCommand)
def exec_namedcommand(active_workspace: Workspace, command: NamedCommand)



def exec_command(active_workspace: Workspace, command: Command) -> Workspace:
    if isinstance(command, NamedCommand):
        
    if isinstance(command, AssignmentCommand):

    if isinstance(command, OperationCommand):


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
