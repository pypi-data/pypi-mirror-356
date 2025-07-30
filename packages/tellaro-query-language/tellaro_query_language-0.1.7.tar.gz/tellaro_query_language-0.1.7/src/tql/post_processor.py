"""Post-processor for applying mutators to OpenSearch query results.

This module handles the application of mutators that cannot be pre-processed
by OpenSearch field mappings/analyzers and must be applied to results after
they are returned from OpenSearch.
"""

import copy
from typing import Any, Dict, List, Optional

from .mutator_analyzer import PostProcessingRequirement
from .mutators import apply_mutators


class QueryPostProcessor:
    """Applies post-processing mutators to OpenSearch query results."""

    def __init__(self):
        """Initialize the post-processor."""

    def filter_results(
        self, results: List[Dict[str, Any]], requirements: List[PostProcessingRequirement]
    ) -> List[Dict[str, Any]]:
        """Filter results based on post-processing requirements.

        This method handles operator-based filtering for all operators that require
        post-processing evaluation.

        Args:
            results: List of result records from OpenSearch
            requirements: List of post-processing requirements

        Returns:
            Filtered list of results
        """
        if not requirements:
            return results

        filtered_results = []

        for result in results:
            should_include = True

            # Check each requirement
            for requirement in requirements:
                if requirement.metadata and "operator" in requirement.metadata:
                    operator = requirement.metadata["operator"]
                    value = requirement.metadata.get("value")

                    # Get the field value - either mutated or original
                    # First check for mutated value in temp field
                    temp_field_name = f"__{requirement.field_name}_mutated__"
                    if temp_field_name in result:
                        field_value = result[temp_field_name]
                    else:
                        field_value = self._get_field_value(result, requirement.field_name)

                    # Apply the operator check
                    if not self._check_operator(field_value, operator, value):
                        should_include = False
                        break

            if should_include:
                filtered_results.append(result)

        return filtered_results

    def _check_operator(self, field_value: Any, operator: str, value: Any) -> bool:  # noqa: C901
        """Check if a field value matches the given operator and value.

        Args:
            field_value: The field value to check
            operator: The operator to apply
            value: The value to compare against

        Returns:
            True if the operator check passes, False otherwise
        """
        # Unwrap single-element lists for comparison
        if isinstance(value, list) and len(value) == 1:
            value = value[0]

        # Handle None/missing fields
        if field_value is None:
            # Most operators should return False for missing fields
            return False

        # String operators
        if operator == "contains":
            return str(value).lower() in str(field_value).lower()
        elif operator == "not_contains":
            return str(value).lower() not in str(field_value).lower()
        elif operator == "startswith":
            return str(field_value).lower().startswith(str(value).lower())
        elif operator == "not_startswith":
            return not str(field_value).lower().startswith(str(value).lower())
        elif operator == "endswith":
            return str(field_value).lower().endswith(str(value).lower())
        elif operator == "not_endswith":
            return not str(field_value).lower().endswith(str(value).lower())

        # Equality operators
        elif operator in ["eq", "="]:
            # Handle boolean comparisons
            if isinstance(field_value, bool) and isinstance(value, str):
                # Convert string to boolean for comparison
                if value.lower() == "true":
                    return field_value is True
                elif value.lower() == "false":
                    return field_value is False
            return field_value == value
        elif operator in ["ne", "!="]:
            # Handle boolean comparisons
            if isinstance(field_value, bool) and isinstance(value, str):
                # Convert string to boolean for comparison
                if value.lower() == "true":
                    return field_value is not True
                elif value.lower() == "false":
                    return field_value is not False
            return field_value != value

        # Comparison operators
        elif operator in ["gt", ">"]:
            try:
                return float(field_value) > float(value)
            except (ValueError, TypeError):
                return str(field_value) > str(value)
        elif operator in ["gte", ">="]:
            try:
                return float(field_value) >= float(value)
            except (ValueError, TypeError):
                return str(field_value) >= str(value)
        elif operator in ["lt", "<"]:
            try:
                return float(field_value) < float(value)
            except (ValueError, TypeError):
                return str(field_value) < str(value)
        elif operator in ["lte", "<="]:
            try:
                return float(field_value) <= float(value)
            except (ValueError, TypeError):
                return str(field_value) <= str(value)

        # Array operators
        elif operator == "all":
            if isinstance(field_value, (list, tuple)):
                # For arrays, ALL elements must equal the value
                # Empty arrays should not pass ALL
                return len(field_value) > 0 and all(elem == value for elem in field_value)
            else:
                # For single values, simple equality
                return field_value == value
        elif operator == "not_all":
            if isinstance(field_value, (list, tuple)):
                # For arrays, if ALL elements equal the value, fail
                # Empty arrays should pass NOT_ALL
                return len(field_value) == 0 or not all(elem == value for elem in field_value)
            else:
                # For single values, if equal, fail
                return field_value != value

        # Default to False for unknown operators
        return False

    def process_results(
        self,
        results: List[Dict[str, Any]],
        requirements: List[PostProcessingRequirement],
        track_enrichments: bool = False,
    ) -> List[Dict[str, Any]]:
        """Apply post-processing mutators to query results.

        Args:
            results: List of result records from OpenSearch
            requirements: List of post-processing requirements
            track_enrichments: If True, track which records were enriched

        Returns:
            List of processed results with mutators applied.
            If track_enrichments is True, each result will have a '_enriched' flag.
        """
        if not requirements:
            return results

        processed_results = []

        for result in results:
            # Deep copy to avoid modifying original
            processed_result = copy.deepcopy(result)
            enriched = False

            # Apply each post-processing requirement
            for requirement in requirements:
                try:
                    was_enriched = self._apply_requirement(processed_result, requirement)
                    if was_enriched:
                        enriched = True
                except Exception:
                    # Log error but continue processing
                    # In a production system, you might want to log this
                    continue

            # Track enrichment status if requested
            if track_enrichments:
                processed_result["_enriched"] = enriched

            processed_results.append(processed_result)

        return processed_results

    def _apply_requirement(self, result: Dict[str, Any], requirement: PostProcessingRequirement) -> bool:
        """Apply a single post-processing requirement to a result.

        Args:
            result: The result record to modify
            requirement: The post-processing requirement to apply

        Returns:
            True if the record was enriched, False otherwise
        """
        if requirement.applies_to == "field":
            return self._apply_field_mutators(result, requirement)
        elif requirement.applies_to == "value":
            return self._apply_value_mutators(result, requirement)
        elif requirement.applies_to == "geo_expr":
            return self._apply_geo_expression(result, requirement)
        elif requirement.applies_to == "nslookup_expr":
            return self._apply_nslookup_expression(result, requirement)
        return False

    def _apply_field_mutators(self, result: Dict[str, Any], requirement: PostProcessingRequirement) -> bool:
        """Apply field mutators to a result record.

        Args:
            result: The result record to modify
            requirement: The field mutator requirement

        Returns:
            True if enrichment occurred, False otherwise
        """
        # Check if this is an operator-only requirement (like ALL operator with no mutators)
        if requirement.metadata and "operator" in requirement.metadata and not requirement.mutators:
            # This is handled separately in filter_results
            return False

        # Get the field value using the mapped field name
        field_value = self._get_field_value(result, requirement.mapped_field_name)

        if field_value is None:
            return False

        # Apply mutators to the field value
        try:
            mutated_value = apply_mutators(field_value, requirement.mutators, requirement.field_name, result)

            # Check if this is a type-changing mutator that should not replace the field
            # These mutators are used for filtering, not transforming the field value
            TYPE_CHANGING_FILTER_MUTATORS = {
                "is_private",
                "is_global",
                "length",
                "any",
                "all",
                "avg",
                "average",
                "sum",
                "max",
                "min",
                "split",
            }
            mutator_names = {m.get("name", "").lower() for m in requirement.mutators}

            # Check the operator from metadata to determine if this is for filtering only
            operator = requirement.metadata.get("operator", "") if requirement.metadata else ""
            is_filtering_operation = operator in [
                "contains",
                "not_contains",
                "startswith",
                "endswith",
                "not_startswith",
                "not_endswith",
                "eq",
                "=",
                "ne",
                "!=",
                ">",
                ">=",
                "<",
                "<=",
                "gt",
                "gte",
                "lt",
                "lte",
            ]

            if mutator_names.intersection(TYPE_CHANGING_FILTER_MUTATORS) or is_filtering_operation:
                # For type-changing mutators or filtering operations, store the result in a temporary field
                # This allows re-evaluation to work correctly
                temp_field_name = f"__{requirement.field_name}_mutated__"
                self._set_field_value(result, temp_field_name, mutated_value)
            else:
                # Update the result with the mutated value
                # Use the original field name for the output
                self._set_field_value(result, requirement.field_name, mutated_value)

            # Check if this is an enrichment mutator
            from .mutators import ENRICHMENT_MUTATORS

            for mutator in requirement.mutators:
                if mutator.get("name", "").lower() in ENRICHMENT_MUTATORS:
                    return True

        except Exception:
            # If mutation fails, leave original value
            pass

        return False

    def _apply_value_mutators(self, result: Dict[str, Any], requirement: PostProcessingRequirement) -> bool:
        """Apply value mutators to a result record.

        Note: Value mutators are typically applied during query evaluation,
        not to results. This method is included for completeness but may
        not be commonly used.

        Args:
            result: The result record to modify
            requirement: The value mutator requirement

        Returns:
            False (value mutators do not enrich records)
        """
        # Value mutators are typically applied to query values, not result values
        # This method is included for completeness but may not be used in practice
        return False

    def _apply_geo_expression(  # noqa: C901
        self, result: Dict[str, Any], requirement: PostProcessingRequirement
    ) -> bool:
        """Apply geo expression enrichment and filtering to a result.

        Args:
            result: The result record to modify
            requirement: The geo expression requirement

        Returns:
            True if geo enrichment occurred, False otherwise
        """
        # Get the IP field value
        ip_value = self._get_field_value(result, requirement.field_name)

        if not ip_value:
            # No IP value, nothing to enrich
            return False

        # Apply geoip_lookup mutator for enrichment
        try:
            geo_data = apply_mutators(
                ip_value, requirement.mutators, requirement.field_name, result  # Contains geoip_lookup mutator
            )

            # The geo data is returned as a dict with geo.* and as.* fields
            # We need to nest it under the parent of the IP field
            if isinstance(geo_data, dict) and geo_data:
                # Check if a custom field location was specified
                custom_field = None
                for mutator in requirement.mutators:
                    if "params" in mutator:
                        params = mutator["params"]
                        # Convert params from list format to dict if needed
                        if isinstance(params, list):
                            params_dict = {}
                            for param in params:
                                if len(param) == 2:
                                    params_dict[param[0]] = param[1]
                            params = params_dict

                        if "field" in params:
                            custom_field = params["field"]
                            break

                if custom_field:
                    # Use the custom field location
                    parent = self._get_or_create_parent(result, custom_field)
                    # Store geo data directly at the custom location
                    if "geo" in geo_data:
                        parent.update(geo_data["geo"])
                    # Store AS data separately if present
                    if "as" in geo_data and custom_field:
                        # If custom field has a parent, store AS data as sibling
                        if "." in custom_field:
                            as_parent_path = custom_field.rsplit(".", 1)[0]
                            as_parent = self._get_or_create_parent(result, as_parent_path)
                            as_parent["as"] = geo_data["as"]
                        else:
                            # Store at root level
                            result["as"] = geo_data["as"]
                else:
                    # Default behavior: store under parent.geo and parent.as
                    if "." in requirement.field_name:
                        # Nested field like destination.ip or source.ip
                        parent_path = requirement.field_name.rsplit(".", 1)[0]
                        parent = self._get_or_create_parent(result, parent_path)

                        # Add geo and as data under the parent
                        if "geo" in geo_data:
                            parent["geo"] = geo_data["geo"]
                        if "as" in geo_data:
                            parent["as"] = geo_data["as"]
                    else:
                        # Top-level field like 'ip' - use generic enrichment parent
                        if "enrichment" not in result:
                            result["enrichment"] = {}

                        if "geo" in geo_data:
                            result["enrichment"]["geo"] = geo_data["geo"]
                        if "as" in geo_data:
                            result["enrichment"]["as"] = geo_data["as"]

            # Note: Filtering based on conditions is handled separately
            # during the filter_results phase, not here
            return True  # Geo enrichment occurred

        except Exception:
            # If geo lookup fails, continue without enrichment
            pass

        return False

    def _apply_nslookup_expression(  # noqa: C901
        self, result: Dict[str, Any], requirement: PostProcessingRequirement
    ) -> bool:
        """Apply nslookup expression enrichment and filtering to a result.

        Args:
            result: The result record to modify
            requirement: The nslookup expression requirement

        Returns:
            True if DNS enrichment occurred, False otherwise
        """
        # Get the field value (IP or hostname)
        field_value = self._get_field_value(result, requirement.field_name)

        if not field_value:
            # No value, nothing to enrich
            return False

        # Apply nslookup mutator for enrichment
        try:
            dns_data = apply_mutators(
                field_value, requirement.mutators, requirement.field_name, result  # Contains nslookup mutator
            )

            # The DNS data is returned as a dict with the query value as key
            # Each value contains ECS-compliant DNS data
            if isinstance(dns_data, dict) and dns_data:
                # DNS data should have one entry for the queried value
                # Extract the ECS data for the field value
                ecs_dns_data = None
                if field_value in dns_data:
                    ecs_dns_data = dns_data[field_value]
                elif len(dns_data) == 1:
                    # If there's only one entry, use it
                    ecs_dns_data = next(iter(dns_data.values()))

                if ecs_dns_data:
                    # Check if a custom field location was specified
                    custom_field = None
                    for mutator in requirement.mutators:
                        if "params" in mutator:
                            params = mutator["params"]
                            # Convert params from list format to dict if needed
                            if isinstance(params, list):
                                params_dict = {}
                                for param in params:
                                    if len(param) == 2:
                                        params_dict[param[0]] = param[1]
                                params = params_dict

                            if "field" in params:
                                custom_field = params["field"]
                                break

                    if custom_field:
                        # Use the custom field location
                        parent = self._get_or_create_parent(result, custom_field)
                        # Store DNS data directly at the custom location
                        parent.update(ecs_dns_data)
                    else:
                        # Default behavior: store at parent.domain
                        if "." in requirement.field_name:
                            # Nested field like destination.ip or source.hostname
                            parent_path = requirement.field_name.rsplit(".", 1)[0]
                            parent = self._get_or_create_parent(result, parent_path)

                            # Add ECS DNS data under the parent
                            parent["domain"] = ecs_dns_data
                        else:
                            # Top-level field like 'ip' - use generic enrichment parent
                            if "enrichment" not in result:
                                result["enrichment"] = {}

                            result["enrichment"]["domain"] = ecs_dns_data

            # Note: Filtering based on conditions is handled separately
            # during the filter_results phase, not here
            return True  # DNS enrichment occurred

        except Exception:
            # If DNS lookup fails, continue without enrichment
            pass

        return False

    def _get_or_create_parent(self, record: Dict[str, Any], parent_path: str) -> Dict[str, Any]:
        """Get or create a parent object in the record.

        Args:
            record: The record to modify
            parent_path: Dot-separated path to the parent

        Returns:
            The parent dictionary
        """
        parts = parent_path.split(".")
        current = record

        for part in parts:
            if part not in current:
                current[part] = {}
            elif not isinstance(current[part], dict):
                # If the parent exists but isn't a dict, we can't add to it
                raise ValueError(f"Cannot add geo data: {parent_path} is not an object")
            current = current[part]

        return current

    def _get_field_value(self, record: Dict[str, Any], field_path: str) -> Any:
        """Get a field value from a record, supporting nested fields.

        Args:
            record: The record dictionary
            field_path: Dot-separated field path or literal field name

        Returns:
            The field value, or None if not found
        """
        # First try the field_path as a literal key
        if isinstance(record, dict) and field_path in record:
            return record[field_path]

        # If not found as literal, try as dot-separated nested path
        parts = field_path.split(".")
        current = record

        for part in parts:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                return None

        return current

    def _set_field_value(self, record: Dict[str, Any], field_path: str, value: Any) -> None:
        """Set a field value in a record, supporting nested fields.

        Args:
            record: The record dictionary to modify
            field_path: Dot-separated field path or literal field name
            value: The value to set
        """
        # For setting values, we'll use the dot-separated path approach
        # and create nested structures as needed
        parts = field_path.split(".")
        current = record

        # Navigate to the parent of the target field
        for part in parts[:-1]:
            if part not in current:
                current[part] = {}
            current = current[part]

        # Set the final value
        current[parts[-1]] = value


