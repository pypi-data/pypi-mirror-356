from dataclasses import dataclass

from zeolite.column._clean._variants import (
    CleanColumn,
    StringColumn,
    CleanEnumColumn,
    CleanDecimalColumn,
    CleanBooleanColumn,
    CleanDateColumn,
    CleanDatetimeColumn,
    CleanNumberColumn,
    CleanIntegerColumn,
    CleanIdColumn,
)


@dataclass(frozen=True)
class Clean:
    string = StringColumn
    number = CleanNumberColumn
    float = CleanNumberColumn
    int = CleanIntegerColumn
    integer = CleanIntegerColumn
    decimal = CleanDecimalColumn
    boolean = CleanBooleanColumn
    date = CleanDateColumn
    datetime = CleanDatetimeColumn
    id = CleanIdColumn
    enum = CleanEnumColumn


type CleanStage = (
    CleanColumn
    | StringColumn
    | CleanNumberColumn
    | CleanDecimalColumn
    | CleanBooleanColumn
    | CleanDateColumn
    | CleanEnumColumn
    | CleanIdColumn
)
__all__ = [
    "Clean",
    "CleanStage",
    "CleanColumn",
]
