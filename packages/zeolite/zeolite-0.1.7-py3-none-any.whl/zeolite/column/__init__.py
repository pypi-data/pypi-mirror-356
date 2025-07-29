from dataclasses import field
from typing import List, Any

from polars import Expr, lit

from ..ref import ColumnRef
from ..types import ThresholdLevel, CoerceOption
from ..types.data_type import ColumnDataType
from ..types.sensitivity import Sensitivity
from ._base import ColumnSchema
from ._clean import CleanStage, Clean
from .validation import ColumnCheckType, ThresholdType

__all__ = [
    "col",
    "column",
    "ColumnSchema",
    "str_col",
    "bool_col",
    "date_col",
    "int_col",
    "float_col",
    "derived_col",
    "derived_custom_check",
    "meta_col",
    "Clean",
]


# -----------------------------------------------------------------------------------------------------------
# Column Definitions
# -----------------------------------------------------------------------------------------------------------
def _create_col(
    ref: ColumnRef,
    data_type: ColumnDataType = "unknown",
    sensitivity: Sensitivity = None,
    aliases: set[str] = None,
    coerce: CoerceOption = "default",
    validations: List[ColumnCheckType] = None,
    clean: CleanStage | ColumnDataType | dict[str, Any] | None = None,
) -> ColumnSchema:
    return ColumnSchema(
        col_ref=ref,
        data_type=data_type,
        coerce=coerce,
        sensitivity=sensitivity,
        aliases=aliases,
        validations=validations,
        clean=clean,
    )


class Col:
    data_type: ColumnDataType

    def __init__(self, data_type: ColumnDataType = "unknown"):
        self.data_type = data_type

    def __call__(
        self,
        name: str | None = None,
        *,
        data_type: ColumnDataType | None = None,
        sensitivity: Sensitivity = None,
        aliases: set[str] = None,
        coerce: CoerceOption = "default",
        validations: List[ColumnCheckType] = None,
        clean: CleanStage | ColumnDataType | dict[str, Any] | None = None,
    ) -> ColumnSchema:
        """
        Define a new column.

        Parameters:
            name: Name of the column.
            data_type: Data type of the column.
            sensitivity: Sensitivity of the column.
            aliases: Aliases for the column.
            validations: List of validation checks.
            clean: Clean stage for the column.

        Returns:
            ColumnSchema: The column schema.
        """
        return _create_col(
            ref=ColumnRef(name),
            data_type=data_type or self.data_type,
            coerce=coerce,
            sensitivity=sensitivity,
            aliases=aliases,
            validations=validations,
            clean=clean,
        )

    def __getattr__(self, name: str) -> ColumnSchema:
        # For autocomplete to work with IPython
        if name.startswith("__wrapped__"):
            return getattr(type(self), name)

        return _create_col(ColumnRef(name))


column: Col = Col()
col: Col = Col()
"""
Define a new column.
Example:
    zeolite.col("id").validations(zeolite.check_is_value_empty(), ...)

Parameters:
    name: Name of the column.
    data_type: Data type of the column.
    sensitivity: Sensitivity of the column.
    aliases: Aliases for the column.
    validations: List of validation checks.
    clean: Clean stage for the column.

Returns:
    ColumnSchema: The column schema.
"""


# -----------------------------------------------------------------------------------------------------------
# Data-Type Specific Column Definitions
# -----------------------------------------------------------------------------------------------------------

str_col = Col("string")
"""
Helper to define a new string column.
"""

bool_col = Col("boolean")
"""
Helper to define a new boolean column.
"""

date_col = Col("date")
"""
Helper to define a new date column.
"""

int_col = Col("integer")
"""
Helper to define a new integer column.
"""


float_col = Col("float")
"""
Helper to define a new float column.
"""


