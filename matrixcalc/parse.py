import re
from matrixcalc.matrix import Matrix, MatrixCellValue
from matrixcalc.symlgc import Monomial, Polynomial
from dataclasses import dataclass

# TODO: Make Operand + Operator data class
# handle = case
# make MatrixReference class
# define ParseError

VALID_OPERATORS = {"+", "-", "*", "@", "/"}
NAMED_COMMANDS = {} #FINISH THIS!!

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

# add rest of named command usage msgs


@dataclass
class Command:
    """A parsed CLI command."""


@dataclass
class NamedCommand(Command):
    name: str
    args: list[object]


@dataclass
class OperationCommand(Command):
    operands: list[Operand]
    operators: list[str]
    destination: MatrixReference | None

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
        self._name = name.upper()

    @property
    def name(self) -> str:
        return self._name

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
        value = ast.literal_eval(text)
    except (ValueError, SyntaxError):
        raise ValueError(f"Invalid number: {text}")

    if isinstance(value, (int, float)):
        return value

    raise ValueError(f"Invalid number: {text}")

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

def parse_value(text: str) -> MatrixCellValue:
    try:
        return parse_number(text)
    except ValueError:
        return parse_polynomial(text)

def parse_quick_matrix(quick_matrix_entry: list[str]) -> Matrix:
    # Takes 'quick matrix input' and returns Matrix object
    # All values must be numbers or Polynomials
    # TODO: Add validation, raise more errors!
    # TODO: Move this comment to docstring?
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
                raise ParseError(CLR_USAGE_MSG)

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
                raise ParseError(CLR_USAGE_MSG)

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
                # TODO: Write this error!
                # should specify invalid ws name
                # can reuse error after written for other wsname cmds
                raise ParseError("")

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
                # TODO: Write this error!
                # reused -- use a constant
                raise ParseError("")
            
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
                # TODO: Write this error!
                # reused -- use a constant
                raise ParseError("")

            return NamedCommand(
                name="rename",
                args=[workspace_name],
            )

        case "save":
            if len(arglist) > 1 and arglist[1] == "as":
                # handle as case
                pass

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
                    # TODO: Write this error!
                    # reused -- use a constant
                    raise ParseError("")

                return NamedCommand(
                    name="saveas",
                    args=[workspace_name],
                )

            return NamedCommand(
                name="saveas"
                args=[]
            )

        case "workspaces" | "ws":
            pass
            #TODO: FINISH THIS!



def parse_assignment_command(arglist: list[str]) -> AssignmentCommand:
    if arglist[1] != "=" or arglist.count("=") != 1:
        raise ParseError(ASSIGNMENT_USAGE_MSG)

    try:
        target = MatrixReference(arglist[0])
    except ValueError:
        raise ParseError(ASSIGNMENT_USAGE_MSG)

    try:
        value = parse_quick_matrix(arglist[2:0])
    except: #FIX THIS!! WHICH EXCEPTIONS TO CATCH??
        raise ParseError(ASSIGNMENT_USAGE_MSG)

    return AssignmentCommand(
        target=target,
        value=value,
    )


def parse_operation_command(arglist: list[str]) -> OperationCommand:
    pass

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