class PostProcessingContext:
    """Context information for post-processing operations."""

    def __init__(self, query: str, field_mappings: Dict[str, Any], requirements: List[PostProcessingRequirement]):
        """Initialize post-processing context.

        Args:
            query: Original TQL query string
            field_mappings: Field mappings used in the query
            requirements: Post-processing requirements
        """
        self.query = query
        self.field_mappings = field_mappings
        self.requirements = requirements
        self.stats = PostProcessingStats()

    def get_performance_impact(self) -> Dict[str, Any]:
        """Get information about the performance impact of post-processing.

        Returns:
            Dictionary with performance impact information
        """
        impact: Dict[str, Any] = {
            "has_post_processing": bool(self.requirements),
            "requirement_count": len(self.requirements),
            "impacted_fields": list(set(req.field_name for req in self.requirements)),
            "mutator_types": [],
            "estimated_overhead": "low",
        }

        # Analyze mutator types for performance estimation
        mutator_counts: Dict[str, int] = {}
        for req in self.requirements:
            for mutator in req.mutators:
                mutator_name = mutator.get("name", "unknown")
                mutator_counts[mutator_name] = mutator_counts.get(mutator_name, 0) + 1
                if mutator_name not in impact["mutator_types"]:
                    impact["mutator_types"].append(mutator_name)

        # Estimate overhead based on mutator types
        expensive_mutators = {"geoip_lookup", "nslookup", "geo"}
        if any(mutator in expensive_mutators for mutator in mutator_counts):
            impact["estimated_overhead"] = "high"
        elif len(self.requirements) > 5:
            impact["estimated_overhead"] = "medium"

        impact["mutator_usage"] = mutator_counts

        return impact


