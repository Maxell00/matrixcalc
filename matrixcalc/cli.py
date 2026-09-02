import ast
import re
from pathlib import Path
from matrixcalc.matrix import Matrix, MatrixCellValue
from matrixcalc.workspace import Workspace
from matrixcalc.symlgc import Monomial, Polynomial
from collections.abc import Callable
from typing import Any

# TODO: Add autosave-load functionality, handle on-off with flag, set related constant (if necessary)

# Sets savefile path
# Hardcoded to ~/.matrixcalc/workspaces
WORKSPACE_DIR = Path.home() / ".matrixcalc" / "workspaces"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

LAST_WORKSPACE = WORKSPACE_DIR / ".last_workspace"

# pyright: reportExplicitAny=false
# pyright: reportAny=false

Operand = MatrixCellValue | Matrix
Operation = Callable[[Any, Any], Any]

OPERATIONS: dict[str, Operation] = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "@": lambda a, b: a @ b,
    "/": lambda a, b: a / b,
}

# Methods

def parse_value(text: str) -> MatrixCellValue:
    try:
        return parse_number(text)
    except ValueError:
        return parse_polynomial(text)

def parse_number(text: str) -> int | float:
    try:
        value = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        raise ValueError(f"Invalid number: {text}")

    if isinstance(value, (int, float)):
        return value

    raise ValueError(f"Invalid number: {text}")

def command_is_op(command: str) -> bool:
    parts = command.split()
    return any(part in OPERATIONS for part in parts)

# NOTE: Only supports entry of polynomials with positive exponents
# Even though underlying data structure can support negative exponents
# TODO: Add internal and user facing format specification
def parse_polynomial(text: str) -> Polynomial:
    result_data: dict[Monomial, int | float] = {}

    # Split into terms in the form "-2x2yz"
    terms = re.findall(r"[+-]?(?:\d+)?(?:[a-z]\d*)+", text)

    # Ensure first term has an explicit sign
    if terms[0][0] not in "+-":
        terms[0] = "+" + terms[0]
    for term in terms:
        is_negative = term[0] == "-"
        term = term[1:]

        # Find constant_coef
        constant_coef = 1
        if term[0].isdigit():
            match = re.match(r"\d+", term)
            if match:
                constant_coef = int(match.group())
        if is_negative:
            constant_coef = -constant_coef

        # Find monomial
        variables = re.findall(r"[a-z]\d*", term)
        mono = varlist_to_monomial(variables) 

        # Assign to internal dict
        if mono in result_data:
            raise ValueError("Polynomial cannot have repeated Monomials")
        result_data[mono] = constant_coef

    return Polynomial(result_data)

def varlist_to_monomial(varlist: list[str]) -> Monomial:
    result_data: dict[str, int] = {}
    for variable in varlist:
        letter = variable[0]
        if letter in result_data:
            raise ValueError("Monomial cannot have repeated variables")
        exponent = 1

        if len(variable) > 1:
            exponent = int(variable[1:])
        result_data[letter] = exponent

    return Monomial(result_data)
        
def parse_matrix(text: str) -> Matrix:
    data = ast.literal_eval(text)
    return Matrix(data)

def parse_quick_matrix(text: str) -> Matrix:
    # Takes 'quick matrix input' and returns Matrix object
    # All values must be numbers or Polynomials
    data = [
        [parse_value(value) for value in row.split()]
        for row in text.split(";")
    ]

    return Matrix(data)

def parse_operation(delimiter: str, command: str) -> tuple[str, str]:
    left, right = command.split(delimiter, 1)
    return left.strip(), right.strip()

# TODO Verify, does this need to handle Polynomial?
# Resolve an operand string from CLI into a number or Matrix
def resolve_operand(operand: str, workspace: Workspace) -> int | float | Matrix:
    if workspace.contains(operand):
        return workspace.get(operand)
    return parse_number(operand)

def update_last_workspace(workspace: Workspace) -> None:
    _ = LAST_WORKSPACE.write_text(workspace.name, encoding="utf-8")

def confirm(prompt: str) -> bool:
    response = input(f"{prompt} [y/N] ").strip().lower()
    return response in ("y", "yes")

