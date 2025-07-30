"""Mutator analysis for determining pre vs post-processing requirements.

This module analyzes TQL queries with mutators to determine which mutators can be
handled by OpenSearch field mappings/analyzers (pre-processing) and which must be
applied to results after they return from OpenSearch (post-processing).
"""

import copy
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Union

# from .exceptions import TQLFieldError  # Reserved for future use
from .mutators import create_mutator
from .mutators.base import PerformanceClass
from .opensearch import FieldMapping


class MutatorType(Enum):
    """Classification of mutator processing types."""

    PRE_PROCESSABLE = "pre"  # Can be handled by field mappings/analyzers
    POST_PROCESSABLE = "post"  # Must be applied to results
    CONDITIONAL = "conditional"  # Depends on field mapping availability


# Classification of built-in mutators
MUTATOR_CLASSIFICATIONS: Dict[str, MutatorType] = {
    "lowercase": MutatorType.POST_PROCESSABLE,  # Always post-process (transforms result)
    "uppercase": MutatorType.POST_PROCESSABLE,  # Always post-process (transforms result)
    "trim": MutatorType.POST_PROCESSABLE,  # Always post-process (transforms result)
    "split": MutatorType.POST_PROCESSABLE,  # Always post-process (returns array)
    "nslookup": MutatorType.POST_PROCESSABLE,  # Always post-process (enrichment)
    "geoip_lookup": MutatorType.POST_PROCESSABLE,  # Always post-process (enrichment)
    "geo": MutatorType.POST_PROCESSABLE,  # Always post-process (enrichment)
    "length": MutatorType.POST_PROCESSABLE,  # Always post-process (returns int)
    "refang": MutatorType.POST_PROCESSABLE,  # Always post-process (modifies value)
    "defang": MutatorType.POST_PROCESSABLE,  # Always post-process (modifies value)
    "b64encode": MutatorType.POST_PROCESSABLE,  # Always post-process (modifies value)
    "b64decode": MutatorType.POST_PROCESSABLE,  # Always post-process (modifies value)
    "urldecode": MutatorType.POST_PROCESSABLE,  # Always post-process (modifies value)
    "is_private": MutatorType.POST_PROCESSABLE,  # Always post-process (returns bool)
    "is_global": MutatorType.POST_PROCESSABLE,  # Always post-process (returns bool)
}


@dataclass
class PostProcessingRequirement:
    """Represents a mutator that needs to be applied after OpenSearch query execution."""

    field_name: str  # Original field name from query
    mapped_field_name: str  # Field name used in OpenSearch query
    mutators: List[Dict[str, Any]]  # List of mutator specifications
    applies_to: Literal[
        "field", "value", "geo_expr", "nslookup_expr"
    ]  # Whether this applies to field, value mutators, geo, or nslookup expressions
    metadata: Optional[Dict[str, Any]] = None  # Additional metadata for special processing


@dataclass
class MutatorAnalysisResult:
    """Result of analyzing mutators in a TQL query."""

    optimized_ast: Dict[str, Any]  # AST with pre-processable mutators removed
    post_processing_requirements: List[PostProcessingRequirement]  # Post-processing needed
    health_status: Literal["green", "yellow", "red"]  # Health status
    health_reasons: List[Dict[str, str]]  # Health issues found
    optimizations_applied: List[str]  # List of optimizations applied
    query_dsl: Optional[Dict[str, Any]] = None  # OpenSearch query DSL (added by core TQL class)
    save_enrichment_requested: bool = False  # Whether any mutator requested enrichment saving


