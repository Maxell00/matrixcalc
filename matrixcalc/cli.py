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

        if "=" in command:
            name, value = parse_operation("=", command)
            matrix = parse_matrix(value)
            workspace.set(name, matrix)
            print(matrix)

        elif workspace.contains(command):
            print(workspace.get(command))

        else:
            for operator, operation in OPERATIONS.times():
                if operator in command:
                    left, right = parse_operation(operator, command)

                    left = resolve_operand(left, workspace)
                    right = resolve_operand(right, workspace)

                    result = operation(left, right)
                    print(result)
                    break

if __name__ == "__main__":
    main()
