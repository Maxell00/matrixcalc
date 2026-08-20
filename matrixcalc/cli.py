import ast
from pathlib import Path
from matrixcalc.matrix import Matrix
from matrixcalc.workspace import Workspace

# TODO: Add autosave-load functionality, handle on-off with flag, set related constant (if necessary)

# Sets savefile path
WORKSPACE_DIR = Path.home() / ".matrixcalc" / "workspaces"
WORKSPACE_DIR.mkdir(parents=True, exist_ok=True)

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

def main():
    workspace = Workspace()

    while True:
        command = input("> ")
        
        # Handle named commands
        if command in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        elif command == "name":
            print(workspace.name)

        elif command == "save":
            if workspace.name == "untitled":
                name = input("Save as: ").strip()
                workspace.save_as(WORKSPACE_DIR, name)
            else:
                workspace.save(WORKSPACE_DIR)

        # Save as after prompt
        elif command == "save as":
            name = input("Save as: ").strip()
            # #debug
            # breakpoint()
            print(f"saving as {name}.json...")
            workspace.save_as(WORKSPACE_DIR, name)

        # Save as immediately
        elif command.startswith("save as "):
            name = command[len("save as "):].strip()
            workspace.save_as(WORKSPACE_DIR, name)

        elif command.startswith("load "):
            name = command[len("load "):].strip()
            # TODO Prevent data loss by checking diff since save
            workspace = workspace.load(WORKSPACE_DIR, name)

        elif command.startswith("set name "):
            name = command[len("set name "):].strip()
            workspace.rename(name)

        # Command is an assignment
        elif "=" in command:
            name, value = parse_operation("=", command)
            # Long matrix syntax
            if value[0] == "[":
                matrix = parse_matrix(value)
            # Quick matrix sytax
            else:
                matrix = parse_quick_matrix(value)
            workspace.set(name, matrix)
            print(matrix)

        # Command is recall
        elif workspace.contains(command):
            print(workspace.get(command))

        # Command is an operation or invalid
        else:
            # Command is an operation
            for operator, operation in OPERATIONS.items():
                if operator in command:
                    left, right = parse_operation(operator, command)

                    left = resolve_operand(left, workspace)
                    right = resolve_operand(right, workspace)

                    result = operation(left, right)
                    print(result)
                    break
            # Command is invalid
            else:
                print("No valid command")

if __name__ == "__main__":
    main()