class MutatorAnalyzer:
    """Analyzes TQL queries to determine mutator processing requirements."""

    def __init__(self, field_mappings: Optional[Dict[str, Union[str, Dict[str, Any]]]] = None):
        """Initialize the analyzer.

        Args:
            field_mappings: Field mappings for intelligent analysis
        """
        self.field_mappings = field_mappings or {}
        self.intelligent_mappings = {}

        # Parse field mappings into FieldMapping objects
        for field_name, mapping in self.field_mappings.items():
            if isinstance(mapping, dict):
                # Check if this is an OpenSearch-style mapping
                if "type" in mapping and not any(k for k in mapping.keys() if k not in ["type", "fields", "analyzer"]):
                    # OpenSearch-style mapping for a single field
                    field_mapping = FieldMapping(mapping)
                    field_mapping.set_base_field_name(field_name)
                    self.intelligent_mappings[field_name] = field_mapping
                else:
                    # Traditional intelligent mapping with multiple field variants
                    field_mapping = FieldMapping(mapping)
                    if not field_mapping.base_field_name:
                        field_mapping.base_field_name = field_name
                    self.intelligent_mappings[field_name] = field_mapping
            elif isinstance(mapping, str):
                # Check if this looks like a type specification
                if mapping in [
                    "keyword",
                    "text",
                    "long",
                    "integer",
                    "short",
                    "byte",
                    "double",
                    "float",
                    "boolean",
                    "date",
                    "ip",
                ]:
                    # Type specification, create intelligent mapping
                    self.intelligent_mappings[field_name] = FieldMapping({field_name: mapping})

    def analyze_ast(self, ast: Dict[str, Any], context: str = "opensearch") -> MutatorAnalysisResult:  # noqa: C901
        """Analyze an AST to determine mutator processing requirements.

        Args:
            ast: The parsed TQL query AST
            context: Execution context ("opensearch" or "in_memory")

        Returns:
            Analysis result with optimized AST and post-processing requirements
        """
        # Deep copy AST to avoid modifying original
        optimized_ast = copy.deepcopy(ast)
        post_processing_requirements: List[PostProcessingRequirement] = []
        health_reasons: List[Dict[str, str]] = []
        optimizations_applied: List[str] = []

        # Track if enrichment saving is requested
        save_enrichment_requested = False

        # Analyze the AST recursively
        self._analyze_node(optimized_ast, post_processing_requirements, health_reasons, optimizations_applied)

        # Check if any mutator requested enrichment saving
        for req in post_processing_requirements:
            for mutator in req.mutators:
                if mutator.get("params"):
                    for param in mutator["params"]:
                        if isinstance(param, list) and len(param) == 2 and param[0] == "save" and param[1]:
                            save_enrichment_requested = True
                            break
            # Also check geo_params in metadata
            if req.metadata and "geo_params" in req.metadata:
                geo_params = req.metadata["geo_params"]
                if geo_params.get("save"):
                    save_enrichment_requested = True
            # Also check nslookup_params in metadata
            if req.metadata and "nslookup_params" in req.metadata:
                nslookup_params = req.metadata["nslookup_params"]
                if nslookup_params.get("save"):
                    save_enrichment_requested = True

        # Determine overall health status based on context
        health_status: Literal["green", "yellow", "red"] = "green"
        if post_processing_requirements:
            # Evaluate health based on context
            health_eval = self._evaluate_health_for_context(post_processing_requirements, context)
            health_status = health_eval["health_status"]  # type: ignore[assignment]
            health_reasons.extend(health_eval["health_reasons"])

        # Check for red health conditions (errors)
        for reason in health_reasons:
            if reason["status"] == "red":
                health_status = "red"
                break

        return MutatorAnalysisResult(
            optimized_ast=optimized_ast,
            post_processing_requirements=post_processing_requirements,
            health_status=health_status,
            health_reasons=health_reasons,
            optimizations_applied=optimizations_applied,
            save_enrichment_requested=save_enrichment_requested,
        )

    def _analyze_node(  # noqa: C901
        self,
        node: Dict[str, Any],
        post_processing_reqs: List[PostProcessingRequirement],
        health_reasons: List[Dict[str, str]],
        optimizations: List[str],
    ) -> None:
        """Recursively analyze an AST node for mutator processing.

        Args:
            node: Current AST node
            post_processing_reqs: List to append post-processing requirements
            health_reasons: List to append health issues
            optimizations: List to append optimization descriptions
        """
        if not isinstance(node, dict):
            return

        node_type = node.get("type")

        if node_type == "comparison":
            self._analyze_comparison_node(node, post_processing_reqs, health_reasons, optimizations)
        elif node_type == "collection_op":
            self._analyze_collection_node(node, post_processing_reqs, health_reasons, optimizations)
        elif node_type == "logical_op":
            # Recursively analyze both sides
            self._analyze_node(node.get("left", {}), post_processing_reqs, health_reasons, optimizations)
            self._analyze_node(node.get("right", {}), post_processing_reqs, health_reasons, optimizations)
        elif node_type == "unary_op":
            # Analyze the operand
            self._analyze_node(node.get("operand", {}), post_processing_reqs, health_reasons, optimizations)
        elif node_type == "geo_expr":
            # Geo expressions always require post-processing since they involve geoip_lookup
            field_name = node.get("field")
            conditions = node.get("conditions")
            geo_params = node.get("geo_params", {})

            if field_name:
                # Create a special post-processing requirement for geo expressions
                # that includes both the enrichment and the filtering

                # Build mutator params list from geo_params
                mutator_params = []
                for param_name, param_value in geo_params.items():
                    mutator_params.append([param_name, param_value])

                geo_requirement = PostProcessingRequirement(
                    field_name=field_name,
                    mapped_field_name=field_name,
                    mutators=(
                        [{"name": "geoip_lookup", "params": mutator_params}]
                        if mutator_params
                        else [{"name": "geoip_lookup"}]
                    ),
                    applies_to="geo_expr",  # Special type for geo expressions
                    metadata={
                        "conditions": conditions,  # Include the conditions for filtering
                        "node_type": "geo_expr",
                        "geo_params": geo_params,  # Include geo parameters
                    },
                )
                post_processing_reqs.append(geo_requirement)

                # Mark the node for post-processing
                node["requires_post_processing"] = True
                node["post_process_type"] = "geo_expr"

                if conditions:
                    optimizations.append(
                        f"Geo expression on field '{field_name}' with conditions requires post-processing"
                    )
                else:
                    optimizations.append(f"Geo expression on field '{field_name}' for enrichment only")

            # Don't analyze conditions recursively - they're part of the geo expression
        elif node_type == "nslookup_expr":
            # NSLookup expressions always require post-processing since they involve DNS lookups
            field_name = node.get("field")
            conditions = node.get("conditions")
            nslookup_params = node.get("nslookup_params", {})

            if field_name:
                # Create a special post-processing requirement for nslookup expressions
                # that includes both the enrichment and the filtering

                # Build mutator params list from nslookup_params
                mutator_params = []
                for param_name, param_value in nslookup_params.items():
                    mutator_params.append([param_name, param_value])

                nslookup_requirement = PostProcessingRequirement(
                    field_name=field_name,
                    mapped_field_name=field_name,
                    mutators=(
                        [{"name": "nslookup", "params": mutator_params}] if mutator_params else [{"name": "nslookup"}]
                    ),
                    applies_to="nslookup_expr",  # Special type for nslookup expressions
                    metadata={
                        "conditions": conditions,  # Include the conditions for filtering
                        "node_type": "nslookup_expr",
                        "nslookup_params": nslookup_params,  # Include nslookup parameters
                    },
                )
                post_processing_reqs.append(nslookup_requirement)

                # Mark the node for post-processing
                node["requires_post_processing"] = True
                node["post_process_type"] = "nslookup_expr"

                if conditions:
                    optimizations.append(
                        f"NSLookup expression on field '{field_name}' with conditions requires post-processing"
                    )
                else:
                    optimizations.append(f"NSLookup expression on field '{field_name}' for enrichment only")

            # Don't analyze conditions recursively - they're part of the nslookup expression

    def _analyze_comparison_node(  # noqa: C901
        self,
        node: Dict[str, Any],
        post_processing_reqs: List[PostProcessingRequirement],
        health_reasons: List[Dict[str, str]],
        optimizations: List[str],
    ) -> None:
        """Analyze a comparison node for mutator processing.

        Args:
            node: Comparison AST node
            post_processing_reqs: List to append post-processing requirements
            health_reasons: List to append health issues
            optimizations: List to append optimization descriptions
        """
        field_name = node.get("field")
        operator = node.get("operator")
        field_mutators = node.get("field_mutators", [])
        value_mutators = node.get("value_mutators", [])

        if not field_name or not operator:
            return

        # Analyze field mutators
        if field_mutators:
            result = self._analyze_field_mutators(field_name, field_mutators, operator)

            # Update node with optimized mutators
            if result.optimized_mutators != field_mutators:
                if result.optimized_mutators:
                    node["field_mutators"] = result.optimized_mutators
                else:
                    # Remove field_mutators if all were optimized away
                    node.pop("field_mutators", None)

                optimizations.extend(result.optimizations)

            # Add post-processing requirements
            if result.post_processing_mutators:
                post_processing_reqs.append(
                    PostProcessingRequirement(
                        field_name=field_name,
                        mapped_field_name=result.selected_field or field_name,
                        mutators=result.post_processing_mutators,
                        applies_to="field",
                        metadata={"operator": operator, "value": node.get("value")},
                    )
                )

                # Check if any mutators change the field type
                has_type_changing_mutator = any(
                    mutator.get("name", "").lower()
                    in ["length", "avg", "average", "sum", "max", "min", "any", "all", "is_private", "is_global"]
                    for mutator in result.post_processing_mutators
                )

                # For field mutators on certain operations, we need to make the query less restrictive
                # This allows post-processing to correctly filter results
                if operator in [
                    "eq",
                    "=",
                    "ne",
                    "!=",
                    "contains",
                    "not_contains",
                    "startswith",
                    "endswith",
                    "not_startswith",
                    "not_endswith",
                ]:
                    # Mark the node to indicate it needs special handling in OpenSearch
                    node["post_process_value"] = True
                    # Keep the original value for reference
                    node["original_value"] = node.get("value")
                    # Also mark if we have type-changing mutators
                    if has_type_changing_mutator:
                        node["has_type_changing_mutators"] = True
                elif has_type_changing_mutator:
                    # For type-changing mutators with numeric operators, mark for special handling
                    node["has_type_changing_mutators"] = True

            # Add health reasons
            health_reasons.extend(result.health_reasons)

            # Update field name if optimized
            if result.selected_field and result.selected_field != field_name:
                node["field"] = result.selected_field

        # Check if operator requires post-processing (e.g., ALL operator on arrays)
        if operator in ["all", "not_all"]:
            # These operators need post-processing for array fields
            post_processing_reqs.append(
                PostProcessingRequirement(
                    field_name=field_name,
                    mapped_field_name=field_name,
                    mutators=[],  # No mutators, just operator-based filtering
                    applies_to="field",
                    metadata={"operator": operator, "value": node.get("value")},
                )
            )
            # Mark for special handling in OpenSearch
            node["post_process_value"] = True

        # Analyze value mutators (these are typically post-processing)
        if value_mutators:
            post_processing_value_mutators = []

            for mutator in value_mutators:
                mutator_name = mutator.get("name", "").lower()
                classification = MUTATOR_CLASSIFICATIONS.get(mutator_name, MutatorType.POST_PROCESSABLE)

                if classification in [MutatorType.POST_PROCESSABLE, MutatorType.CONDITIONAL]:
                    post_processing_value_mutators.append(mutator)

            if post_processing_value_mutators:
                post_processing_reqs.append(
                    PostProcessingRequirement(
                        field_name=field_name,
                        mapped_field_name=field_name,  # Value mutators don't affect field mapping
                        mutators=post_processing_value_mutators,
                        applies_to="value",
                    )
                )

                # For value mutators on equality operations, we need to make the query less restrictive
                # This allows post-processing to correctly filter results
                if operator in ["eq", "=", "ne", "!="]:
                    # Mark the node to indicate it needs special handling in OpenSearch
                    node["post_process_value"] = True
                    # Keep the original value for reference
                    node["original_value"] = node.get("value")

                # Remove value mutators from AST since they'll be post-processed
                node.pop("value_mutators", None)
                optimizations.append(f"Moved {len(post_processing_value_mutators)} value mutator(s) to post-processing")

    def _analyze_collection_node(
        self,
        node: Dict[str, Any],
        post_processing_reqs: List[PostProcessingRequirement],
        health_reasons: List[Dict[str, str]],
        optimizations: List[str],
    ) -> None:
        """Analyze a collection operation node for mutator processing.

        Args:
            node: Collection operation AST node
            post_processing_reqs: List to append post-processing requirements
            health_reasons: List to append health issues
            optimizations: List to append optimization descriptions
        """
        field_name = node.get("field")
        field_mutators = node.get("field_mutators", [])
        value_mutators = node.get("value_mutators", [])

        if not field_name:
            return

        # For collection operations, handle mutators similar to comparison nodes
        # but be more conservative about optimizations

        if field_mutators:
            # For collection ops, we're more conservative - most field mutators go to post-processing
            post_processing_field_mutators = []

            for mutator in field_mutators:
                mutator_name = mutator.get("name", "").lower()
                classification = MUTATOR_CLASSIFICATIONS.get(mutator_name, MutatorType.POST_PROCESSABLE)

                # For collection operations, be conservative and post-process most mutators
                if classification != MutatorType.PRE_PROCESSABLE:
                    post_processing_field_mutators.append(mutator)

            if post_processing_field_mutators:
                post_processing_reqs.append(
                    PostProcessingRequirement(
                        field_name=field_name,
                        mapped_field_name=field_name,
                        mutators=post_processing_field_mutators,
                        applies_to="field",
                    )
                )

                # Remove field mutators from AST
                node.pop("field_mutators", None)
                optimizations.append(
                    f"Moved {len(post_processing_field_mutators)} field mutator(s) to "
                    f"post-processing for collection operation"
                )

        if value_mutators:
            # Value mutators always go to post-processing for collection operations
            post_processing_reqs.append(
                PostProcessingRequirement(
                    field_name=field_name, mapped_field_name=field_name, mutators=value_mutators, applies_to="value"
                )
            )

            node.pop("value_mutators", None)
            optimizations.append(
                f"Moved {len(value_mutators)} value mutator(s) to post-processing for collection operation"
            )

    def _evaluate_health_for_context(  # noqa: C901
        self, post_processing_requirements: List[PostProcessingRequirement], context: str
    ) -> Dict[str, Any]:
        """Evaluate health status based on context and mutator performance characteristics.

        Args:
            post_processing_requirements: List of post-processing requirements
            context: Execution context ("opensearch" or "in_memory")

        Returns:
            Dictionary with health_status and health_reasons
        """
        fast_count = 0
        moderate_count = 0
        slow_count = 0
        slow_mutators = []
        all_mutators = []

        # Collect all mutators and their performance classes
        for req in post_processing_requirements:
            for mutator_spec in req.mutators:
                mutator_name = mutator_spec.get("name", "")
                all_mutators.append(mutator_name)

                try:
                    # Create mutator instance to get its performance characteristics
                    mutator = create_mutator(mutator_name, mutator_spec.get("params"))
                    perf_class = mutator.get_performance_class(context)

                    if perf_class == PerformanceClass.FAST:
                        fast_count += 1
                    elif perf_class == PerformanceClass.MODERATE:
                        moderate_count += 1
                    elif perf_class == PerformanceClass.SLOW:
                        slow_count += 1
                        slow_mutators.append(mutator_name)
                except Exception:
                    # If we can't create the mutator, assume moderate performance
                    moderate_count += 1

        # Determine health status based on context
        health_status = "green"
        health_reasons = []

        if context == "in_memory":
            # In-memory context: only slow mutators significantly impact health
            if slow_count > 0:
                health_status = "yellow"
                if slow_count > 2:
                    health_status = "red"
                health_reasons.append(
                    {
                        "status": health_status,
                        "query_part": f"mutators: {', '.join(slow_mutators)}",
                        "reason": f"{slow_count} slow mutator(s) ({', '.join(slow_mutators)}) may impact performance",
                    }
                )
            elif moderate_count > 5:
                # Many moderate mutators can also impact performance
                health_status = "yellow"
                health_reasons.append(
                    {
                        "status": "yellow",
                        "query_part": "multiple mutators",
                        "reason": f"{moderate_count} moderate-performance mutators may impact "
                        f"performance when combined",
                    }
                )
            # Fast mutators don't impact health in memory context

        elif context == "opensearch":
            # OpenSearch context: post-processing always impacts performance
            if slow_count > 0 or moderate_count > 0 or fast_count > 0:
                health_status = "yellow"
                if slow_count > 0:
                    health_status = "red" if slow_count > 1 else "yellow"

                reason_parts = []
                if fast_count > 0:
                    reason_parts.append(f"{fast_count} mutator(s)")
                if moderate_count > 0:
                    reason_parts.append(f"{moderate_count} moderate mutator(s)")
                if slow_count > 0:
                    reason_parts.append(f"{slow_count} slow mutator(s) [{', '.join(slow_mutators)}]")

                health_reasons.append(
                    {
                        "status": health_status,
                        "query_part": "post-processing required",
                        "reason": (
                            f"Post-processing required for {' + '.join(reason_parts)}, "
                            "which impacts performance with large result sets"
                        ),
                    }
                )

        return {"health_status": health_status, "health_reasons": health_reasons}

    def _analyze_field_mutators(
        self, field_name: str, mutators: List[Dict[str, Any]], operator: str
    ) -> "FieldMutatorAnalysisResult":
        """Analyze field mutators for a specific field."""
        analyzer = FieldMutatorAnalyzer(self.intelligent_mappings)
        return analyzer.analyze(field_name, mutators, operator)


