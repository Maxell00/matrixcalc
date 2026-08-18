import ast
from matrixcalc.matrix import Matrix
from matrixcalc.workspace import Workspace

OPERATIONS = {
    "+": lambda a, b: a + b,
    "-": lambda a, b: a - b,
    "*": lambda a, b: a * b,
    "@": lambda a, b: a @ b,
    "/": lambda a, b: a / b,
}

def parse_matrix(text):
    data = ast.literal_eval(text)
    return Matrix(data)

def parse_quick_matrix(text):
    # Takes 'quick matrix input' and returns Matrix object
    # CAN ONLY HANDLE INTEGERS CURRENTLY
    data = [
        [int(value) for value in row.split()]
        for row in text.split(";")
    ]

    return Matrix(data)

def print_matrix(matrix):
    print(matrix)

def parse_operation(delimiter, command):
    left, right = command.split(delimiter, 1)
    return left.strip(), right.strip()

def resolve_operand(operand, workspace):
    if workspace.contains(operand):
        return workspace.get(operand)

    try:
        value = ast.literal_eval(operand)
    except (ValueError, SyntaxError):
        raise ValueError(f"Unknown operand: {operand}")

    if isinstance(value, (int, float)):
        return value

    raise ValueError(f"Unknown operand: {operand}")

def main():
    workspace = Workspace()

    while True:
        command = input("> ")

        if command in ("quit", "exit", "q"):
            print("Goodbye!")
            break

        # Command is an assignment
        if "=" in command:
            name, value = parse_operation("=", command)
            if value[0] == "[":
                matrix = parse_matrix(value)
            else:
                matrix = parse_quick_matrix(value)
            workspace.set(name, matrix)
            print(matrix)

        # Command is recall
        elif workspace.contains(command):
            print(workspace.get(command))

        # Command is an operation or invalid
        else:
            for operator, operation in OPERATIONS.items():
                if operator in command:
                    left, right = parse_operation(operator, command)

                    left = resolve_operand(left, workspace)
                    right = resolve_operand(right, workspace)

                    result = operation(left, right)
                    print(result)
                    break
            # Command is invalid
            print("No valid command")

if __name__ == "__main__":
    main()