def do_command(command: str, active_workspace: Workspace) -> Workspace:

    # Handle named commands
    if command == "name":
        print(active_workspace.name)
        return active_workspace

    elif command == "save":
        if active_workspace.name == "untitled":
            name = input("Save as: ").strip()
            # Validation?
            print(f"Saving as {name}.json... ", end="")
            active_workspace.save_as(WORKSPACE_DIR, name)
            print("Done.")
        else:
            print(f"Saving {active_workspace.name}.json... ", end="")
            active_workspace.save(WORKSPACE_DIR)
            print("Done")

        return active_workspace

    # Save as after prompt
    elif command in ("save as", "saveas"):
        name = input("Save as: ").strip()
        # Validate here or workspace level?
        print(f"Saving as {name}.json... ", end="")
        active_workspace.save_as(WORKSPACE_DIR, name)
        print("Done.")

        return active_workspace

    # Save as immediately
    elif command.startswith("save as ") or command.startswith("saveas "):
        prefix = (
            "save as "
            if command.startswith("save as ")
            else "saveas "
        )
        name = command[len(prefix):].strip()

        print(f"Saving as {name}.json... ", end="")
        # TODO: Add a try to catch name ValueErrors
        active_workspace.save_as(WORKSPACE_DIR, name)
        print("Done.")

        return active_workspace

    elif command.startswith("load "):
        if not active_workspace.dirty or confirm("Discard changes and load?"):
            name = command[len("load "):].strip()
            # Validate here or workspace level?
            print(f"Loading {name}.json... ", end="")
            active_workspace = active_workspace.load(WORKSPACE_DIR, name)
            print("Done.")

        return active_workspace

    # Show loadable workspaces
    elif command in ("workspaces", "ws"):
        names = sorted(
            path.stem
            for path in WORKSPACE_DIR.iterdir()
            if path.suffix == ".json"
        )

        for name in names:
            print(name)

        return active_workspace

    # Rename after prompt
    elif command == "rename":
        name = input("Rename: ").strip()
        active_workspace.rename(name)
        return active_workspace

    # Rename immediately
    elif command.startswith("rename "):
        name = command[len("rename "):].strip()
        # TODO Validate here or in workspace.py
        active_workspace.rename(name)
        return active_workspace

    elif command in ("list", "ls"):
        for label in sorted(active_workspace.labels()):
            print(label)
        return active_workspace

    elif command in ("list all", "listall", "la"):
        for label in sorted(active_workspace.labels()):
            print(f"{label}:")
            print(active_workspace.get(label))
            print("")
        return active_workspace

    # Command is an assignment
    elif "=" in command:
        name, value = parse_operation("=", command)
        # Long matrix syntax
        if value[0] == "[":
            matrix = parse_matrix(value)
        # Quick matrix sytax
        else:
            matrix = parse_quick_matrix(value)
        try:
            active_workspace.set(name, matrix)
        except ValueError as e:
            print(e)
            return active_workspace
        print(matrix)
        return active_workspace

    elif command.startswith("clear ") or command.startswith("clr "):
        name = command.split(maxsplit=1)[1]
        # TODO: Error handling
        active_workspace.delete_matrix(name)
        return active_workspace

    elif command in ("clearall", "clear all"):
        if not active_workspace.dirty or confirm("Discard changes and clear workspace?"):
            active_workspace = Workspace(active_workspace.name)
            active_workspace.dirty = True
        return active_workspace

    elif command == "new":
        if not active_workspace.dirty or confirm("Discard unsaved changes and open new workspace?"):
            active_workspace = Workspace()
        return active_workspace

    elif command.startswith("new "):
        if not active_workspace.dirty or confirm("Discard unsaved changes and open new workspace?"):
            name = command.split(maxsplit=1)[1]
            active_workspace = Workspace(name=name)
        return active_workspace

    # Command is storage, operation, recall,
    # set, or invalid
    # Gets 'result' and then stores or prints outside chain
    else:
        result: Matrix | None = None

        # Get storage var and strip
        storage_var = None
        if ">>" in command:
            command, storage_var = parse_operation(">>", command)

        # Command is recall
        if active_workspace.contains(command):
            result = active_workspace.get(command)

        # Command is set
        elif command.startswith("set "):
            # Split by ' ' delim
            parts = command.split()

            if len(parts) != 5:
                print("Usage: set NAME ROW COL VALUE")
                return active_workspace
            else:
                # Set name, row, col, value
                name = parts[1]
                row = int(parts[2]) - 1
                col = int(parts[3]) - 1
                value = parse_value(parts[4])

                active_workspace.set_cell(name, (row, col), value)
                result = active_workspace.get(name)

        # Assumes operand operator operand etc. syntax
        # e.g. A + B - C * 3
        elif command_is_op(command):
            parts = command.split()

            working_total: MatrixCellValue | Matrix = resolve_operand(parts[0], active_workspace)
            for i in range(1, len(parts), 2):
                op_string = parts[i]
                operation = OPERATIONS[op_string]
                operand2  = resolve_operand(parts[i + 1], active_workspace)
                working_total = operation(working_total, operand2)
            if not isinstance(working_total, Matrix):
                raise ValueError("Operation did not produce matrix")

            result = working_total

        # Print and store result
        if result is not None:
            if storage_var is not None:
                active_workspace.set(storage_var, result.copy())
            print(f"{result}\n")
        else:
            print("No valid command")

    return active_workspace

def main() -> None:
    active_workspace = Workspace()

    # Auto-load
    # TODO Add option to disable with flag
    if LAST_WORKSPACE.is_file():
        name = LAST_WORKSPACE.read_text(encoding="utf-8").strip()
        try:
            print(f"Loading {name}.json... ", end="")
            active_workspace = active_workspace.load(WORKSPACE_DIR, name)
            print("Done.")
        except:
            print("\nAutoload failed.")
    else:
        print("Autoload failed.")

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

        commands = command_line.split("|")

        for command in commands:
            active_workspace = do_command(
                command.strip(),
                active_workspace
            )
        

if __name__ == "__main__":
    main()
