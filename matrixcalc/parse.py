import re
from matrixcalc.matrix import Matrix, MatrixCellValue
from matrixcalc.symlgc import Monomial, Polynomial
from dataclasses import dataclass

@dataclass
class Command:
    """A parsed CLI command."""

@dataclass
class NamedCommand(Command):
    name: str
    args: list[object]

@dataclass
class OperationCommand(Command):
    op

def parse(line: str) -> list ?????:
