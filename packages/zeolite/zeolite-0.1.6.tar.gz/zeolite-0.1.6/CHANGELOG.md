# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### What's Changed

- Changes in existing functionality

### Deprecated

- Soon-to-be removed features

### Removed

- Now removed features

### Fixed

- Any bug fixes

### Security

- In case of vulnerabilities

## [0.1.6] - 2025-06-18

### What's Changed
- 🧼 cleaning functions are now defined under the `z.Clean` namespace (e.g. `z.Clean.date()`)
- 🏷️ `NO_DATA` and `INVALID_DATA` values used in cleaning steps are now exported (to help with custom logic)
- 💎 added `z.Check.custom(...)` check

## [0.1.5] - 2025-06-10

### What's Changed
- 💎 column checks are now defined under the `z.Check` namespace (e.g. `z.Check.not_null()`)
- 💎 a number of new checks have been added:
  - `equal_to` - check if the column (exactly) equal a given value
  - `not_equal_to` - check if the column (exactly) does not equal a given value
  - `is_in` - check if the column is in a given list of values
  - `not_in` - check if the column is not in a given list of values
  - `less_than` - check if the column is less than a given number
  - `less_than_or_equal` - check if the column is less than or equal to a given number
  - `greater_than` - check if the column is greater than a given number
  - `greater_than_or_equal` - check if the column is greater than or equal to a given number
  - `between` - check if the column is between a given range of numbers
  - `str_matches` - check if the column matches a given string pattern
  - `str_not_matches` - check if the column does not match a given string pattern
  - `str_length` - check length of strings in the column length are less than/greater than/between given values
- 💎 columns are now `required` by default with `optional` flag (fixes #21)
- 💎 previously if a row/value check failed, the value was based on the max threshold level. Now it is only based on `remove_row_on_fail` option (fixes #19)
- ⚡ added support for DataFrames in addition to LazyFrames
- ⚗️ added a coercian stage between normalise & prep to handle casting/conversion to the expected column data types (fixes #1 and #5)
- 🧼 added decimal variant to cleaning stages


## [0.1.4] - 2025-05-21

### What's Changed

- ⚗️ updated schema to support defining columns with a dictionary or kwargs (fixes #4)
- 🧼 updated `CleanEnumColumn` to handle null and invalid value (fixes #16 and #17)
- 🐛 updated `TableSchema.process_data` to not return validated lazyframe when validate stage fails (fixes #15)
- ⚗️ updated `ref` & `col` constructors to allows definitions using both a call pattern ( `z.col("demo")` ) and as a
  direct attribute ( `z.col.demo` )
- 🔧 added `parse_column_name` function to parse a column name into a `ColumnRef`

## [0.1.3] - 2025-05-15

### What's Changed

- ⚗️ removed `with_stage` from TableSchema (introduced on 0.1.2) - stage should not be changed after initialisation
- ♻️ refactored to support better public submodule exports - `zeolite.ref` and `zeolite.types` are now public
- 🧼 added alias for `float`/`decimal`/`integer` cleaning

## [0.1.2] - 2025-05-14

### What's Changed

- 🐛 fixed bug with extract_base_name not handling prefixes properly
- ⚗️ added `name`, `is_required`, `stage` getter props to TableSchema
- ⚗️ added `required` and `with_stage` setter functions to TableSchema
- 💎 added debug error level to validation thresholds Linden

## [0.1.1] - 2025-05-13

### What's Changed

- ⚗️ updated normalisation to sanitise both the data source columns and the alias columns from the schema to make sure
  the match is clean. This also lets us go straight from source -> sanitised in one rename step
- ⚗️ updated TableSchema to check for alias conflicts
- 🔧 updated sanitisation functions with better edge case handling

## [0.1.0] - 2025-05-06

### What's Changed

- 🎉 Initial release of Zeolite!
- ⚗️ Added `schema`/`TableSchema` and `col`/`ColumnSchema` structs to capture table/column definitions and undertake
  processing/validation of datasets
- 💎 Added validation check functions for `check_is_value_empty`, `check_is_value_duplicated`,
  `check_is_value_invalid_date` and `check_is_value_equal_to`
- 🗃️ Added internal `ColumnRegistry` to manage column definitions, lineage, etc
- 🔧 Added `ref`/`ColumnRef` helper to create name/id references to other columns

[Unreleased]: https://github.com/username/zeolite/compare/v0.1.0...HEAD

[0.1.0]: https://github.com/username/zeolite/releases/tag/v0.1.0 