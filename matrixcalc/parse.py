from __future__ import annotations
import ast
import re
from matrixcalc.matrix import Matrix, MatrixCellValue
from matrixcalc.symlgc import Monomial, Polynomial
from dataclasses import dataclass
from collections.abc import Sequence

# handle = case

VALID_OPERATORS = {"+", "-", "*", "@", "/"}
NAMED_COMMANDS = {
    "clearall",
    "clr",
    "clear",
    "cls",
    "clearscreen",
    "del",
    "delete",
    "la",
    "listall",
    "ls",
    "list",
    "load",
    "name",
    "new",
    "rename",
    "save",
    "saveas",
    "workspaces",
    "ws",
}

ASSIGNMENT_USAGE_MSG = ""
OPERATION_USAGE_MSG = ""

CLEAR_USAGE_MSG = ""
CLEARALL_USAGE_MSG = ""
CLEARSCREEN_USAGE_MSG = ""
DELETE_USAGE_MSG = ""
LIST_USAGE_MSG = ""
LISTALL_USAGE_MSG = ""
LOAD_USAGE_MSG = ""
NAME_USAGE_MSG = ""
NEW_USAGE_MSG = ""
RENAME_USAGE_MSG = ""
SAVE_USAGE_MSG = ""
SAVEAS_USAGE_MSG = ""
WORKSPACES_USAGE_MSG = ""

INVALID_COMMAND_MSG = ""
INVALID_WS_NAME_MSG = ""
INVALID_STORAGE_MSG = ""

TERM_BODY_RE = r"(?:\d+)?(?:[a-z]\d*)+"
TERM_RE = rf"[+-]?{TERM_BODY_RE}"
POLYNOMIAL_RE = rf"{TERM_RE}(?:[+-]{TERM_BODY_RE})*"

class ParseError(ValueError):
    pass

@dataclass
class Command:
    """A parsed CLI command."""


@dataclass
class NamedCommand(Command):
    name: str
    args: Sequence[str | MatrixReference]


@dataclass
class OperationCommand(Command):
    operands: list[Operand]
    operators: list[str]
    destination: list[MatrixReference] | None

    def __post_init__(self) -> None:
        if len(self.operands) != len(self.operators) + 1:
            raise ValueError(
                "Operation command must have one more operand than operator"
            )


@dataclass
class AssignmentCommand(Command):
    target: MatrixReference
    value: Matrix


class MatrixReference:
    def __init__(self, name: str) -> None:
        if len(name) != 1 or not name.isascii() or not name.isalpha():
            raise ValueError("Matrix reference must be a single ASCII character")
        self._name: str = name.upper()

    @property
    def name(self) -> str:
        return self._name

Operand = Polynomial | MatrixReference | int | float

# Helper functions
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

def validate_workspace_name(name: str) -> None:
    #TODO: Copy over WORKSPACE NAME RE and add check
    pass

# Parse Functions
def parse_number(text: str) -> int | float:
    try:
        value = ast.literal_eval(text) # pyright: ignore[reportAny]
    except (ValueError, SyntaxError):
        raise ValueError(f"Invalid number: {text}")

    if not isinstance(value, (int, float)):
        raise ValueError(f"Invalid number: {text}")
    
    return value

def parse_polynomial(text: str) -> Polynomial:
    result_data: dict[Monomial, int | float] = {}

    # Ensure valid input string
    if not re.fullmatch(POLYNOMIAL_RE, text):
        raise ValueError("Invalid Polynomial")

    # Split into terms in the form "-2x2yz"
    terms: list[str] = re.findall(TERM_RE, text)

    # Normalize explicit sign for first term
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

def parse_operand(operand: str) -> MatrixCellValue | MatrixReference:
    try:
        return parse_value(operand)
    except ValueError:
        return MatrixReference(operand)

def parse_value(text: str) -> MatrixCellValue:
    try:
        return parse_number(text)
    except ValueError:
        return parse_polynomial(text)

