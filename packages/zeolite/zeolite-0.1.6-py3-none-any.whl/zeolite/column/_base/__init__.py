# %%
from dataclasses import dataclass, field, KW_ONLY, fields, replace
from typing import Any, List, Literal, Optional
from polars import Expr, Float64, DataType

from ..._utils.data_type import get_polars_type, get_data_type_label
from ...ref import ColumnRef
from ...types import ColumnNode, CoerceOption
from ...types.sensitivity import Sensitivity
from ...types.data_type import ColumnDataType, ColumnDataTypeLabel
from ...types.validation.threshold import CheckLevel, ThresholdLevel
from ..._utils.args import flatten_args
from .._clean import (
    CleanStage,
    Clean,
    CleanColumn,
)
from ..validation import (
    ColumnCheckType,
    BaseCheck,
    ThresholdType,
    create_validation_rule,
)

# %%

type _RequiredLevel = CheckLevel | bool | None


@dataclass(frozen=True)
class _ColumnParams:
    ref: ColumnRef
    _: KW_ONLY
    type_label: str = field(default="unknown")
    dtype: Optional[DataType] = field(default=None)
    coerce: CoerceOption = field(default="default")
    sensitivity: Sensitivity = field(default=Sensitivity.UNKNOWN)
    aliases: set[str] = field(default_factory=set)
    if_missing: ThresholdLevel = field(default=ThresholdLevel.REJECT)
    validations: List[ColumnCheckType] = field(default_factory=list)
    clean: Optional[CleanStage] = field(default=None)
    expression: Optional[Expr] = field(default=None)
    custom_validation: dict[str, str | ThresholdType] | None = field(default=None)


def _verify_validations(validations: List[ColumnCheckType] | None):
    if validations is not None:
        for v in validations:
            assert isinstance(v, BaseCheck), (
                f"Expected {v} to be a Column Validation Check"
            )