@dataclass
class FieldMutatorAnalysisResult:
    """Result of analyzing field mutators for a specific field."""

    optimized_mutators: List[Dict[str, Any]]  # Mutators that remain in AST
    post_processing_mutators: List[Dict[str, Any]]  # Mutators for post-processing
    selected_field: Optional[str]  # Field name to use in OpenSearch query
    optimizations: List[str]  # Descriptions of optimizations applied
    health_reasons: List[Dict[str, str]]  # Health issues found


class FieldMutatorAnalyzer:
    """Analyzes field mutators for a specific field."""

    def __init__(self, field_mappings: Dict[str, FieldMapping]):
        """Initialize with intelligent field mappings."""
        self.field_mappings = field_mappings

    def analyze(self, field_name: str, mutators: List[Dict[str, Any]], operator: str) -> FieldMutatorAnalysisResult:
        """Analyze field mutators for optimization opportunities.

        Args:
            field_name: Name of the field
            mutators: List of mutator specifications
            operator: The operator being used in the comparison

        Returns:
            Analysis result with optimization recommendations
        """
        optimized_mutators: List[Dict[str, Any]] = []
        post_processing_mutators = []
        selected_field = None
        optimizations = []
        health_reasons = []

        # Check if we have intelligent mapping for this field
        if field_name in self.field_mappings:
            field_mapping = self.field_mappings[field_name]

            # Try to optimize mutators using field mapping
            for mutator in mutators:
                mutator_name = mutator.get("name", "").lower()

                if mutator_name == "lowercase":
                    optimization_result = self._optimize_lowercase_mutator(field_mapping, operator, mutator)
                elif mutator_name == "uppercase":
                    optimization_result = self._optimize_uppercase_mutator(field_mapping, operator, mutator)
                elif mutator_name == "trim":
                    optimization_result = self._optimize_trim_mutator(field_mapping, operator, mutator)
                else:
                    # Unknown or non-optimizable mutator - goes to post-processing
                    optimization_result = MutatorOptimizationResult(
                        can_optimize=False,
                        selected_field=None,
                        post_process_mutator=mutator,
                        optimization_description=f"Mutator '{mutator_name}' requires post-processing",
                    )

                # Apply optimization result
                if optimization_result.can_optimize:
                    if optimization_result.selected_field:
                        selected_field = optimization_result.selected_field
                    optimizations.append(optimization_result.optimization_description)
                    # Don't add to optimized_mutators if fully optimized
                else:
                    if optimization_result.post_process_mutator:
                        post_processing_mutators.append(optimization_result.post_process_mutator)
                    if optimization_result.health_issue:
                        health_reasons.append(optimization_result.health_issue)
        else:
            # No intelligent mapping - all mutators go to post-processing
            post_processing_mutators = mutators
            optimizations.append(f"No field mapping for '{field_name}' - all mutators require post-processing")

        return FieldMutatorAnalysisResult(
            optimized_mutators=optimized_mutators,
            post_processing_mutators=post_processing_mutators,
            selected_field=selected_field,
            optimizations=optimizations,
            health_reasons=health_reasons,
        )

    def _optimize_lowercase_mutator(
        self, field_mapping: FieldMapping, operator: str, mutator: Dict[str, Any]
    ) -> "MutatorOptimizationResult":
        """Try to optimize a lowercase mutator using field mappings."""
        # Check if we have a text field with lowercase analyzer
        lowercase_field = field_mapping.text_fields.get("lowercase")
        standard_field = field_mapping.text_fields.get("standard")

        if lowercase_field:
            # Perfect match - we have a lowercase analyzer
            return MutatorOptimizationResult(
                can_optimize=True,
                selected_field=lowercase_field,
                post_process_mutator=None,
                optimization_description=f"Using field '{lowercase_field}' with lowercase analyzer instead of mutator",
            )
        elif standard_field:
            # Standard analyzer might handle lowercase - use it but also post-process
            return MutatorOptimizationResult(
                can_optimize=False,
                selected_field=standard_field,
                post_process_mutator=mutator,
                optimization_description=f"Using text field '{standard_field}' but post-processing lowercase mutator",
            )
        elif field_mapping.keyword_field:
            # Only keyword field available - check operator compatibility
            if operator in [
                "eq",
                "=",
                "ne",
                "!=",
                "in",
                "not_in",
                "contains",
                "not_contains",
                "startswith",
                "endswith",
                "not_startswith",
                "not_endswith",
            ]:
                # These operators will work with post-processing
                return MutatorOptimizationResult(
                    can_optimize=False,
                    selected_field=field_mapping.keyword_field,
                    post_process_mutator=mutator,
                    optimization_description=f"Using keyword field '{field_mapping.keyword_field}' "
                    f"with post-processing",
                    health_issue={
                        "status": "yellow",
                        "query_part": f"{field_mapping.base_field_name} | lowercase",
                        "reason": "Keyword field used with lowercase mutator requires post-processing",
                    },
                )
            else:
                # Range operators don't make sense with lowercase
                return MutatorOptimizationResult(
                    can_optimize=False,
                    selected_field=None,
                    post_process_mutator=None,
                    optimization_description="",
                    health_issue={
                        "status": "red",
                        "query_part": f"{field_mapping.base_field_name} | lowercase {operator}",
                        "reason": (
                            f"Field '{field_mapping.base_field_name}' does not support case-insensitive "
                            f"searching with operator '{operator}'. Available: {field_mapping.keyword_field} (keyword)"
                        ),
                    },
                )
        else:
            # No suitable fields
            return MutatorOptimizationResult(
                can_optimize=False,
                selected_field=None,
                post_process_mutator=mutator,
                optimization_description="No suitable field mappings for lowercase optimization",
            )

    def _optimize_uppercase_mutator(
        self, field_mapping: FieldMapping, operator: str, mutator: Dict[str, Any]
    ) -> "MutatorOptimizationResult":
        """Try to optimize an uppercase mutator using field mappings."""
        # Check if we actually have an uppercase analyzer
        # We need to check the text_fields dict directly to ensure we have the specific analyzer
        if "uppercase" in field_mapping.text_fields:
            uppercase_field = field_mapping.text_fields["uppercase"]
            return MutatorOptimizationResult(
                can_optimize=True,
                selected_field=uppercase_field,
                post_process_mutator=None,
                optimization_description=f"Using field '{uppercase_field}' with uppercase analyzer instead of mutator",
            )
        else:
            # No uppercase analyzer - requires post-processing
            return MutatorOptimizationResult(
                can_optimize=False,
                selected_field=None,
                post_process_mutator=mutator,
                optimization_description="No uppercase analyzer available - requires post-processing",
            )

    def _optimize_trim_mutator(
        self, field_mapping: FieldMapping, operator: str, mutator: Dict[str, Any]
    ) -> "MutatorOptimizationResult":
        """Try to optimize a trim mutator using field mappings."""
        # Check if any text field might handle trimming
        # Most analyzers include trimming by default, but we can't be sure
        text_field = field_mapping.text_fields.get("standard")

        if text_field:
            # Assume standard analyzer handles trimming (common case)
            return MutatorOptimizationResult(
                can_optimize=True,
                selected_field=text_field,
                post_process_mutator=None,
                optimization_description=f"Assuming field '{text_field}' analyzer handles trimming",
            )
        else:
            # No text field - requires post-processing
            return MutatorOptimizationResult(
                can_optimize=False,
                selected_field=None,
                post_process_mutator=mutator,
                optimization_description="No text field available for trim optimization",
            )


@dataclass
class MutatorOptimizationResult:
    """Result of attempting to optimize a single mutator."""

    can_optimize: bool  # Whether mutator can be optimized away
    selected_field: Optional[str]  # Field to use in OpenSearch query
    post_process_mutator: Optional[Dict[str, Any]]  # Mutator for post-processing (if needed)
    optimization_description: str  # Description of what was done
    health_issue: Optional[Dict[str, str]] = None  # Health issue if any


# Monkey patch the analyzer into MutatorAnalyzer
# Method moved into class
