import ast
from pathlib import Path
from matrixcalc.matrix import Matrix
from matrixcalc.workspace import Workspace

# TODO: Add autosave-load functionality, handle on-off with flag, set related constant (if necessary)

# Sets savefile path
WORKSPACE_DIR = Path.home() / ".matrixcalc" / "workspaces"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

LAST_WORKSPACE = WORKSPACE_DIR / ".last_workspace"

OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "@": lambda a, b: a @ b,
    "/": lambda a, b: a / b,
}

def parse_number(text):
    try:
        value = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        raise ValueError(f"Invalid number: {text}")

    if isinstance(value, (int, float)):
        return value

    raise ValueError(f"Invalid number: {text}")

def parse_matrix(text):
    data = ast.literal_eval(text)
    return Matrix(data)

def parse_quick_matrix(text):
    # Takes 'quick matrix input' and returns Matrix object
    # Currently assumed all values are numbers
    data = [
        [parse_number(value) for value in row.split()]
        for row in text.split(";")
    ]

    return Matrix(data)

def parse_operation(delimiter, command):
    left, right = command.split(delimiter, 1)
    return left.strip(), right.strip()

def resolve_operand(operand, workspace):
    if workspace.contains(operand):
        return workspace.get(operand)

    return parse_number(operand)

def update_last_workspace(workspace):
    LAST_WORKSPACE.write_text(workspace.name, encoding="utf-8")

def confirm(prompt):
    response = input(f"{prompt} [y/N] ").strip().lower()
    return response in ("y", "yes")

def do_command(command, active_workspace):

    # Handle named commands

    if command == "name":
        print(active_workspace.name)

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

    # Save as after prompt
    elif command in ("save as", "saveas"):
        name = input("Save as: ").strip()
        # Validate here or workspace level?
        print(f"Saving as {name}.json... ", end="")
        active_workspace.save_as(WORKSPACE_DIR, name)
        print("Done.")

    # Save as immediately
    elif command.startswith("save as "):
        name = command[len("save as "):].strip()
        # Validate here or workspace level?
        print(f"Saving as {name}.json... ", end="")
        active_workspace.save_as(WORKSPACE_DIR, name)
        print("Done.")

    elif command.startswith("load "):
        if active_workspace.dirty and confirm("Discard changes and load?"):
            name = command[len("load "):].strip()
            # Validate here or workspace level?
            print(f"Loading {name}.json... ", end="")
            active_workspace = active_workspace.load(WORKSPACE_DIR, name)
            print("Done.")

    # Show loadable workspaces
    elif command in ("workspaces", "ws"):
        for path in WORKSPACE_DIR.iterdir():
            if path.suffix == ".json":
                print(path.stem)

    elif command.startswith("set name "):
        name = command[len("set name "):].strip()
        # Allow validation to happen on the workspace level (?)
        active_workspace.rename(name)

    elif command in ("list", "ls"):
        for label in active_workspace.labels():
            print(label)

    elif command in ("list all", "listall"):
        for label in active_workspace.labels():
            print(f"{label}:")
            print(active_workspace.get(label))
            print("")

    # Command is an assignment
    elif "=" in command:
        name, value = parse_operation("=", command)
        # Long matrix syntax
        if value[0] == "[":
            matrix = parse_matrix(value)
        # Quick matrix sytax
        else:
            matrix = parse_quick_matrix(value)
        active_workspace.set(name, matrix)
        print(matrix)

    elif command.startswith("clear ") or command.startswith("clr "):
        name = command[len("clear "):].strip()
        # TODO Add validation
        active_workspace.delete(name)

    elif command in ("clearall", "clear all"):
        if not active_workspace.dirty or confirm("Discard changes and clear workspace?"):
            active_workspace = Workspace(active_workspace.name)
            active_workspace.dirty = True

    elif command == "new":
        if active_workspace.dirty and confirm("Discard unsaved changes and open new workspace?"):
            active_workspace = Workspace()

    # Command is storage, operation, recall, or invalid
    # Gets 'result' and then stores or prints outside chain
    else:
        result = None

        # Get storage var and strip
        storage_var = None
        if ">>" in command:
            command, storage_var = parse_operation(">>", command)

        # Get operation and operator
        operation = None
        operator = None

        for op, func in OPERATIONS.items():
            if op in command:
                operator = op
                operation = func
                break

        # Command is recall
        if active_workspace.contains(command):
            result = active_workspace.get(command)

        # Command is an operation
        elif operator is not None and operation is not None:
            left, right = parse_operation(operator, command)

            left = resolve_operand(left, active_workspace)
            right = resolve_operand(right, active_workspace)
            result = operation(left, right)

        # Print and store result
        if result is not None:
            if storage_var is not None:
                active_workspace.set(storage_var, result)
            print(result)
        # Unless command is invalid
        else:
            print("No valid command")

    return active_workspace

def main():
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