def parse_quick_matrix(quick_matrix_entry: str) -> Matrix:
    """Parse string with quick matrix syntax into a Matrix object.

    Rows are separated by semicolons; entries within a row are
    separated by whitespace. Each entry must be a valid number or
    polynomial.
    """
    data = [
        [parse_value(value) for value in row]
        for row in quick_matrix_entry.split(";")
    ]

    return Matrix(data)

# Functions to parse command by type
def parse_named_command(arglist: list[str]) -> NamedCommand:
    command = arglist[0]

    match command:
        case "clearall":
            if len(arglist) != 1:
                raise ParseError(CLEARALL_USAGE_MSG)
            return NamedCommand(
                name="clearall",
                args=[],
            )

        case "clr" | "clear":
            if len(arglist) == 1:
                raise ParseError(CLEAR_USAGE_MSG)

            if arglist[1] == "screen":
                if len(arglist) != 2:
                    raise ParseError(CLEARSCREEN_USAGE_MSG)
                return NamedCommand(
                    name="clearscreen",
                    args=[],
                )

            if arglist[1] == "all":
                if len(arglist) != 2:
                    raise ParseError(CLEARALL_USAGE_MSG)
                return NamedCommand(
                    name="clearall",
                    args=[],
                )

            try:
                parsed_args = [MatrixReference(arg) for arg in arglist[1:]]
            except ValueError:
                raise ParseError(CLEAR_USAGE_MSG)

            return NamedCommand(
                name="clear",
                args=parsed_args,
            )

        case "cls" | "clearscreen":
            if len(arglist) != 1:
                raise ParseError(CLEARSCREEN_USAGE_MSG)

            return NamedCommand(
                name="clearscreen",
                args=[],
            )

        case "del" | "delete":
            if len(arglist) == 1:
                raise ParseError(DELETE_USAGE_MSG)

            parsed_args = arglist[1:]
            try:
                for arg in parsed_args:
                    #TODO: Write this function!
                    validate_workspace_name(arg)
            except ValueError:
                raise ParseError(DELETE_USAGE_MSG)

            return NamedCommand(
                name="delete",
                args=parsed_args,
            )

        case "la" | "listall":
            if len(arglist) != 1:
                raise ParseError(LISTALL_USAGE_MSG)

            return NamedCommand(
                name="listall",
                args=[],
            )

        case "ls" | "list":
            if len(arglist) > 1 and arglist[1] == "all":
                if len(arglist) > 2:
                    raise ParseError(LISTALL_USAGE_MSG)
                return NamedCommand(
                    name="listall",
                    args=[],
                )

            if len(arglist) != 1:
                raise ParseError(LIST_USAGE_MSG)

            return NamedCommand(
                name="list",
                args=[],
            )

        case "load":
            if len(arglist) != 2:
                raise ParseError(LOAD_USAGE_MSG)

            workspace_name = arglist[1]
            try:
                validate_workspace_name(workspace_name)
            except ValueError:
                raise ParseError(INVALID_WS_NAME_MSG)

            return NamedCommand(
                name="load",
                args=[workspace_name],
            )

        case "name":
            if len(arglist) != 1:
                raise ParseError(NAME_USAGE_MSG)

            return NamedCommand(
                name="name",
                args=[],
            )

        case "new":
            if len(arglist) > 2:
                raise ParseError(NEW_USAGE_MSG)

            if len(arglist) == 1:
                return NamedCommand(
                    name="new",
                    args=[],
                )

            workspace_name = arglist[1]
            try:
                validate_workspace_name(workspace_name)
            except ValueError:
                raise ParseError(INVALID_WS_NAME_MSG)
            
            return NamedCommand(
                name="new",
                args=[workspace_name],
            )

        case "rename":
            if len(arglist) > 2:
                raise ParseError(RENAME_USAGE_MSG)

            if len(arglist) == 1:
                return NamedCommand(
                    name="rename",
                    args=[],
                )

            workspace_name = arglist[1]
            try:
                validate_workspace_name(workspace_name)
            except ValueError:
                raise ParseError(INVALID_WS_NAME_MSG)

            return NamedCommand(
                name="rename",
                args=[workspace_name],
            )

        case "save":
            if len(arglist) > 1 and arglist[1] == "as":
                if len(arglist) > 3:
                    raise ParseError(SAVEAS_USAGE_MSG)

                if len(arglist) == 3:
                    workspace_name = arglist[2]
                    try:
                        validate_workspace_name(workspace_name)
                    except ValueError:
                        raise ParseError(INVALID_WS_NAME_MSG)

                    return NamedCommand(
                        name="saveas",
                        args=[workspace_name],
                    )

                return NamedCommand(
                    name="saveas",
                    args=[],
                )
                

            if len(arglist) != 1:
                raise ParseError(SAVE_USAGE_MSG)

            return NamedCommand(
                name="save",
                args=[],
            )

        case "saveas":
            if len(arglist) > 2:
                raise ParseError(SAVEAS_USAGE_MSG)

            if len(arglist) == 2:
                workspace_name = arglist[1]
                try:
                    validate_workspace_name(workspace_name)
                except ValueError:
                    raise ParseError(INVALID_WS_NAME_MSG)

                return NamedCommand(
                    name="saveas",
                    args=[workspace_name],
                )

            return NamedCommand(
                name="saveas",
                args=[],
            )

        case "workspaces" | "ws":
            if len(arglist) != 1:
                raise ParseError(WORKSPACES_USAGE_MSG)

            return NamedCommand(
                name="workspaces",
                args=[],
            )

        case _:
            raise ParseError(INVALID_COMMAND_MSG)