# -----------------------------------------------------------------------------------------------------------
# Derived Column Definitions
# -----------------------------------------------------------------------------------------------------------
class DerivedCol:
    def __call__(
        self,
        name: str | None = None,
        *,
        function: Expr,
        data_type: ColumnDataType = "unknown",
        sensitivity: Sensitivity = None,
        validations: List[ColumnCheckType] = None,
    ) -> ColumnSchema:
        """
        Define a derived column whose value is computed from an expression.

        Parameters:
            name: Name of the derived column.
            function: Polars expression to compute the column.
            data_type: (Optional) Data type of the column.
            sensitivity: (Optional) Sensitivity of the column.
            validations: (Optional) List of validation checks.

        Returns:
            ColumnSchema: The derived column schema.
        """
        return _create_col(
            ref=ColumnRef(name).derived(),
            data_type=data_type,
            sensitivity=sensitivity,
            validations=validations,
        ).derived(function)

    def __getattr__(self, name: str) -> ColumnSchema:
        # For autocomplete to work with IPython
        if name.startswith("__wrapped__"):
            return getattr(type(self), name)

        # We add a literal to the expression to ensure that the derived column has an expression
        return _create_col(ColumnRef(name).derived()).derived(lit(name))


derived_col: DerivedCol = DerivedCol()
"""
Define a derived column whose value is computed from an expression.

Parameters:
    name: Name of the derived column.
    function: Polars expression to compute the column.
    data_type: (Optional) Data type of the column.
    sensitivity: (Optional) Sensitivity of the column.
    validations: (Optional) List of validation checks.

Returns:
    ColumnSchema: The derived column schema.
"""


class DerivedCustomCheckCol:
    def __call__(
        self,
        name: str | None = None,
        *,
        function: Expr,
        sensitivity: Sensitivity = Sensitivity.NON_SENSITIVE,
        thresholds: ThresholdType = None,
        message: str = field(default=""),
    ) -> ColumnSchema:
        """
        Define a derived custom check/validation that is computed from an expression.

        Parameters:
            name: Name of the derived validation.
            function: Polars expression to compute the validation.
            sensitivity: (Optional) Sensitivity of the validation.
            thresholds: (Optional) Thresholds for the validation.
            message: (Optional) Message for the validation.

        Returns:
            ColumnSchema: The derived validation schema.
        """
        return _create_col(
            ref=ColumnRef(name).custom_check(),
            data_type="boolean",
            sensitivity=sensitivity,
        ).custom_check(function, thresholds, message)

    def __getattr__(self, name: str) -> ColumnSchema:
        # For autocomplete to work with IPython
        if name.startswith("__wrapped__"):
            return getattr(type(self), name)

        # We add a pass default to ensure that the custom_check has an expression
        return _create_col(ColumnRef(name).custom_check()).custom_check(
            lit(ThresholdLevel.PASS.level), None, "Not implemented"
        )


derived_custom_check: DerivedCustomCheckCol = DerivedCustomCheckCol()
"""
Define a derived custom check/validation that is computed from an expression.

Parameters:
   name: Name of the derived validation.
   function: Polars expression to compute the validation.
   sensitivity: (Optional) Sensitivity of the validation.
   thresholds: (Optional) Thresholds for the validation.
   message: (Optional) Message for the validation.

Returns:
   ColumnSchema: The derived validation schema.
"""


class MetaCol:
    def __call__(
        self,
        name: str | None = None,
        *,
        function: Expr = None,
        data_type: ColumnDataType = "unknown",
        sensitivity: Sensitivity = None,
    ) -> ColumnSchema:
        """
        Define a meta column - this is a special column that is usually added
        to the data e.g. during initial ingestion, and should be identified as
        separate from the source data.

        Parameters:
            name: Name of the meta column.
            function: (Optional) Polars expression to compute the column.
            data_type: (Optional) Data type of the column.
            sensitivity: (Optional) Sensitivity of the column.

        Returns:
            ColumnSchema: The meta column schema.
        """
        m_col = _create_col(
            ref=ColumnRef(name, is_meta=True),
            data_type=data_type,
            sensitivity=sensitivity,
        )
        return m_col.derived(function) if function is not None else m_col

    def __getattr__(self, name: str) -> ColumnSchema:
        # For autocomplete to work with IPython
        if name.startswith("__wrapped__"):
            return getattr(type(self), name)

        return _create_col(ColumnRef(name, is_meta=True))


meta_col: MetaCol = MetaCol()
"""
Define a meta column - this is a special column that is usually added
to the data e.g. during initial ingestion, and should be identified as
separate from the source data.

Parameters:
    name: Name of the meta column.
    function: (Optional) Polars expression to compute the column.
    data_type: (Optional) Data type of the column.
    sensitivity: (Optional) Sensitivity of the column.

Returns:
    ColumnSchema: The meta column schema.
"""
