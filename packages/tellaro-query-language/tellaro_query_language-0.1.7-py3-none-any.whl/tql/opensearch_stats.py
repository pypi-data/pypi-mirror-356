"""OpenSearch stats translator for TQL.

This module translates TQL stats queries to OpenSearch aggregation DSL.
"""

from typing import Any, Dict, List, Optional, Union

from .exceptions import TQLError


class OpenSearchStatsTranslator:
    """Translates TQL stats AST to OpenSearch aggregations."""

    # Map TQL aggregation functions to OpenSearch aggregation types
    AGGREGATION_MAPPING = {
        "count": "value_count",
        "unique_count": "cardinality",
        "sum": "sum",
        "min": "min",
        "max": "max",
        "average": "avg",
        "avg": "avg",
        "median": "percentiles",
        "med": "percentiles",
        "std": "extended_stats",  # Will extract std_deviation
        "standard_deviation": "extended_stats",
        "percentile": "percentiles",
        "percentiles": "percentiles",
        "p": "percentiles",
        "pct": "percentiles",
        "percentile_rank": "percentile_ranks",
        "percentile_ranks": "percentile_ranks",
        "pct_rank": "percentile_ranks",
        "pct_ranks": "percentile_ranks",
        "zscore": None,  # Requires post-processing
        "values": "terms",  # Return unique values
        "unique": "terms",  # Alias for values
        "cardinality": "cardinality",  # Count of unique values
    }

    # Aggregations that require numeric fields
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
        "zscore",
        "percentile",
        "percentiles",
        "p",
        "pct",
        "percentile_rank",
        "percentile_ranks",
        "pct_rank",
        "pct_ranks",
    }

    def translate_stats(
        self, stats_ast: Dict[str, Any], field_mappings: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Translate stats AST to OpenSearch aggregations.

        Args:
            stats_ast: Stats AST from parser
            field_mappings: Optional field type mappings

        Returns:
            OpenSearch aggregation DSL
        """
        aggregations = stats_ast.get("aggregations", [])
        group_by_fields = stats_ast.get("group_by", [])

        if not aggregations:
            raise TQLError("No aggregations specified in stats query")

        # Build OpenSearch aggregations
        aggs_dsl = {}

        if group_by_fields:
            # Build nested terms aggregations for grouping
            aggs_dsl = self._build_grouped_aggregations(aggregations, group_by_fields, field_mappings)
        else:
            # Simple aggregations without grouping
            aggs_dsl = self._build_simple_aggregations(aggregations, field_mappings)

        return {"aggs": aggs_dsl}

    def _build_simple_aggregations(  # noqa: C901
        self, aggregations: List[Dict[str, Any]], field_mappings: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Build simple aggregations without grouping.

        Args:
            aggregations: List of aggregation specifications
            field_mappings: Optional field mappings

        Returns:
            OpenSearch aggregations DSL
        """
        aggs_dsl: Dict[str, Any] = {}

        for i, agg in enumerate(aggregations):
            func = agg["function"]
            field = agg["field"]
            alias = agg.get("alias") or f"{func}_{field}_{i}"

            # Validate field type if mappings provided
            if field_mappings and func in self.NUMERIC_AGGREGATIONS and field != "*":
                self._validate_numeric_field(field, func, field_mappings)

            # Build aggregation based on function
            if func == "count" and field == "*":
                # Special case for count(*)
                aggs_dsl[alias] = {"value_count": {"field": "_id"}}
            elif func in self.AGGREGATION_MAPPING:
                os_agg_type = self.AGGREGATION_MAPPING[func]

                if os_agg_type is None:
                    # Functions that require post-processing
                    raise TQLError(
                        f"Aggregation function '{func}' requires post-processing",
                        suggestions=[
                            "This function is not directly supported by OpenSearch",
                            "Consider using a different function or processing results client-side",
                        ],
                    )

                # Build aggregation
                if func in ["median", "med"]:
                    # Median uses percentiles aggregation at 50th percentile
                    aggs_dsl[alias] = {"percentiles": {"field": field, "percents": ["50"]}}
                elif func in ["std", "standard_deviation"]:
                    # Standard deviation uses extended_stats
                    aggs_dsl[alias] = {"extended_stats": {"field": field}}
                elif func in ["percentile", "percentiles", "p", "pct"]:
                    # Percentiles aggregation with custom values
                    percentile_values = agg.get("percentile_values", [50])
                    # Convert to strings for OpenSearch
                    percents = [str(p) for p in percentile_values]
                    aggs_dsl[alias] = {"percentiles": {"field": field, "percents": percents}}
                elif func in ["percentile_rank", "percentile_ranks", "pct_rank", "pct_ranks"]:
                    # Percentile ranks aggregation
                    rank_values = agg.get("rank_values", [])
                    if not rank_values:
                        raise TQLError("percentile_rank requires at least one value")
                    aggs_dsl[alias] = {"percentile_ranks": {"field": field, "values": rank_values}}
                elif func in ["values", "unique"]:
                    # Terms aggregation to get unique values
                    aggs_dsl[alias] = {"terms": {"field": field, "size": 10000}}  # Large size to get all values
                else:
                    # Direct mapping
                    aggs_dsl[alias] = {os_agg_type: {"field": field}}
            else:
                raise TQLError(f"Unknown aggregation function: {func}")

        return aggs_dsl

    def _build_grouped_aggregations(
        self,
        aggregations: List[Dict[str, Any]],
        group_by_fields: List[str],
        field_mappings: Optional[Dict[str, str]] = None,
    ) -> Dict[str, Any]:
        """Build aggregations with grouping.

        Args:
            aggregations: List of aggregation specifications
            group_by_fields: Fields to group by
            field_mappings: Optional field mappings

        Returns:
            OpenSearch aggregations DSL with nested terms aggregations
        """
        # Start with the innermost aggregations
        inner_aggs = self._build_simple_aggregations(aggregations, field_mappings)

        # Check for top/bottom modifiers
        order_field = None
        order_direction = "desc"
        size = 10

        for agg in aggregations:
            if "modifier" in agg:
                # Configure ordering based on modifier
                alias = agg.get("alias") or f"{agg['function']}_{agg['field']}_0"
                order_field = alias
                order_direction = "desc" if agg["modifier"] == "top" else "asc"
                size = agg.get("limit", 10)
                break

        # Build nested terms aggregations for each group_by field
        current_aggs = inner_aggs

        # Process group_by fields in reverse order to build proper nesting
        for field in reversed(group_by_fields):
            terms_agg = {"terms": {"field": field, "size": size}}

            # Add ordering if this is the outermost aggregation and we have order field
            if field == group_by_fields[0] and order_field:
                # For nested aggregations, we need the full path
                order_path = order_field
                if len(group_by_fields) > 1:
                    # Multi-level grouping requires special handling
                    # OpenSearch doesn't support ordering by sub-aggregations in nested terms
                    # We'll need to handle this in post-processing
                    pass
                else:
                    terms_agg["terms"]["order"] = {order_path: order_direction}

            # Add sub-aggregations
            if current_aggs:
                terms_agg["aggs"] = current_aggs

            # Wrap for next level
            current_aggs = {f"group_by_{field}": terms_agg}

        return current_aggs

    def _validate_numeric_field(self, field: str, function: str, field_mappings: Dict[str, str]) -> None:
        """Validate that a field is numeric for numeric aggregations.

        Args:
            field: Field name
            function: Aggregation function
            field_mappings: Field type mappings

        Raises:
            TQLError: If field is not numeric
        """
        field_type = field_mappings.get(field, "unknown")

        # OpenSearch numeric types
        numeric_types = {
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

        if field_type not in numeric_types and field_type != "unknown":
            raise TQLError(
                f"Cannot perform {function}() on non-numeric field '{field}'. "
                f"Field '{field}' has type '{field_type}'. "
                f"Numeric aggregations require numeric types: {', '.join(sorted(numeric_types))}"
            )

    def transform_response(self, response: Dict[str, Any], stats_ast: Dict[str, Any]) -> Dict[str, Any]:
        """Transform OpenSearch aggregation response to TQL format.

        Args:
            response: OpenSearch aggregation response
            stats_ast: Original stats AST for reference

        Returns:
            Transformed response in TQL format
        """
        aggregations = stats_ast.get("aggregations", [])
        group_by_fields = stats_ast.get("group_by", [])

        if not group_by_fields:
            # Simple aggregation response
            return self._transform_simple_response(response, aggregations)
        else:
            # Grouped aggregation response
            return self._transform_grouped_response(response, aggregations, group_by_fields)

    def _transform_simple_response(
        self, response: Dict[str, Any], aggregations: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Transform simple aggregation response.

        Args:
            response: OpenSearch response
            aggregations: Aggregation specifications

        Returns:
            Transformed response
        """
        aggs_data = response.get("aggregations", {})

        if len(aggregations) == 1:
            # Single aggregation
            agg = aggregations[0]
            alias = agg.get("alias") or f"{agg['function']}_{agg['field']}_0"

            value = self._extract_aggregation_value(aggs_data.get(alias, {}), agg["function"])

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
            for i, agg in enumerate(aggregations):
                alias = agg.get("alias") or f"{agg['function']}_{agg['field']}_{i}"
                value = self._extract_aggregation_value(aggs_data.get(alias, {}), agg["function"])
                key = agg.get("alias") or f"{agg['function']}_{agg['field']}"
                results[key] = value

            return {"type": "multiple_aggregations", "results": results}

    def _transform_grouped_response(
        self, response: Dict[str, Any], aggregations: List[Dict[str, Any]], group_by_fields: List[str]
    ) -> Dict[str, Any]:
        """Transform grouped aggregation response.

        Args:
            response: OpenSearch response
            aggregations: Aggregation specifications
            group_by_fields: Grouping fields

        Returns:
            Transformed response
        """
        # Navigate to the grouped results
        aggs_data = response.get("aggregations", {})

        # Get the outermost grouping
        first_group_key = f"group_by_{group_by_fields[0]}"
        grouped_data = aggs_data.get(first_group_key, {})

        # Extract buckets
        buckets = grouped_data.get("buckets", [])

        # Transform buckets
        results = []
        for bucket in buckets:
            result = self._transform_bucket(bucket, aggregations, group_by_fields, 0)
            if result:
                results.append(result)

        return {"type": "grouped_aggregation", "group_by": group_by_fields, "results": results}

    def _transform_bucket(
        self, bucket: Dict[str, Any], aggregations: List[Dict[str, Any]], group_by_fields: List[str], level: int
    ) -> Optional[Dict[str, Any]]:
        """Transform a single bucket from grouped aggregation.

        Args:
            bucket: OpenSearch bucket
            aggregations: Aggregation specifications
            group_by_fields: Grouping fields
            level: Current nesting level

        Returns:
            Transformed bucket or None
        """
        result = {"key": {}, "doc_count": bucket.get("doc_count", 0)}

        # Add current level key
        if level < len(group_by_fields):
            field = group_by_fields[level]
            result["key"][field] = bucket.get("key")

        # Check if there are more levels
        if level + 1 < len(group_by_fields):
            # Navigate to next level
            next_field = group_by_fields[level + 1]
            next_group_key = f"group_by_{next_field}"

            if next_group_key in bucket:
                # This is a nested grouping, we need to aggregate the sub-buckets
                # For now, we'll just take the first sub-bucket
                # TODO: Handle proper multi-level grouping
                sub_buckets = bucket[next_group_key].get("buckets", [])
                if sub_buckets:
                    sub_result = self._transform_bucket(sub_buckets[0], aggregations, group_by_fields, level + 1)
                    if sub_result:
                        # Merge keys
                        result["key"].update(sub_result["key"])

        # Extract aggregation values
        if len(aggregations) == 1:
            # Single aggregation
            agg = aggregations[0]
            alias = agg.get("alias") or f"{agg['function']}_{agg['field']}_0"
            value = self._extract_aggregation_value(bucket.get(alias, {}), agg["function"])
            agg_key = agg.get("alias") or agg["function"]
            result[agg_key] = value
        else:
            # Multiple aggregations
            result["aggregations"] = {}
            for i, agg in enumerate(aggregations):
                alias = agg.get("alias") or f"{agg['function']}_{agg['field']}_{i}"
                value = self._extract_aggregation_value(bucket.get(alias, {}), agg["function"])
                agg_key = agg.get("alias") or f"{agg['function']}_{agg['field']}"
                result["aggregations"][agg_key] = value

        return result

    def _extract_aggregation_value(  # noqa: C901
        self, agg_result: Dict[str, Any], function: str
    ) -> Union[int, float, Dict[str, Any], None]:
        """Extract value from OpenSearch aggregation result.

        Args:
            agg_result: OpenSearch aggregation result
            function: TQL aggregation function

        Returns:
            Extracted value
        """
        if function == "count":
            return agg_result.get("value", 0)
        elif function == "unique_count":
            return agg_result.get("value", 0)
        elif function in ["sum", "min", "max", "average", "avg"]:
            return agg_result.get("value")
        elif function in ["median", "med"]:
            # Extract from percentiles
            values = agg_result.get("values", {})
            return values.get("50.0") or values.get("50")
        elif function in ["std", "standard_deviation"]:
            # Extract from extended_stats
            return agg_result.get("std_deviation")
        elif function in ["percentile", "percentiles", "p", "pct"]:
            # Extract percentile values
            values = agg_result.get("values", {})
            if len(values) == 1:
                # Single percentile - return just the value
                return list(values.values())[0]
            else:
                # Multiple percentiles - return dict
                result = {}
                for k, v in values.items():
                    # Convert "95.0" to "p95"
                    percentile = int(float(k))
                    result[f"p{percentile}"] = v
                return result
        elif function in ["percentile_rank", "percentile_ranks", "pct_rank", "pct_ranks"]:
            # Extract percentile rank values
            values = agg_result.get("values", {})
            if len(values) == 1:
                # Single rank - return just the value
                return list(values.values())[0]
            else:
                # Multiple ranks - return dict
                result = {}
                for k, v in values.items():
                    result[f"rank_{k}"] = v
                return result
        elif function in ["values", "unique"]:
            # Extract buckets from terms aggregation
            buckets = agg_result.get("buckets", [])
            return [bucket["key"] for bucket in buckets]
        else:
            return None