def parse_assignment_command(arglist: list[str]) -> AssignmentCommand:
    if arglist[1] != "=" or arglist.count("=") != 1:
        raise ParseError(ASSIGNMENT_USAGE_MSG)

    try:
        target = MatrixReference(arglist[0])
    except ValueError:
        raise ParseError(ASSIGNMENT_USAGE_MSG)

    quick_matrix_string = " ".join(arglist[2:])

    try:
        value = parse_quick_matrix(quick_matrix_string)
    except ValueError:
        raise ParseError(ASSIGNMENT_USAGE_MSG)

    return AssignmentCommand(
        target=target,
        value=value,
    )


def parse_operation_command(arglist: list[str]) -> OperationCommand:
    destination = None
    if ">>" in arglist:
        if arglist.count(">>") > 1:
            raise ParseError(INVALID_STORAGE_MSG)

        split_index = arglist.index(">>")

        storage_vars = arglist[split_index + 1:]
        arglist = arglist[:split_index]

        if not storage_vars:
            raise ParseError(INVALID_STORAGE_MSG)

        try:
            destination = [
                MatrixReference(var)
                for var in storage_vars
            ]
        except ValueError:
            raise ParseError(INVALID_STORAGE_MSG)

    if len(arglist) % 2 == 0:
        raise ParseError(OPERATION_USAGE_MSG)

    operands = arglist[::2]
    operators = arglist[1::2]

    if not all(op in VALID_OPERATORS for op in operators):
        raise ParseError(OPERATION_USAGE_MSG)

    try:
        operands = [
            parse_operand(op)
            for op in operands
        ]
    except ValueError:
        raise ParseError(OPERATION_USAGE_MSG)

    return OperationCommand(
        operands=operands,
        operators=operators,
        destination=destination,
    )

# Primary function
def parse(line: str) -> list[Command]:
    arglist = line.split()

    if not arglist:
        raise ParseError("Empty command")

    if arglist[0] in NAMED_COMMANDS:
        return parse_named_command(arglist)

    if "=" in arglist:
        return parse_assignment_command(arglist)

    else:
        return parse_operation_command(arglist)





