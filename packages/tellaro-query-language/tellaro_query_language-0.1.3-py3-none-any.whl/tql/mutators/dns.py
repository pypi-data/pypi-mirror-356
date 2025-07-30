"""DNS lookup mutator."""

import ipaddress
import socket
from typing import Any, Dict, List, Optional

try:
    import dns.rdataclass
    import dns.rdatatype
    import dns.resolver

    dns_available = True
except ImportError:
    dns_available = False
    dns = None  # type: ignore

from ..validators import validate_field
from .base import BaseMutator, PerformanceClass, append_to_result


class NSLookupMutator(BaseMutator):
    """
    Enrichment mutator that performs DNS lookups on hostnames or IP addresses.

    Performance Characteristics:
    - In-memory: SLOW - Network I/O for DNS queries (can be mitigated with caching)
    - OpenSearch: SLOW - Network I/O plus post-processing overhead

    This mutator can:
    - Perform forward DNS lookups (hostname to IP)
    - Perform reverse DNS lookups (IP to hostname)
    - Query specific DNS record types
    - Support force lookup to bypass existing data
    - Return enriched data without modifying the original field value

    Parameters:
        servers: List of DNS server IPs to use (optional)
        append_field: Field name to store results (default: field_name + '_resolved')
        force: Force new lookup even if data exists (default: False)
        save: Save enrichment to record (default: True)
        types: List of DNS record types to query (default: auto-detect)
        field: Field name to store results (preferred over append_field)

    Example:
        hostname | nslookup(servers=['8.8.8.8']) contains 'google.com'
    """

    def __init__(self, params: Optional[Dict[str, Any]] = None) -> None:
        super().__init__(params)
        self.is_enrichment = True
        # DNS lookups are slow due to network I/O
        self.performance_in_memory = PerformanceClass.SLOW
        # Even slower in OpenSearch context due to post-processing overhead
        self.performance_opensearch = PerformanceClass.SLOW

    def apply(self, field_name: str, record: Dict[str, Any], value: Any) -> Any:  # noqa: C901
        # Handle different input types
        if value is None:
            return None

        if isinstance(value, str):
            queries = [value]
        elif isinstance(value, list) and all(isinstance(item, str) for item in value):
            queries = value
        else:
            return None  # Return None for invalid input types instead of raising

        # Check if we should force lookup
        force_lookup = self.params.get("force", False)
        save_enrichment = self.params.get("save", True)

        # Check if DNS data already exists in the record
        # Determine where to store the enrichment data
        # Priority: field parameter > append_field parameter > default location

        # Check for explicit field parameter first
        if "field" in self.params:
            append_field = self.params["field"]
        elif "append_field" in self.params:
            # Legacy parameter support
            append_field = self.params["append_field"]
        else:
            # Default behavior: use 'domain' as the field name
            # If field is like destination.ip, it should be destination.domain
            # If field is just ip, it should be domain
            if "." in field_name:
                # Nested field like destination.ip
                parent_path = field_name.rsplit(".", 1)[0]
                append_field = parent_path + ".domain"
            else:
                # Top-level field
                append_field = "domain"
        existing_dns_data = None

        # Check for existing data at the append field location
        parts = append_field.split(".")
        current: Optional[Dict[str, Any]] = record
        for part in parts[:-1]:
            if isinstance(current, dict) and part in current:
                current = current[part]
            else:
                current = None
                break

        if current and isinstance(current, dict) and parts[-1] in current:
            existing_dns_data = current[parts[-1]]

        # If not forcing and DNS data exists, return it
        if not force_lookup and existing_dns_data:
            return existing_dns_data

        # Get custom DNS servers from parameters, if provided.
        servers = self.params.get("servers")
        if servers is not None:
            if not validate_field(servers, [(list, str)]):
                raise ValueError("The 'servers' parameter must be a list of IP address strings.")
            for srv in servers:
                try:
                    ipaddress.ip_address(srv)
                except ValueError:
                    raise ValueError(f"Invalid DNS server address: {srv}")

        # Get requested DNS record types
        requested_types = self.params.get("types", [])

        resolved_results: Dict[str, Any] = {}

        for query_value in queries:
            # Auto-detect if this is an IP address (for reverse lookup)
            is_ip = False
            try:
                ipaddress.ip_address(query_value)
                is_ip = True
            except ValueError:
                pass

            if servers is not None or requested_types:
                # Use dnspython for advanced queries
                if not dns_available:
                    raise ImportError(
                        "dnspython is required for nslookup with custom servers or specific record types."
                    )

                resolver = dns.resolver.Resolver()
                if servers is not None:
                    resolver.nameservers = servers

                records_list = []

                # Determine which record types to query
                if requested_types:
                    # Use explicitly requested types
                    query_types = requested_types
                elif is_ip:
                    # Auto-detect: reverse lookup for IPs
                    query_types = ["PTR"]
                else:
                    # Auto-detect: common forward lookup types
                    query_types = ["A", "AAAA"]

                # Perform queries for each record type
                for record_type in query_types:
                    try:
                        # Handle reverse lookups for PTR records
                        if record_type == "PTR" and is_ip:
                            # Convert IP to reverse DNS format
                            # Use the already imported ipaddress module
                            ip_obj = ipaddress.ip_address(query_value)
                            if isinstance(ip_obj, ipaddress.IPv4Address):
                                # IPv4 reverse format: 4.3.2.1.in-addr.arpa
                                octets = str(ip_obj).split(".")
                                reverse_name = ".".join(reversed(octets)) + ".in-addr.arpa"
                            else:
                                # IPv6 reverse format
                                hex_str = ip_obj.exploded.replace(":", "")
                                reverse_name = ".".join(reversed(hex_str)) + ".ip6.arpa"

                            answer = resolver.resolve(reverse_name, record_type)
                        else:
                            # Regular forward lookup
                            answer = resolver.resolve(query_value, record_type)

                        for rdata in answer:
                            record_dict = {
                                "class": dns.rdataclass.to_text(rdata.rdclass) if hasattr(rdata, "rdclass") else "IN",
                                "data": rdata.to_text().rstrip("."),  # Remove trailing dot from FQDNs
                                "name": str(answer.qname).rstrip(".") if hasattr(answer, "qname") else query_value,
                                "ttl": answer.ttl if hasattr(answer, "ttl") else 0,
                                "type": record_type,
                            }
                            records_list.append(record_dict)
                    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.resolver.Timeout, Exception):
                        # Continue to next record type if this one fails
                        continue

                # Convert to ECS-compliant structure
                if records_list:
                    resolved_results[query_value] = self._format_dns_ecs(query_value, records_list, query_types)
                else:
                    resolved_results[query_value] = self._format_dns_ecs(query_value, [], query_types)
            else:
                # Fallback to socket for basic lookups
                try:
                    if is_ip:
                        # Reverse lookup
                        hostname, _, _ = socket.gethostbyaddr(query_value)
                        records = [{"class": "IN", "data": hostname, "name": query_value, "ttl": 0, "type": "PTR"}]
                        resolved_results[query_value] = self._format_dns_ecs(query_value, records, ["PTR"])
                    else:
                        # Forward lookup
                        infos = socket.getaddrinfo(query_value, None)
                        ips = list({str(info[4][0]) for info in infos})
                        records = []
                        for ip in ips:
                            # Determine record type based on IP version
                            try:
                                ip_obj = ipaddress.ip_address(ip)
                                record_type = "A" if ip_obj.version == 4 else "AAAA"
                            except ValueError:
                                record_type = "A"  # Default to A record

                            records.append(
                                {"class": "IN", "data": ip, "name": query_value, "ttl": 0, "type": record_type}
                            )
                        resolved_results[query_value] = self._format_dns_ecs(
                            query_value, records, ["A", "AAAA"] if not is_ip else ["PTR"]
                        )
                except Exception:
                    resolved_results[query_value] = self._format_dns_ecs(
                        query_value, [], ["A", "AAAA"] if not is_ip else ["PTR"]
                    )

        # Save enrichment if requested
        if save_enrichment:
            # For single value lookups, unwrap the result
            if len(queries) == 1 and queries[0] in resolved_results:
                # Store the ECS data directly, not wrapped in IP key
                append_to_result(record, append_field, resolved_results[queries[0]])
            else:
                # For multiple queries, keep the dictionary structure
                append_to_result(record, append_field, resolved_results)

        # For enrichment-only mode, return the resolved data
        # This allows it to be used in geo-style parenthetical expressions
        return resolved_results

    def _format_dns_ecs(  # noqa: C901
        self, query_value: str, records: List[Dict[str, Any]], query_types: List[str]
    ) -> Dict[str, Any]:
        """Format DNS results in ECS-compliant structure.

        Args:
            query_value: The original query (hostname or IP)
            records: List of DNS records returned
            query_types: List of DNS record types that were queried

        Returns:
            ECS-compliant DNS data structure
        """
        # Build ECS structure
        ecs_data = {
            "question": {"name": query_value, "type": query_types[0] if query_types else "A"},  # Primary query type
            "answers": records,
            "response_code": "NOERROR" if records else "NXDOMAIN",
        }

        # Extract specific data for convenience fields
        resolved_ips = []
        hostnames = []
        mx_records = []
        txt_records = []

        for record in records:
            record_type = record.get("type", "")
            data = record.get("data", "")

            if record_type in ["A", "AAAA"] and data:
                resolved_ips.append(data)
            elif record_type == "PTR" and data:
                hostnames.append(data)
            elif record_type == "CNAME" and data:
                hostnames.append(data)
            elif record_type == "MX" and data:
                mx_records.append(data)
            elif record_type == "TXT" and data:
                txt_records.append(data)

        # Add resolved_ip array (ECS standard field)
        if resolved_ips:
            ecs_data["resolved_ip"] = resolved_ips

        # Add convenience fields for easier access
        if hostnames:
            ecs_data["hostname"] = hostnames[0]  # Single hostname for simple access
            ecs_data["hostnames"] = hostnames  # Array of all hostnames

        # Add record type specific arrays for convenience
        if resolved_ips:
            # Separate IPv4 and IPv6
            ipv4 = [ip for ip in resolved_ips if ":" not in ip]
            ipv6 = [ip for ip in resolved_ips if ":" in ip]
            if ipv4:
                ecs_data["a"] = ipv4
            if ipv6:
                ecs_data["aaaa"] = ipv6

        if hostnames and any(r.get("type") == "PTR" for r in records):
            ecs_data["ptr"] = hostnames[0]  # Backward compatibility

        if mx_records:
            ecs_data["mx"] = mx_records

        if txt_records:
            ecs_data["txt"] = txt_records

        return ecs_data
