from typing import TYPE_CHECKING

from ....types import ColumnNode
from ....types.sensitivity import Sensitivity
from ....types.validation.threshold import Threshold
from ....types.validation.validation_rule import ColumnValidationRule

if TYPE_CHECKING:
    from ....ref import ColumnRef
    from .._base import BaseCheck


def create_validation_rule(
    check_method_id: str,
    message: str,
    *,
    source_column: str,
    alias: str,
    schema: str,
    thresholds: Threshold | None,
) -> ColumnValidationRule | None:
    """Create a validation rule for a check"""
    if not thresholds:
        return None

    return ColumnValidationRule(
        check_id=check_method_id,
        message=message,
        thresholds=thresholds,
        source_column=source_column,
        check_column=alias,
        schema=schema,
    )


def get_validation_node(
    check: "BaseCheck",
    *,
    source_column: "ColumnRef",
) -> ColumnNode:
    """Create a validation node for a check"""
    params = check.params
    label = params.label if params.label else check.method_id()
    _ref = source_column.clean() if params.check_on_cleaned else source_column

    alias = params.alias if params.alias else _ref.check(label).name

    assert alias != source_column.name, (
        f"Check column name must be different from column - {source_column.name}"
    )
    assert alias != _ref.name, (
        f"Check column name must be different from cleaned column - {_ref.name}"
    )

    expr = check.expression(
        _ref.name,
        alias,
        fail_value="reject" if params.remove_row_on_fail else "fail",
    )
    validation_rule = create_validation_rule(
        check_method_id=check.method_id(),
        message=params.message,
        source_column=source_column.name,
        alias=alias,
        schema=source_column.schema,
        thresholds=params.thresholds,
    )

    return ColumnNode(
        id=_ref.check(label).id,
        name=alias,
        data_type="boolean",
        column_type="validation",
        schema=source_column.schema,
        stage=source_column.stage,
        sensitivity=Sensitivity.NON_SENSITIVE,
        expression=expr,
        validation_rule=validation_rule,
    )
