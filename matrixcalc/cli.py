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

    while True:
        command = input("> ")
        
        # Handle named commands
        if command in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        elif command == "name":
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
        elif command == "save as":
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
            name = command[len("load "):].strip()
            # TODO Prevent data loss by checking diff since save
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
            # Allow validation to happen on the workspace lebel (?)
            active_workspace.rename(name)

        elif command == "list":
            for label in active_workspace.labels():
                print(label)

        elif command == "list all":
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

        # Command is recall
        elif active_workspace.contains(command):
            print(active_workspace.get(command))

        # Command is an operation or invalid
        else:
            # Command is an operation
            for operator, operation in OPERATIONS.items():
                if operator in command:
                    left, right = parse_operation(operator, command)

                    left = resolve_operand(left, active_workspace)
                    right = resolve_operand(right, active_workspace)

                    result = operation(left, right)
                    print(result)
                    break
            # Command is invalid
            else:
                print("No valid command")

if __name__ == "__main__":
    main()
