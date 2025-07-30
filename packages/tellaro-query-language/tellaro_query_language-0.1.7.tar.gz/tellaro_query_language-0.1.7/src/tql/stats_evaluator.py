"""Stats evaluator for TQL aggregation queries.

This module provides the TQLStatsEvaluator class for executing statistical
aggregation queries against data records in memory.
"""

import statistics
from collections import defaultdict
from typing import Any, Dict, List, Optional, Union

from .exceptions import TQLError


class TQLStatsEvaluator:
    """Evaluates TQL stats queries against data records.

    This class handles statistical aggregations, grouping, and produces
    results in a UI-friendly format.
    """

    # Aggregation functions that require numeric fields
    NUMERIC_AGGREGATIONS = {
        "sum",
        "min",
        "max",
        "average",
        "avg",
        "median",
        "med",
        "std",
        "standard_deviation",
        "percentile",
        "percentiles",
        "p",
        "pct",
        "percentile_rank",
        "percentile_ranks",
        "pct_rank",
        "pct_ranks",
    }

    # Aggregation functions that work with any field type
    ANY_TYPE_AGGREGATIONS = {"count", "unique_count", "values", "unique", "cardinality"}

    # Numeric types supported by OpenSearch
    NUMERIC_TYPES = {
        "long",
        "integer",
        "short",
        "byte",
        "double",
        "float",
        "half_float",
        "scaled_float",
        "unsigned_long",
    }

    def __init__(self):
        """Initialize the stats evaluator."""

    def evaluate_stats(
        self, records: List[Dict[str, Any]], stats_ast: Dict[str, Any], field_mappings: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Evaluate stats query against records.

        Args:
            records: List of records to aggregate
            stats_ast: Stats AST from parser
            field_mappings: Optional field type mappings

        Returns:
            Aggregated results in UI-friendly format
        """
        aggregations = stats_ast.get("aggregations", [])
        group_by_fields = stats_ast.get("group_by", [])

        # Validate aggregation types against field mappings if provided
        if field_mappings:
            self._validate_aggregations(aggregations, field_mappings)

        if not group_by_fields:
            # Simple aggregation without grouping
            return self._simple_aggregation(records, aggregations)
        else:
            # Grouped aggregation
            return self._grouped_aggregation(records, aggregations, group_by_fields)

    def _validate_aggregations(self, aggregations: List[Dict[str, Any]], field_mappings: Dict[str, str]) -> None:
        """Validate that aggregation functions are compatible with field types.

        Args:
            aggregations: List of aggregation specifications
            field_mappings: Field type mappings

        Raises:
            TQLError: If aggregation is incompatible with field type
        """
        for agg in aggregations:
            func = agg["function"]
            field = agg["field"]

            # Skip validation for count(*)
            if field == "*":
                continue

            # Check if function requires numeric type
            if func in self.NUMERIC_AGGREGATIONS:
                field_type = field_mappings.get(field, "unknown")

                if field_type not in self.NUMERIC_TYPES and field_type != "unknown":
                    raise TQLError(
                        f"Cannot perform {func}() on non-numeric field '{field}' (type: {field_type}). "
                        f"Use count() or unique_count() for non-numeric fields, or ensure '{field}' "
                        f"is mapped as a numeric type."
                    )

    def _simple_aggregation(self, records: List[Dict[str, Any]], aggregations: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform aggregation without grouping.

        Args:
            records: Records to aggregate
            aggregations: Aggregation specifications

        Returns:
            Aggregated results
        """
        if len(aggregations) == 1:
            # Single aggregation
            agg = aggregations[0]
            value = self._calculate_aggregation(records, agg)

            return {
                "type": "simple_aggregation",
                "function": agg["function"],
                "field": agg["field"],
                "alias": agg.get("alias"),
                "value": value,
            }
        else:
            # Multiple aggregations
            results = {}
            for agg in aggregations:
                value = self._calculate_aggregation(records, agg)
                key = agg.get("alias") or f"{agg['function']}_{agg['field']}"
                results[key] = value

            return {"type": "multiple_aggregations", "results": results}

    def _grouped_aggregation(
        self, records: List[Dict[str, Any]], aggregations: List[Dict[str, Any]], group_by_fields: List[str]
    ) -> Dict[str, Any]:
        """Perform aggregation with grouping.

        Args:
            records: Records to aggregate
            aggregations: Aggregation specifications
            group_by_fields: Fields to group by

        Returns:
            Grouped aggregation results
        """
        # Group records
        groups = defaultdict(list)
        for record in records:
            # Build group key
            key_parts = []
            for field in group_by_fields:
                value = self._get_field_value(record, field)
                key_parts.append((field, value))
            key = tuple(key_parts)
            groups[key].append(record)

        # Calculate aggregations for each group
        results = []
        for key, group_records in groups.items():
            group_result: Dict[str, Any] = {"key": dict(key), "doc_count": len(group_records)}

            if len(aggregations) == 1:
                # Single aggregation
                agg = aggregations[0]
                value = self._calculate_aggregation(group_records, agg)
                agg_key = agg.get("alias") or agg["function"]
                group_result[agg_key] = value
            else:
                # Multiple aggregations
                group_result["aggregations"] = {}
                for agg in aggregations:
                    value = self._calculate_aggregation(group_records, agg)
                    agg_key = agg.get("alias") or f"{agg['function']}_{agg['field']}"
                    group_result["aggregations"][agg_key] = value

            results.append(group_result)

        # Apply modifiers (top/bottom)
        results = self._apply_modifiers(results, aggregations)

        return {"type": "grouped_aggregation", "group_by": group_by_fields, "results": results}

    def _calculate_aggregation(  # noqa: C901
        self, records: List[Dict[str, Any]], agg_spec: Dict[str, Any]
    ) -> Union[int, float, Dict[str, Any], None]:
        """Calculate a single aggregation value.

        Args:
            records: Records to aggregate
            agg_spec: Aggregation specification

        Returns:
            Aggregated value
        """
        func = agg_spec["function"]
        field = agg_spec["field"]

        # Handle count(*)
        if func == "count" and field == "*":
            return len(records)

        # Extract field values
        values = []
        for record in records:
            value = self._get_field_value(record, field)
            if value is not None:
                values.append(value)

        # Calculate aggregation
        if func == "count":
            return len(values)
        elif func == "unique_count":
            return len(set(values))
        elif func == "sum":
            return sum(self._to_numeric(v) for v in values) if values else 0
        elif func == "min":
            return min(self._to_numeric(v) for v in values) if values else None
        elif func == "max":
            return max(self._to_numeric(v) for v in values) if values else None
        elif func in ["average", "avg"]:
            if not values:
                return None
            numeric_values = [self._to_numeric(v) for v in values]
            return statistics.mean(numeric_values)
        elif func in ["median", "med"]:
            if not values:
                return None
            numeric_values = [self._to_numeric(v) for v in values]
            return statistics.median(numeric_values)
        elif func in ["std", "standard_deviation"]:
            if len(values) < 2:
                return None
            numeric_values = [self._to_numeric(v) for v in values]
            return statistics.stdev(numeric_values)
        elif func in ["percentile", "percentiles", "p", "pct"]:
            if not values:
                return None
            numeric_values = sorted([self._to_numeric(v) for v in values])
            percentile_values = agg_spec.get("percentile_values", [50])  # Default to median

            if len(percentile_values) == 1:
                # Single percentile
                return self._calculate_percentile(numeric_values, percentile_values[0])
            else:
                # Multiple percentiles - return dict
                result = {}
                for p in percentile_values:
                    result[f"p{int(p)}"] = self._calculate_percentile(numeric_values, p)
                return result
        elif func in ["percentile_rank", "percentile_ranks", "pct_rank", "pct_ranks"]:
            if not values:
                return None
            numeric_values = sorted([self._to_numeric(v) for v in values])
            rank_values = agg_spec.get("rank_values", [])

            if not rank_values:
                raise TQLError("percentile_rank requires at least one value")

            if len(rank_values) == 1:
                # Single rank value
                return self._calculate_percentile_rank(numeric_values, rank_values[0])
            else:
                # Multiple rank values - return dict
                result = {}
                for v in rank_values:
                    result[f"rank_{v}"] = self._calculate_percentile_rank(numeric_values, v)
                return result
        elif func in ["values", "unique", "cardinality"]:
            # Return unique values from the field
            unique_values = list(set(values)) if values else []
            # Sort the values for consistent output
            try:
                # Try to sort if values are comparable
                unique_values.sort()
            except TypeError:
                # If values aren't comparable (mixed types), just return unsorted
                pass
            return unique_values
        else:
            raise TQLError(f"Unsupported aggregation function: {func}")

    def _apply_modifiers(
        self, results: List[Dict[str, Any]], aggregations: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Apply top/bottom modifiers to results.

        Args:
            results: Aggregation results
            aggregations: Aggregation specifications with modifiers

        Returns:
            Modified results
        """
        # Check if any aggregation has modifiers
        for agg in aggregations:
            if "modifier" in agg:
                # Sort results based on the aggregation value
                agg_key = agg.get("alias") or agg["function"]

                # Get the value from the result
                def get_sort_value(result, key=agg_key):
                    if "aggregations" in result:
                        return result["aggregations"].get(key, 0)
                    else:
                        return result.get(key, 0)

                # Sort
                reverse = agg["modifier"] == "top"
                results = sorted(results, key=get_sort_value, reverse=reverse)

                # Limit
                limit = agg.get("limit", 10)
                results = results[:limit]

                break  # Only apply first modifier found

        return results

    def _get_field_value(self, record: Dict[str, Any], field_path: str) -> Any:
        """Get a field value from a record, supporting nested fields.

        Args:
            record: The record dictionary
            field_path: Dot-separated field path

        Returns:
            The field value or None if not found
        """
        parts = field_path.split(".")
        current = record

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def _to_numeric(self, value: Any) -> Union[int, float]:
        """Convert value to numeric type.

        Args:
            value: Value to convert

        Returns:
            Numeric value

        Raises:
            TQLError: If value cannot be converted
        """
        if isinstance(value, (int, float)):
            return value

        if isinstance(value, str):
            try:
                # Try int first
                if "." not in value:
                    return int(value)
                else:
                    return float(value)
            except ValueError:
                raise TQLError(
                    f"Cannot convert '{value}' to numeric value. " f"Ensure the field contains numeric data."
                )

        raise TQLError(
            f"Cannot convert {type(value).__name__} to numeric value. " f"Ensure the field contains numeric data."
        )

    def _calculate_percentile(self, sorted_values: List[Union[int, float]], percentile: float) -> Optional[float]:
        """Calculate the percentile value for a sorted list of values.

        Args:
            sorted_values: Sorted list of numeric values
            percentile: Percentile to calculate (0-100)

        Returns:
            The percentile value
        """
        if not sorted_values:
            return None

        if percentile < 0 or percentile > 100:
            raise TQLError(f"Percentile must be between 0 and 100, got {percentile}")

        n = len(sorted_values)
        if n == 1:
            return sorted_values[0]

        # Calculate the position using linear interpolation
        pos = (n - 1) * (percentile / 100.0)
        lower_idx = int(pos)
        upper_idx = min(lower_idx + 1, n - 1)

        if lower_idx == upper_idx:
            return sorted_values[lower_idx]

        # Linear interpolation between two values
        lower_value = sorted_values[lower_idx]
        upper_value = sorted_values[upper_idx]
        fraction = pos - lower_idx

        return lower_value + fraction * (upper_value - lower_value)

    def _calculate_percentile_rank(self, sorted_values: List[Union[int, float]], value: float) -> Optional[float]:
        """Calculate the percentile rank of a value within a sorted list.

        Args:
            sorted_values: Sorted list of numeric values
            value: Value to find percentile rank for

        Returns:
            The percentile rank (0-100)
        """
        if not sorted_values:
            return None

        n = len(sorted_values)

        # Count how many values are less than the target value
        count_less = 0
        count_equal = 0

        for v in sorted_values:
            if v < value:
                count_less += 1
            elif v == value:
                count_equal += 1

        # Calculate percentile rank
        # If value is in the list, use midpoint of its range
        if count_equal > 0:
            rank = (count_less + count_equal / 2.0) / n * 100
        else:
            # Value not in list, interpolate
            rank = count_less / n * 100

        return round(rank, 2)