class ColumnSchema:
    """
    Defines a column in a table schema, including data type, sensitivity, validations, and cleaning steps.

    Parameters:
        col_ref (ColumnRef): Reference to the column.
        data_type (ColumnDataType): Data type of the column.
        sensitivity (Sensitivity): Sensitivity level.
        aliases (set[str]): Aliases for the column.
        validations (List[ColumnCheckType]): Validation checks.
        clean (CleanStage | ...): Cleaning stage or type.
    """

    def __init__(
        self,
        col_ref: ColumnRef,
        *,
        data_type: ColumnDataType = "unknown",
        coerce: CoerceOption = "default",
        sensitivity: Sensitivity = None,
        aliases: set[str] = None,
        optional: CheckLevel | bool = False,
        validations: List[ColumnCheckType] = None,
        clean: CleanStage | ColumnDataType | dict[str, Any] | None = None,
    ):
        _verify_validations(validations)
        if clean is not None:
            if isinstance(clean, CleanColumn):
                pass
            elif isinstance(clean, str):
                clean = self._get_clean_stage(clean)
            elif isinstance(clean, dict):
                clean = self._get_clean_stage(**clean)
            else:
                clean = None

        if isinstance(optional, bool):
            optional: CheckLevel = "pass" if optional else "reject"

        self._params = _ColumnParams(
            ref=col_ref,
            type_label=get_data_type_label(data_type),
            dtype=get_polars_type(data_type),
            coerce=coerce,
            sensitivity=sensitivity if sensitivity is not None else Sensitivity.UNKNOWN,
            aliases=aliases if aliases is not None else set(),
            validations=validations if validations is not None else [],
            clean=clean,
            if_missing=_get_missing_level(optional),
        )

    def sensitivity(self, sensitivity: Sensitivity) -> "ColumnSchema":
        return self._replace(sensitivity=sensitivity)

    def data_type(
        self, data_type: ColumnDataType, *, coerce: CoerceOption = "default"
    ) -> "ColumnSchema":
        return self._replace(
            type_label=get_data_type_label(data_type),
            dtype=get_polars_type(data_type),
            coerce=coerce,
        )

    def aliases(self, *args: str | list[str], merge: bool = False) -> "ColumnSchema":
        aliases = set(flatten_args(args))
        if merge:
            aliases = aliases | self._params.aliases
        return self._replace(aliases=aliases)

    def validations(
        self, *args: ColumnCheckType | list[ColumnCheckType], merge: bool = False
    ) -> "ColumnSchema":
        validations = flatten_args(args)
        _verify_validations(validations)
        if merge:
            validations = validations + self._params.validations

        return self._replace(validations=validations)

    def clean(self, to: ColumnDataType | CleanStage, **kwargs: Any) -> "ColumnSchema":
        return self._replace(clean=self._get_clean_stage(to, **kwargs))

    def optional(self, optional: bool | CheckLevel = True) -> "ColumnSchema":
        if isinstance(optional, bool):
            optional: CheckLevel = "pass" if optional else "reject"

        return self._replace(if_missing=_get_missing_level(optional))

    def get_nodes(self, schema: str, stage: str | None = None) -> List[ColumnNode]:
        p = self._params
        ref = p.ref.with_schema(schema, stage)

        column_type = _get_col_type(ref)
        validation_rule = (
            create_validation_rule(
                check_method_id="custom_validation",
                message=p.custom_validation["message"],
                source_column=", ".join(p.expression.meta.root_names()),
                alias=ref.name,
                schema=ref.schema,
                thresholds=p.custom_validation["thresholds"],
            )
            if ref.is_custom_check
            else None
        )

        nodes: list[ColumnNode] = [
            ColumnNode(
                id=ref.id,
                name=ref.name,
                data_type=p.type_label,
                column_type=column_type,
                schema=ref.schema,
                stage=ref.stage,
                sensitivity=p.sensitivity,
                expression=self.expr,
                validation_rule=validation_rule,
            )
        ]
        if p.clean is not None:
            clean_expr = p.clean.clean_expr(ref)
            nodes.append(
                ColumnNode(
                    id=ref.clean().id,
                    name=clean_expr.meta.output_name(),
                    data_type=get_data_type_label(p.clean.data_type),
                    column_type="cleaned",
                    schema=ref.schema,
                    stage=ref.stage,
                    sensitivity=p.clean.col_sensitivity
                    if p.clean.col_sensitivity is not None
                    else p.sensitivity,
                    expression=clean_expr,
                    validation_rule=None,
                )
            )
        for v in p.validations:
            nodes.append(v.get_validation_node(ref))

        return nodes

    @property
    def ref(self) -> ColumnRef:
        """Get the name of the column reference"""
        return self._params.ref

    @property
    def get_aliases(self) -> set[str]:
        """Get the aliases of the column reference"""
        return self._params.aliases

    @property
    def if_missing(self) -> ThresholdLevel:
        """Get the threshold level for the column if missing"""
        return self._params.if_missing

    @property
    def has_expression(self) -> bool:
        """Check if the column is/has an expression"""
        return self._params.expression is not None

    @property
    def coerce(self) -> CoerceOption | None:
        """Check if the column should be coerced to the data type"""
        return self._params.coerce

    @property
    def dtype(self) -> DataType:
        """Returns the polars data type"""
        return self._params.dtype

    @property
    def expr(self) -> Expr | None:
        return (
            self._params.expression.alias(self._params.ref.name)
            if self.has_expression
            else None
        )

    def with_name(self, name: str):
        return self._replace(ref=self._params.ref.with_base_name(name))

    def derived(self, expr: Expr) -> "ColumnSchema":
        return self._replace(ref=self._params.ref.derived(), expression=expr)

    def custom_check(
        self, expr: Expr, thresholds: ThresholdType, message: str
    ) -> "ColumnSchema":
        return self._replace(
            ref=self._params.ref.custom_check(),
            expression=expr,
            custom_validation={"message": message, "thresholds": thresholds},
        )

    def _get_clean_stage(
        self, to: ColumnDataTypeLabel | CleanStage, **kwargs: dict[str, Any]
    ) -> CleanStage:
        # TODO: figure out a cleaner (ha) way to do determine clean stage based on data type
        # FIXME: figure out if it's possible to have dynamic typed kwargs based on the data type

        if to is None:
            raise ValueError("'to' cannot be None for cleaning stage")

        if isinstance(to, CleanColumn):
            return to
        elif to == "string":
            return Clean.string(**kwargs)
        elif to == "sanitised_string":
            return Clean.string(
                **kwargs,
                sanitize=kwargs["sanitize"] if "sanitize" in kwargs else "full",
            )
        elif to == "number":
            return Clean.number(**kwargs)
        elif to == "integer":
            return Clean.int(**kwargs)
        elif to == "decimal":
            return Clean.decimal(**kwargs)
        elif to == "float":
            return Clean.float(
                output_format=Float64,
                data_type="float",
                **kwargs,
            )
        elif to == "boolean":
            return Clean.boolean(**kwargs)
        elif to == "date":
            return Clean.date(**kwargs)
        elif to == "datetime":
            return Clean.datetime(**kwargs)
        elif to == "enum":
            return Clean.enum(**kwargs)
        elif to == "id":
            return Clean.id(**kwargs)

        # TODO: implement custom clean stage
        # elif to == "custom":
        # return CleanCustomColumn(**kwargs)
        else:
            raise ValueError(f"Unimplemented clean stage: {to}")

    def _replace(self, **kwargs):
        new_params = replace(self._params, **kwargs)
        # initiate an empty column reference & manually apply the new params
        # we do it this way to set properties not allowed in the constructor
        return ColumnSchema(col_ref=new_params.ref).__set_params(new_params)

    def __set_params(self, params: _ColumnParams) -> "ColumnSchema":
        self._params = params
        return self

    def __repr__(self):
        """Return a string representation of the instance."""
        param_strs = []
        for field_name in [f.name for f in fields(_ColumnParams)]:
            value = getattr(self._params, field_name)
            if value is not None and (not isinstance(value, list) or value):
                param_strs.append(f"{field_name}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(param_strs)})"


# %%
def _get_col_type(
    ref: ColumnRef,
) -> Literal["source", "cleaned", "validation", "meta", "derived", "custom_validation"]:
    if ref.is_meta:
        return "meta"
    if ref.is_derived:
        return "custom_validation"
    elif ref.is_derived:
        return "derived"
    else:
        return "source"


def _get_missing_level(level: CheckLevel) -> ThresholdLevel:
    if level == "debug":
        return ThresholdLevel.DEBUG
    elif level == "warning":
        return ThresholdLevel.WARNING
    elif level == "error":
        return ThresholdLevel.ERROR
    elif level == "reject":
        return ThresholdLevel.REJECT
    else:
        return ThresholdLevel.PASS


# %%