class PostProcessingStats:
    """Statistics tracking for post-processing operations."""

    def __init__(self):
        """Initialize stats tracking."""
        self.processed_records = 0
        self.failed_records = 0
        self.mutator_applications = 0
        self.errors = []

    def record_success(self):
        """Record a successful record processing."""
        self.processed_records += 1

    def record_failure(self, error: str):
        """Record a failed record processing."""
        self.failed_records += 1
        self.errors.append(error)

    def record_mutator_application(self):
        """Record a mutator application."""
        self.mutator_applications += 1

    def get_summary(self) -> Dict[str, Any]:
        """Get a summary of processing statistics.

        Returns:
            Dictionary with processing statistics
        """
        total_records = self.processed_records + self.failed_records
        success_rate = (self.processed_records / total_records * 100) if total_records > 0 else 0

        return {
            "total_records": total_records,
            "processed_successfully": self.processed_records,
            "failed_records": self.failed_records,
            "success_rate_percent": round(success_rate, 2),
            "mutator_applications": self.mutator_applications,
            "error_count": len(self.errors),
            "recent_errors": self.errors[-5:] if self.errors else [],  # Last 5 errors
        }


class PostProcessingError(Exception):
    """Exception raised during post-processing operations."""

    def __init__(self, message: str, field_name: Optional[str] = None, mutator_name: Optional[str] = None):
        """Initialize post-processing error.

        Args:
            message: Error message
            field_name: Field name where error occurred
            mutator_name: Mutator name that caused the error
        """
        super().__init__(message)
        self.field_name = field_name
        self.mutator_name = mutator_name


class BatchPostProcessor(QueryPostProcessor):
    """Post-processor optimized for large batches of results."""

    def __init__(self, batch_size: int = 1000):
        """Initialize batch post-processor.

        Args:
            batch_size: Number of records to process in each batch
        """
        super().__init__()
        self.batch_size = batch_size

    def process_results(
        self,
        results: List[Dict[str, Any]],
        requirements: List[PostProcessingRequirement],
        track_enrichments: bool = False,
    ) -> List[Dict[str, Any]]:
        """Process results in batches for better memory efficiency.

        Args:
            results: List of result records from OpenSearch
            requirements: List of post-processing requirements
            track_enrichments: Whether to track enrichment operations

        Returns:
            List of processed results with mutators applied
        """
        if not requirements:
            return results

        processed_results = []

        # Process in batches
        for i in range(0, len(results), self.batch_size):
            batch = results[i : i + self.batch_size]
            processed_batch = super().process_results(batch, requirements, track_enrichments)
            processed_results.extend(processed_batch)

        return processed_results
