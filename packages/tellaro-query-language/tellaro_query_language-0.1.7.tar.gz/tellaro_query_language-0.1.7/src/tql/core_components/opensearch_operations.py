"""OpenSearch operations for TQL.

This module handles all OpenSearch-specific operations including query conversion,
execution, and result processing.
"""

import os
from typing import Any, Dict, List, Optional, Union

from ..exceptions import TQLExecutionError
from ..mutator_analyzer import MutatorAnalysisResult, MutatorAnalyzer
from ..opensearch import OpenSearchBackend
from ..parser import TQLParser
from ..post_processor import QueryPostProcessor


class OpenSearchOperations:
    """Handles OpenSearch-specific operations for TQL."""

    def __init__(self, parser: TQLParser, field_mappings: Dict[str, Any], enhanced_mappings: Dict[str, Any]):
        """Initialize OpenSearch operations.

        Args:
            parser: TQL parser instance
            field_mappings: Field mapping configuration
            enhanced_mappings: Enhanced field mappings with analyzer info
        """
        self.parser = parser
        self.field_mappings = field_mappings
        self.enhanced_mappings = enhanced_mappings
        self.has_analyzer_info = any(mapping.is_enhanced_mapping() for mapping in self.enhanced_mappings.values())

    def to_opensearch(self, query: str) -> Dict[str, Any]:
        """Convert TQL query to OpenSearch query format.

        Args:
            query: TQL query string

        Returns:
            OpenSearch query dictionary

        Raises:
            TQLParseError: If query parsing fails
        """
        # Parse the query
        ast = self.parser.parse(query)

        # Create OpenSearch backend
        backend = OpenSearchBackend(field_mappings=self.field_mappings)

        # Convert to OpenSearch query
        opensearch_query = backend.convert(ast)

        return opensearch_query

    def to_opensearch_dsl(self, query: str) -> Dict[str, Any]:
        """Convert TQL query to OpenSearch DSL format.

        This is an alias for to_opensearch() for backward compatibility.

        Args:
            query: TQL query string

        Returns:
            OpenSearch DSL query dictionary
        """
        return self.to_opensearch(query)

    def analyze_opensearch_query(self, query: str) -> Union[MutatorAnalysisResult, Dict[str, Any]]:
        """Analyze a TQL query for OpenSearch optimization opportunities.

        This method examines mutator usage and field mappings to determine:
        1. Which mutators can be pushed to OpenSearch (Phase 1)
        2. Which mutators must be applied post-query (Phase 2)
        3. How field mappings affect operator choices

        Args:
            query: TQL query string

        Returns:
            MutatorAnalysisResult if mutators present, otherwise analysis dict
        """
        # Parse the query
        ast = self.parser.parse(query)

        # If there are no mutators, just analyze for field mapping optimizations
        if not self._has_mutators(ast):
            backend = OpenSearchBackend(field_mappings=self.field_mappings)
            os_query = backend.convert(ast)

            return {
                "has_mutators": False,
                "original_query": query,
                "opensearch_query": os_query,
                "optimizations": self._analyze_field_optimizations(ast),
            }

        # Create analyzer
        analyzer = MutatorAnalyzer(self.enhanced_mappings)

        # Analyze the AST
        return analyzer.analyze_ast(ast)

    def _has_mutators(self, ast: Dict[str, Any]) -> bool:
        """Check if AST contains any mutators."""
        if isinstance(ast, dict):
            # Check for mutators in current node
            if ast.get("field_mutators") or ast.get("value_mutators"):
                return True

            # Check for special expressions (geo, nslookup)
            if ast.get("type") in ["geo_expr", "nslookup_expr"]:
                return True

            # Recursively check child nodes
            for key, value in ast.items():
                if key in ["left", "right", "operand", "filter", "conditions"]:
                    if self._has_mutators(value):
                        return True

        return False

    def _analyze_field_optimizations(self, ast: Dict[str, Any]) -> List[Dict[str, str]]:
        """Analyze field-specific optimizations based on mappings."""
        optimizations = []

        # Check if we have analyzer information
        if self.has_analyzer_info:
            optimizations.append(
                {
                    "type": "field_mapping",
                    "description": "Enhanced field mappings with analyzer information available",
                    "benefit": "Queries optimized based on field types and analyzers",
                }
            )

        return optimizations

    def execute_opensearch(  # noqa: C901
        self,
        query: str,
        index: Optional[str] = None,
        size: int = 10000,
        from_: int = 0,
        sort: Optional[List[Dict[str, Any]]] = None,
        source_includes: Optional[List[str]] = None,
        source_excludes: Optional[List[str]] = None,
        track_total_hits: Union[bool, int] = True,
        explain: bool = False,
        timeout: int = 30,
        preference: Optional[str] = None,
        routing: Optional[str] = None,
        request_cache: Optional[bool] = None,
        terminate_after: Optional[int] = None,
        search_type: Optional[str] = None,
        scroll: Optional[str] = None,
        client: Optional[Any] = None,
        timestamp_field: str = "@timestamp",
        time_range: Optional[Dict[str, str]] = None,
        scan_all: bool = False,
        scroll_size: int = 1000,
        scroll_timeout: str = "5m",
        **kwargs,
    ) -> Union[List[Dict[str, Any]], Dict[str, Any]]:
        """Execute TQL query against OpenSearch and return results.

        This method handles the complete query execution pipeline:
        1. Parse TQL query and analyze mutators
        2. Generate optimized OpenSearch query (Phase 1)
        3. Execute query against OpenSearch
        4. Apply post-processing mutators (Phase 2)
        5. Apply any result filtering

        Args:
            query: TQL query string
            index: OpenSearch index name (uses environment variable if not provided)
            size: Maximum number of results to return (default: 10000)
            from_: Offset for pagination (default: 0)
            sort: List of sort specifications
            source_includes: Fields to include in response
            source_excludes: Fields to exclude from response
            track_total_hits: Whether to track total hit count
            explain: Include score explanation
            timeout: Query timeout
            preference: Query routing preference
            routing: Custom routing value
            request_cache: Whether to use request cache
            terminate_after: Maximum documents to collect per shard
            search_type: Search execution type
            scroll: Scroll timeout for scroll API
            client: Optional OpenSearch client instance (for testing)
            timestamp_field: Field name for timestamp filtering
            time_range: Optional time range dict with 'gte' and/or 'lte' keys
            scan_all: If True, use scroll API to retrieve all matching documents
            scroll_size: Size per scroll when scan_all=True
            scroll_timeout: Scroll timeout when scan_all=True
            **kwargs: Additional OpenSearch parameters

        Returns:
            List of matching documents with mutators applied, or full response dict if raw=True

        Raises:
            TQLParseError: If query parsing fails
            TQLExecutionError: If OpenSearch execution fails
            ImportError: If opensearch-py is not installed
        """
        try:
            from opensearchpy import OpenSearch
        except ImportError:
            raise ImportError("opensearch-py package is required for OpenSearch queries")

        # Get index from environment if not provided
        if index is None:
            index = os.getenv("OPENSEARCH_INDEX")
            if not index:
                raise ValueError("OpenSearch index must be provided or set in OPENSEARCH_INDEX environment variable")

        # Parse the query first to check if it's a stats query
        ast = self.parser.parse(query)

        # Initialize variables that might be used later
        opensearch_query = None
        needs_phase2 = False

        # Check if this is a stats query
        is_stats_query = ast.get("type") in ["stats_expr", "query_with_stats"]

        if is_stats_query:
            # Handle stats queries differently
            from ..opensearch_stats import OpenSearchStatsTranslator

            translator = OpenSearchStatsTranslator()

            # Determine the filter and stats parts
            if ast.get("type") == "query_with_stats":
                # Has a filter before stats
                filter_ast = ast.get("filter")
                stats_ast = ast.get("stats")

                # Convert filter to OpenSearch query
                backend = OpenSearchBackend(field_mappings=self.field_mappings)
                if filter_ast:
                    filter_query = backend.convert(filter_ast)["query"]
                else:
                    filter_query = {"match_all": {}}
            else:
                # Pure stats query
                stats_ast = ast
                filter_query = {"match_all": {}}

            # Build aggregations
            if stats_ast:
                stats_result = translator.translate_stats(stats_ast, self.field_mappings)
            else:
                stats_result = {"aggs": {}}

            # Extract the aggregations (translate_stats returns {"aggs": {...}})
            aggregations = stats_result.get("aggs", {})

            # Build the complete query
            opensearch_query = {"query": filter_query, "aggs": aggregations}
            needs_phase2 = False
            has_mutators = False
        else:
            # Parse and analyze the query normally
            analysis_result = self.analyze_opensearch_query(query)

            # Determine if we have mutators
            has_mutators = isinstance(analysis_result, MutatorAnalysisResult)

        if not is_stats_query:
            if has_mutators and isinstance(analysis_result, MutatorAnalysisResult):
                # Use optimized AST (Phase 1) for OpenSearch
                phase1_ast = analysis_result.optimized_ast
                backend = OpenSearchBackend(field_mappings=self.field_mappings)
                opensearch_query = backend.convert(phase1_ast)

                # Check if we need Phase 2 (post-processing)
                needs_phase2 = bool(analysis_result.post_processing_requirements)
                # Phase 2 will be handled by post_processing_requirements
            else:
                # No mutators, use original query
                assert isinstance(analysis_result, dict)
                opensearch_query = analysis_result["opensearch_query"]
                needs_phase2 = False
                # No phase 2 needed for non-mutator queries

        # Use provided client or create OpenSearch client
        if client is None:
            client = OpenSearch(
                hosts=[
                    {
                        "host": os.getenv("OPENSEARCH_HOST", "localhost"),
                        "port": int(os.getenv("OPENSEARCH_PORT", "9200")),
                    }
                ],
                http_auth=(
                    (os.getenv("OPENSEARCH_USERNAME", "admin"), os.getenv("OPENSEARCH_PASSWORD", "admin"))
                    if os.getenv("OPENSEARCH_USERNAME")
                    else None
                ),
                use_ssl=os.getenv("OPENSEARCH_USE_SSL", "false").lower() == "true",
                verify_certs=os.getenv("OPENSEARCH_VERIFY_CERTS", "false").lower() == "true",
                ssl_show_warn=False,
            )

        # Build search body
        # opensearch_query already contains {"query": {...}} from backend.convert()
        if opensearch_query is None:
            raise ValueError("Failed to generate OpenSearch query")
        search_body = opensearch_query.copy()

        # Handle time range filtering
        if time_range is None:
            # Default time range: last 15 minutes
            time_range = {"gte": "now-15m", "lte": "now"}

        # Add time range filter to the query
        if time_range:
            base_query = search_body.get("query", {})
            time_filter = {"range": {timestamp_field: time_range}}

            # Wrap the existing query with time filter
            if base_query:
                search_body["query"] = {"bool": {"must": [base_query, time_filter]}}
            else:
                search_body["query"] = time_filter

        search_body.update({"size": size, "from": from_, "track_total_hits": track_total_hits})

        # Add optional parameters
        if sort:
            search_body["sort"] = sort
        if source_includes or source_excludes:
            search_body["_source"] = {}
            if source_includes:
                search_body["_source"]["includes"] = source_includes
            if source_excludes:
                search_body["_source"]["excludes"] = source_excludes
        if explain:
            search_body["explain"] = explain

        # Add any additional parameters from kwargs
        search_body.update(kwargs)

        # Build search parameters
        search_params: Dict[str, Any] = {"index": index, "body": search_body, "timeout": timeout}

        # Add optional search parameters
        if preference:
            search_params["preference"] = preference
        if routing:
            search_params["routing"] = routing
        if request_cache is not None:
            search_params["request_cache"] = request_cache
        if terminate_after:
            search_params["terminate_after"] = terminate_after
        if search_type:
            search_params["search_type"] = search_type
        if scroll:
            search_params["scroll"] = scroll

        # Initialize scroll tracking
        scroll_count = 0

        # Handle scan_all functionality with scroll API
        if scan_all:
            all_hits = []
            search_params["scroll"] = scroll_timeout
            search_params["body"]["size"] = scroll_size
            # Remove from parameter for scroll API
            search_params["body"].pop("from", None)

            try:
                # Initial search
                response = client.search(**search_params)
                hits = response.get("hits", {}).get("hits", [])
                all_hits.extend(hits)
                scroll_count += 1

                scroll_id = response.get("_scroll_id")

                # Continue scrolling until no more results
                while scroll_id and hits:
                    scroll_response = client.scroll(scroll_id=scroll_id, scroll=scroll_timeout)

                    hits = scroll_response.get("hits", {}).get("hits", [])
                    all_hits.extend(hits)
                    scroll_id = scroll_response.get("_scroll_id")
                    scroll_count += 1

                # Clean up scroll
                if scroll_id:
                    try:
                        client.clear_scroll(scroll_id=scroll_id)
                    except Exception:
                        pass  # Ignore cleanup errors

                # Create a response structure that mimics regular search
                response = {"hits": {"total": {"value": len(all_hits)}, "hits": all_hits}}

            except Exception as e:
                raise TQLExecutionError(f"OpenSearch scroll query failed: {str(e)}")
        else:
            # Regular search
            try:
                response = client.search(**search_params)
            except Exception as e:
                raise TQLExecutionError(f"OpenSearch query failed: {str(e)}")

        # Handle stats query results differently
        if is_stats_query:
            # Process stats aggregation results
            aggs_response = response.get("aggregations", {})

            # Format the stats results based on the test expectations
            # Use the correct stats AST
            if ast.get("type") == "query_with_stats":
                stats_ast = ast.get("stats")
            else:
                stats_ast = ast

            # Extract aggregation info
            if stats_ast:
                aggregations = stats_ast.get("aggregations", [])
                group_by_fields = stats_ast.get("group_by", [])
            else:
                aggregations = []
                group_by_fields = []

            # Format results differently based on whether we have grouping
            if group_by_fields:
                # For grouped stats, we need to extract buckets
                if stats_ast:
                    buckets = self._extract_grouped_buckets(aggs_response, group_by_fields, aggregations, stats_ast)
                else:
                    buckets = []

                # For multiple aggregations, include all operations
                operations = [agg.get("function") for agg in aggregations]
                fields = [agg.get("field") for agg in aggregations]

                stats_results = {
                    "type": "stats_grouped",
                    "operation": operations[0] if len(operations) == 1 else operations,
                    "field": fields[0] if len(fields) == 1 else fields,
                    "results": buckets,  # Array of buckets for grouped results
                    "group_by": group_by_fields,
                }
            else:
                # Simple aggregations without grouping
                if aggregations:
                    if len(aggregations) == 1:
                        # Single aggregation
                        first_agg = aggregations[0]
                        func = first_agg.get("function", "")
                        field = first_agg.get("field", "*")

                        # Get the aggregation result
                        # The alias is typically func_field_0 for the first aggregation
                        alias = first_agg.get("alias") or f"{func}_{field}_0"
                        agg_result = aggs_response.get(alias, {})

                        # Extract the value based on aggregation type
                        if func == "count":
                            value = agg_result.get("value", 0)
                        elif func in ["sum", "min", "max", "avg", "average"]:
                            value = agg_result.get("value", 0)
                        elif func == "unique_count":
                            value = agg_result.get("value", 0)
                        elif func in ["percentile", "percentiles", "p", "pct"]:
                            # Percentiles return a values dict
                            values_dict = agg_result.get("values", {})
                            # For a single percentile, extract the value
                            if len(values_dict) == 1:
                                value = list(values_dict.values())[0]
                            else:
                                value = values_dict
                        elif func in ["values", "unique"]:
                            # Extract buckets from terms aggregation
                            buckets = agg_result.get("buckets", [])
                            value = [bucket["key"] for bucket in buckets]
                        else:
                            value = agg_result

                        stats_results = {
                            "type": "stats",
                            "operation": func,
                            "field": field,
                            "values": value,
                            "group_by": [],
                        }
                    else:
                        # Multiple aggregations
                        results = {}
                        for i, agg in enumerate(aggregations):
                            func = agg.get("function", "")
                            field = agg.get("field", "*")
                            alias = agg.get("alias") or f"{func}_{field}_{i}"
                            agg_result = aggs_response.get(alias, {})

                            # Extract the value based on aggregation type
                            if func == "count":
                                value = agg_result.get("value", 0)
                            elif func in ["sum", "min", "max", "avg", "average"]:
                                value = agg_result.get("value", 0)
                            elif func == "unique_count":
                                value = agg_result.get("value", 0)
                            elif func in ["percentile", "percentiles", "p", "pct"]:
                                # Percentiles return a values dict
                                values_dict = agg_result.get("values", {})
                                # For a single percentile, extract the value
                                if len(values_dict) == 1:
                                    value = list(values_dict.values())[0]
                                else:
                                    value = values_dict
                            elif func in ["values", "unique"]:
                                # Extract buckets from terms aggregation
                                buckets = agg_result.get("buckets", [])
                                value = [bucket["key"] for bucket in buckets]
                            else:
                                value = agg_result

                            key = agg.get("alias") or f"{func}_{field}"
                            results[key] = value

                        stats_results = {
                            "type": "stats",
                            "results": results,
                        }
                else:
                    stats_results = {"type": "stats", "operation": "unknown", "field": "*", "values": 0, "group_by": []}

            # Extract hits if size > 0
            hits = response.get("hits", {}).get("hits", [])
            documents = []
            if size > 0 and hits:
                for hit in hits:
                    doc = hit["_source"].copy()
                    # Preserve metadata
                    if "_id" in hit:
                        doc["_id"] = hit["_id"]
                    if "_score" in hit:
                        doc["_score"] = hit["_score"]
                    documents.append(doc)

            # Return in the expected format
            result = {
                "results": documents,
                "total": response.get("hits", {}).get("total", {}).get("value", 0),
                "stats": stats_results,
                "post_processing_applied": False,
                "health_status": "HEALTHY",
                "health_reasons": [],
                "performance_impact": {"overhead_ms": 0, "mutators_applied": 0},
                "scan_info": {"used_scan": False},
            }

            # Add query_type if documents were requested
            if size > 0:
                result["query_type"] = "stats_with_docs"

            return result

        # Extract hits for regular queries
        hits = response.get("hits", {}).get("hits", [])
        total_hits = response.get("hits", {}).get("total", {}).get("value", 0)

        # Process results based on whether we need Phase 2
        if needs_phase2:
            # Apply Phase 2 processing
            processor = QueryPostProcessor()

            # Extract documents from hits
            documents = []
            hit_metadata = []
            for hit in hits:
                documents.append(hit["_source"])
                hit_metadata.append(
                    {
                        "_id": hit.get("_id"),
                        "_score": hit.get("_score"),
                        "_explanation": hit.get("_explanation") if explain else None,
                    }
                )

            # First apply mutators to all documents
            if isinstance(analysis_result, MutatorAnalysisResult):
                processed_docs = processor.process_results(
                    documents,
                    analysis_result.post_processing_requirements,
                    track_enrichments=kwargs.get("save_enrichment", False),
                )

                # Then filter results based on requirements (e.g., ALL operator, contains with mutators)
                filtered_docs = processor.filter_results(processed_docs, analysis_result.post_processing_requirements)
            else:
                # No post-processing needed
                processed_docs = documents
                filtered_docs = documents

            # Build final results with preserved metadata
            results = []
            for doc in filtered_docs:
                # Find the original hit metadata for this document
                # This is a simple approach - in production you might want to track IDs
                for i, orig_doc in enumerate(documents):
                    if orig_doc == doc or self._docs_match(orig_doc, doc):
                        # Add metadata
                        if hit_metadata[i]["_id"]:
                            doc["_id"] = hit_metadata[i]["_id"]
                        if hit_metadata[i]["_score"]:
                            doc["_score"] = hit_metadata[i]["_score"]
                        if hit_metadata[i]["_explanation"]:
                            doc["_explanation"] = hit_metadata[i]["_explanation"]
                        break
                results.append(doc)
        else:
            # No Phase 2 needed, just extract documents
            results = []
            for hit in hits:
                doc = hit["_source"].copy()
                # Preserve metadata
                if "_id" in hit:
                    doc["_id"] = hit["_id"]
                if "_score" in hit:
                    doc["_score"] = hit["_score"]
                if explain and "explanation" in hit:
                    doc["_explanation"] = hit["explanation"]
                results.append(doc)

        # Return raw response if requested
        if kwargs.get("raw_response", False):
            return {
                "took": response.get("took"),
                "timed_out": response.get("timed_out"),
                "hits": {
                    "total": response.get("hits", {}).get("total"),
                    "max_score": response.get("hits", {}).get("max_score"),
                    "hits": results,
                },
            }

        # Build performance impact info
        performance_impact = {
            "has_post_processing": needs_phase2,
            "impacted_fields": [],
            "mutator_types": [],
            "estimated_overhead": "low",
        }

        if needs_phase2 and isinstance(analysis_result, MutatorAnalysisResult):
            impacted_fields = set()
            mutator_types = set()

            for req in analysis_result.post_processing_requirements:
                impacted_fields.add(req.field_name)
                for mutator in req.mutators:
                    mutator_types.add(mutator.get("name", "unknown"))

            performance_impact["impacted_fields"] = list(impacted_fields)
            performance_impact["mutator_types"] = list(mutator_types)

            # Estimate overhead based on mutator types
            expensive_mutators = {"nslookup", "geoip_lookup", "geo"}
            if any(m in mutator_types for m in expensive_mutators):
                performance_impact["estimated_overhead"] = "high"
            elif len(mutator_types) > 2:
                performance_impact["estimated_overhead"] = "medium"

        # Determine health status
        if needs_phase2:
            health_status = "yellow"
            health_reasons = ["Post-processing required - results may be incomplete with pagination"]
        else:
            health_status = "green"
            health_reasons = []

        # Get opensearch total before filtering
        opensearch_total = total_hits

        result = {
            "results": results,
            "total": len(results),
            "returned": len(results),  # Alias for total
            "opensearch_total": opensearch_total,
            "post_processing_applied": needs_phase2,
            "health_status": health_status,
            "health_reasons": health_reasons,
            "performance_impact": performance_impact,
            "optimizations_applied": [],  # TODO: Track actual optimizations  # noqa: W0511
            "opensearch_query": (
                opensearch_query.get("query", {}) if opensearch_query else {}
            ),  # Include the query that was sent
            "time_range": time_range,
            "timestamp_field": timestamp_field,
            "query_type": "regular",  # Regular query (not stats)
            "scan_info": {
                "used_scan": scan_all,
                "scroll_size": scroll_size if scan_all else None,
                "scroll_timeout": scroll_timeout if scan_all else None,
                "scroll_count": scroll_count if scan_all else None,
                "documents_retrieved": len(results) if scan_all else None,
                "estimated_total": total_hits if scan_all else None,
            },
        }

        # Add pagination info for non-scan queries
        if not scan_all:
            result["pagination"] = {
                "size": size,
                "from": from_,
                "total": opensearch_total,
                "has_more": opensearch_total > (from_ + len(results)),
            }

        return result

    def _docs_match(self, doc1: Dict[str, Any], doc2: Dict[str, Any]) -> bool:
        """Check if two documents are the same (accounting for mutations).

        This is a simple implementation - in production you'd want something more robust.
        """
        # If they have the same _id, they match
        if "_id" in doc1 and "_id" in doc2 and doc1["_id"] == doc2["_id"]:
            return True

        # Otherwise do a simple comparison of a few key fields
        # This is imperfect but works for most cases
        key_fields = ["id", "name", "hostname", "@timestamp"]
        for field in key_fields:
            if field in doc1 and field in doc2 and doc1[field] == doc2[field]:
                return True

        return False

    def _extract_grouped_buckets(  # noqa: C901
        self,
        aggs_response: Dict[str, Any],
        group_by_fields: List[str],
        aggregations: List[Dict[str, Any]],
        stats_ast: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Extract buckets from grouped aggregation response.

        Args:
            aggs_response: OpenSearch aggregations response
            group_by_fields: List of fields used for grouping
            aggregations: List of aggregation specifications
            stats_ast: The stats AST for reference

        Returns:
            List of bucket dictionaries with group keys and aggregation values
        """
        buckets = []

        # For single-level grouping
        if len(group_by_fields) == 1:
            field = group_by_fields[0]
            # Look for the terms aggregation with the group field name
            terms_agg_name = f"group_by_{field}"

            # The aggregation might be named differently, check for it
            # OpenSearch stats translator uses the field name directly
            if field in aggs_response:
                buckets_data = aggs_response[field].get("buckets", [])
            elif terms_agg_name in aggs_response:
                buckets_data = aggs_response[terms_agg_name].get("buckets", [])
            else:
                # Try to find any terms aggregation
                for _key, value in aggs_response.items():
                    if isinstance(value, dict) and "buckets" in value:
                        buckets_data = value["buckets"]
                        break
                else:
                    buckets_data = []

            # Process each bucket
            for bucket in buckets_data:
                bucket_result = {field: bucket.get("key")}

                # Extract aggregation values
                for i, agg in enumerate(aggregations):
                    func = agg.get("function", "")
                    field_name = agg.get("field", "*")
                    alias = agg.get("alias") or f"{func}_{field_name}_{i}"

                    # Map function names to expected output names
                    output_key = func
                    if func == "avg":
                        output_key = "average"
                    elif func == "unique_count":
                        output_key = "distinct_count"

                    if alias in bucket:
                        agg_value = bucket[alias]
                        # Extract the actual value
                        if isinstance(agg_value, dict) and "value" in agg_value:
                            bucket_result[output_key] = agg_value["value"]
                        else:
                            bucket_result[output_key] = agg_value
                    else:
                        # Try without index suffix for first aggregation
                        simple_alias = f"{func}_{field_name}"
                        if simple_alias in bucket:
                            agg_value = bucket[simple_alias]
                            if isinstance(agg_value, dict) and "value" in agg_value:
                                bucket_result[output_key] = agg_value["value"]
                            else:
                                bucket_result[output_key] = agg_value

                buckets.append(bucket_result)

        else:
            # Multi-level grouping - need to traverse nested structure
            # Start with the outermost grouping
            current_agg = aggs_response

            # Find the first group_by aggregation
            for field in group_by_fields:
                group_key = f"group_by_{field}"
                if group_key in current_agg:
                    current_agg = current_agg[group_key]
                    break
                elif field in current_agg:
                    current_agg = current_agg[field]
                    break

            # Process nested buckets recursively
            if "buckets" in current_agg:
                buckets = self._process_nested_buckets(current_agg["buckets"], group_by_fields, aggregations, 0)

        return buckets

    def _process_nested_buckets(  # noqa: C901
        self,
        buckets_data: List[Dict[str, Any]],
        group_by_fields: List[str],
        aggregations: List[Dict[str, Any]],
        level: int,
    ) -> List[Dict[str, Any]]:
        """Process nested buckets for multi-level grouping.

        Args:
            buckets_data: List of bucket data from OpenSearch
            group_by_fields: List of fields used for grouping
            aggregations: List of aggregation specifications
            level: Current nesting level (0-based)

        Returns:
            Flattened list of bucket results
        """
        results = []

        for bucket in buckets_data:
            # Get the key for this level
            field_name = group_by_fields[level]
            bucket_key = {field_name: bucket.get("key")}

            # Check if there are more levels
            if level + 1 < len(group_by_fields):
                # Look for the next level's aggregation
                next_field = group_by_fields[level + 1]
                next_group_key = f"group_by_{next_field}"

                if next_group_key in bucket and "buckets" in bucket[next_group_key]:
                    # Recursively process nested buckets
                    nested_results = self._process_nested_buckets(
                        bucket[next_group_key]["buckets"], group_by_fields, aggregations, level + 1
                    )

                    # Merge current key with nested results
                    for nested in nested_results:
                        merged = bucket_key.copy()
                        merged.update(nested)
                        results.append(merged)
            else:
                # This is the innermost level - extract aggregation values
                result = bucket_key.copy()

                # Extract aggregation values
                for i, agg in enumerate(aggregations):
                    func = agg.get("function", "")
                    field_name = agg.get("field", "*")
                    alias = agg.get("alias") or f"{func}_{field_name}_{i}"

                    # Map function names to expected output names
                    output_key = func
                    if func == "avg":
                        output_key = "average"
                    elif func == "unique_count":
                        output_key = "distinct_count"

                    if alias in bucket:
                        agg_value = bucket[alias]
                        # Extract the actual value
                        if isinstance(agg_value, dict) and "value" in agg_value:
                            result[output_key] = agg_value["value"]
                        else:
                            result[output_key] = agg_value
                    else:
                        # Try without index suffix for first aggregation
                        simple_alias = f"{func}_{field_name}"
                        if simple_alias in bucket:
                            agg_value = bucket[simple_alias]
                            if isinstance(agg_value, dict) and "value" in agg_value:
                                result[output_key] = agg_value["value"]
                            else:
                                result[output_key] = agg_value

                results.append(result)

        return results
