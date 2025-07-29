from dataclasses import dataclass, field, replace
from typing import Optional, Literal
from polars import Expr, LazyFrame, DataType

from .data_type import ColumnDataType
from .sensitivity import Sensitivity
from .validation.threshold import ThresholdLevel
from .validation.validation_rule import ColumnValidationRule
from .error import (
    SchemaValidationError,
    FileValidationError,
    StructureValidationError,
    DataValidationError,
    UnknownValidationError,
)

__all__ = [
    "ColumnNode",
    "ColumnDataType",
    "CoerceOption",
    "SourceColDef",
    "ValidationResult",
    "ProcessingResult",
    "ProcessingFailure",
    "ProcessingSuccess",
    "SchemaValidationError",
    "FileValidationError",
    "StructureValidationError",
    "DataValidationError",
    "UnknownValidationError",
    "ThresholdLevel",
]


@dataclass(frozen=True)
class ColumnNode:
    id: str
    name: str
    data_type: str
    column_type: Literal[
        "source", "cleaned", "validation", "meta", "derived", "custom_validation"
    ]
    schema: str
    stage: str
    sensitivity: Sensitivity
    expression: Optional[Expr] = None
    validation_rule: Optional[ColumnValidationRule] = None
    parent_columns: frozenset[str] = field(default_factory=frozenset)
    parent_ids: frozenset[str] = field(default_factory=frozenset)

    def __post_init__(self):
        if self.expression is not None:
            assert self.name == self.expression.meta.output_name(), (
                f"Column name {self.name} does not match expression output name {self.expression.meta.output_name()}"
            )
            if len(self.parent_columns) == 0:
                object.__setattr__(
                    self,
                    "parent_columns",
                    frozenset({c for c in self.expression.meta.root_names()}),
                )

    def with_parent_ids(self, parent_ids: set[str]) -> "ColumnNode":
        return replace(self, parent_ids=frozenset(parent_ids))


type CoerceOption = Literal["strict", "default", "skip"]


@dataclass(frozen=True)
class SourceColDef:
    name: str
    aliases: set[str]
    if_missing: ThresholdLevel
    is_meta: bool
    dtype: DataType | None = None
    coerce: CoerceOption | None = None


# Validation Results
@dataclass(frozen=True)
class ValidationResult:
    data: LazyFrame
    errors: list[SchemaValidationError]
    reject: bool = False


@dataclass(frozen=True)
class ProcessingResult:
    normalised: LazyFrame | None
    prepared: LazyFrame | None
    coerced: LazyFrame | None
    validated: LazyFrame | None
    errors: list[SchemaValidationError]
    success: bool = False
    failed_stage: Literal["normalise", "coerce", "prepare", "validate"] | None = None


@dataclass(frozen=True)
class ProcessingFailure(ProcessingResult):
    success: False = False
    failed_stage: Literal["normalise", "coerce", "prepare", "validate"]


@dataclass(frozen=True)
class ProcessingSuccess(ProcessingResult):
    normalised: LazyFrame
    prepared: LazyFrame
    coerced: LazyFrame
    validated: LazyFrame
    success: True = True
    failed_stage: None = None
