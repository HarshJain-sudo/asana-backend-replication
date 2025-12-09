"""
API Comparator Module

Compares OpenAPI specification with existing Django implementation
to identify missing APIs, extra APIs, and schema mismatches.
"""

from typing import Dict, List, Any, Set, Tuple
from datetime import datetime


class APIComparator:
    """Compares OpenAPI spec with existing implementation."""
    
    def __init__(
        self,
        openapi_endpoints: List[Dict[str, Any]],
        existing_endpoints: List[Dict[str, Any]]
    ):
        """
        Initialize comparator.
        
        Args:
            openapi_endpoints: Endpoints from OpenAPI spec
            existing_endpoints: Endpoints from Django implementation
        """
        self.openapi_endpoints = openapi_endpoints
        self.existing_endpoints = existing_endpoints
        self.missing_apis = []
        self.extra_apis = []
        self.matched_apis = []
        
    def compare(self) -> Dict[str, Any]:
        """
        Perform complete comparison.
        
        Returns:
            Dict containing comparison results
        """
        print("\nComparing OpenAPI spec with existing implementation...")
        
        # Build lookup sets
        spec_endpoints = self._build_endpoint_set(
            self.openapi_endpoints,
            'spec'
        )
        impl_endpoints = self._build_endpoint_set(
            self.existing_endpoints,
            'impl'
        )
        
        # Find missing (in spec but not implemented)
        self.missing_apis = self._find_missing(
            spec_endpoints,
            impl_endpoints
        )
        
        # Find extra (implemented but not in spec)
        self.extra_apis = self._find_extra(
            spec_endpoints,
            impl_endpoints
        )
        
        # Find matched
        self.matched_apis = self._find_matched(
            spec_endpoints,
            impl_endpoints
        )
        
        print(f"✓ Found {len(self.missing_apis)} missing APIs")
        print(f"✓ Found {len(self.extra_apis)} extra APIs")
        print(f"✓ Found {len(self.matched_apis)} matched APIs")
        
        return {
            'missing': self.missing_apis,
            'extra': self.extra_apis,
            'matched': self.matched_apis,
            'summary': self._generate_summary()
        }
    
    def _build_endpoint_set(
        self,
        endpoints: List[Dict[str, Any]],
        source: str
    ) -> Dict[str, Dict[str, Any]]:
        """
        Build lookup dictionary for endpoints.
        
        Args:
            endpoints: List of endpoint dictionaries
            source: 'spec' or 'impl'
            
        Returns:
            Dict mapping (method, path) to endpoint data
        """
        endpoint_set = {}
        
        for endpoint in endpoints:
            if source == 'spec':
                path = self._normalize_path(endpoint['path'])
                method = endpoint['method']
            else:  # impl
                path = self._normalize_path(endpoint.get(
                    'normalized_path',
                    endpoint['path']
                ))
                # Handle multiple methods per endpoint
                for method in endpoint['methods']:
                    if method == 'UNKNOWN':
                        continue
                    key = (method, path)
                    endpoint_set[key] = endpoint
                continue
            
            key = (method, path)
            endpoint_set[key] = endpoint
        
        return endpoint_set
    
    def _normalize_path(self, path: str) -> str:
        """
        Normalize path for comparison.
        
        Args:
            path: API path
            
        Returns:
            Normalized path
        """
        # Ensure leading slash
        if not path.startswith('/'):
            path = '/' + path
        
        # Remove trailing slash
        if path.endswith('/') and len(path) > 1:
            path = path[:-1]
        
        # Standardize path parameters
        # Convert both {param} and <type:param> to {param}
        import re
        path = re.sub(r'<(?:str|int|uuid|slug):([^>]+)>', r'{\1}', path)
        
        return path
    
    def _find_missing(
        self,
        spec_endpoints: Dict[Tuple[str, str], Dict],
        impl_endpoints: Dict[Tuple[str, str], Dict]
    ) -> List[Dict[str, Any]]:
        """
        Find APIs in spec but not implemented.
        
        Args:
            spec_endpoints: Spec endpoint lookup
            impl_endpoints: Implementation endpoint lookup
            
        Returns:
            List of missing API details
        """
        missing = []
        
        for key, spec_endpoint in spec_endpoints.items():
            if key not in impl_endpoints:
                method, path = key
                
                # Check for fuzzy match (different parameter names)
                fuzzy_match = self._find_fuzzy_match(
                    path,
                    method,
                    impl_endpoints
                )
                
                missing_info = {
                    'method': method,
                    'path': path,
                    'operation_id': spec_endpoint.get('operation_id', ''),
                    'summary': spec_endpoint.get('summary', ''),
                    'resource': spec_endpoint.get('resource', ''),
                    'tags': spec_endpoint.get('tags', []),
                    'parameters': spec_endpoint.get('parameters', {}),
                    'request_body': spec_endpoint.get('request_body'),
                    'responses': spec_endpoint.get('responses', {}),
                    'fuzzy_match': fuzzy_match,
                    'priority': self._calculate_priority(spec_endpoint)
                }
                
                missing.append(missing_info)
        
        # Sort by priority (high to low)
        missing.sort(key=lambda x: x['priority'], reverse=True)
        
        return missing
    
    def _find_extra(
        self,
        spec_endpoints: Dict[Tuple[str, str], Dict],
        impl_endpoints: Dict[Tuple[str, str], Dict]
    ) -> List[Dict[str, Any]]:
        """
        Find APIs implemented but not in spec.
        
        Args:
            spec_endpoints: Spec endpoint lookup
            impl_endpoints: Implementation endpoint lookup
            
        Returns:
            List of extra API details
        """
        extra = []
        
        for key, impl_endpoint in impl_endpoints.items():
            if key not in spec_endpoints:
                method, path = key
                
                extra_info = {
                    'method': method,
                    'path': path,
                    'app': impl_endpoint.get('app', ''),
                    'view_class': impl_endpoint.get('view_class', ''),
                    'resource': impl_endpoint.get('resource', '')
                }
                
                extra.append(extra_info)
        
        return extra
    
    def _find_matched(
        self,
        spec_endpoints: Dict[Tuple[str, str], Dict],
        impl_endpoints: Dict[Tuple[str, str], Dict]
    ) -> List[Dict[str, Any]]:
        """
        Find APIs present in both spec and implementation.
        
        Args:
            spec_endpoints: Spec endpoint lookup
            impl_endpoints: Implementation endpoint lookup
            
        Returns:
            List of matched API details
        """
        matched = []
        
        for key in spec_endpoints:
            if key in impl_endpoints:
                method, path = key
                spec_endpoint = spec_endpoints[key]
                impl_endpoint = impl_endpoints[key]
                
                matched_info = {
                    'method': method,
                    'path': path,
                    'operation_id': spec_endpoint.get('operation_id', ''),
                    'app': impl_endpoint.get('app', ''),
                    'view_class': impl_endpoint.get('view_class', ''),
                    'resource': spec_endpoint.get('resource', '')
                }
                
                matched.append(matched_info)
        
        return matched
    
    def _find_fuzzy_match(
        self,
        path: str,
        method: str,
        impl_endpoints: Dict[Tuple[str, str], Dict]
    ) -> bool:
        """
        Check if there's a fuzzy match for the path.
        
        Args:
            path: Path to match
            method: HTTP method
            impl_endpoints: Implementation endpoints
            
        Returns:
            True if fuzzy match found
        """
        # Extract path pattern (replace params with wildcard)
        import re
        pattern = re.sub(r'\{[^}]+\}', '*', path)
        
        for (impl_method, impl_path) in impl_endpoints.keys():
            if impl_method != method:
                continue
            
            impl_pattern = re.sub(r'\{[^}]+\}', '*', impl_path)
            if pattern == impl_pattern:
                return True
        
        return False
    
    def _calculate_priority(self, endpoint: Dict[str, Any]) -> int:
        """
        Calculate priority score for missing API.
        
        Higher priority = more important to implement
        
        Args:
            endpoint: Endpoint data
            
        Returns:
            Priority score (0-100)
        """
        score = 50  # Base score
        
        # Increase for common resources
        resource = endpoint.get('resource', '').lower()
        important_resources = [
            'tasks', 'projects', 'workspaces',
            'users', 'teams'
        ]
        if resource in important_resources:
            score += 20
        
        # Increase for common operations
        operation_id = endpoint.get('operation_id', '').lower()
        if any(op in operation_id for op in [
            'get', 'list', 'create', 'update', 'delete'
        ]):
            score += 15
        
        # Decrease for deprecated
        if endpoint.get('deprecated', False):
            score -= 30
        
        # Increase if has request body (usually POST/PUT)
        if endpoint.get('request_body'):
            score += 10
        
        return max(0, min(100, score))
    
    def _generate_summary(self) -> Dict[str, Any]:
        """
        Generate comparison summary.
        
        Returns:
            Summary dictionary
        """
        total_spec = len(self.openapi_endpoints)
        total_impl = len(self.existing_endpoints)
        
        # Calculate coverage
        coverage = 0
        if total_spec > 0:
            coverage = (len(self.matched_apis) / total_spec) * 100
        
        # Group missing by resource
        missing_by_resource = {}
        for api in self.missing_apis:
            resource = api['resource']
            if resource not in missing_by_resource:
                missing_by_resource[resource] = []
            missing_by_resource[resource].append(api)
        
        # Group by priority
        high_priority = [
            a for a in self.missing_apis if a['priority'] >= 70
        ]
        medium_priority = [
            a for a in self.missing_apis
            if 40 <= a['priority'] < 70
        ]
        low_priority = [
            a for a in self.missing_apis if a['priority'] < 40
        ]
        
        return {
            'total_in_spec': total_spec,
            'total_implemented': len(self.matched_apis),
            'total_missing': len(self.missing_apis),
            'total_extra': len(self.extra_apis),
            'coverage_percentage': round(coverage, 2),
            'missing_by_resource': {
                k: len(v) for k, v in missing_by_resource.items()
            },
            'priority_distribution': {
                'high': len(high_priority),
                'medium': len(medium_priority),
                'low': len(low_priority)
            }
        }
    
    def generate_report(self, output_file: str = None) -> str:
        """
        Generate detailed comparison report.
        
        Args:
            output_file: Optional file path to save report
            
        Returns:
            Report as markdown string
        """
        if not self.missing_apis and not self.extra_apis:
            # Run comparison if not done yet
            self.compare()
        
        report = self._build_markdown_report()
        
        if output_file:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(report)
            print(f"\n✓ Report saved to {output_file}")
        
        return report
    
    def _build_markdown_report(self) -> str:
        """Build markdown report."""
        summary = self._generate_summary()
        
        lines = [
            "# API Comparison Report",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "## Summary",
            "",
            f"- **Total endpoints in OpenAPI spec**: "
            f"{summary['total_in_spec']}",
            f"- **Total endpoints implemented**: "
            f"{summary['total_implemented']}",
            f"- **Missing endpoints**: {summary['total_missing']}",
            f"- **Extra endpoints**: {summary['total_extra']}",
            f"- **Coverage**: {summary['coverage_percentage']}%",
            "",
            "## Priority Distribution",
            "",
            f"- **High Priority** (≥70): "
            f"{summary['priority_distribution']['high']}",
            f"- **Medium Priority** (40-69): "
            f"{summary['priority_distribution']['medium']}",
            f"- **Low Priority** (<40): "
            f"{summary['priority_distribution']['low']}",
            "",
        ]
        
        # Missing APIs by resource
        if summary['missing_by_resource']:
            lines.extend([
                "## Missing APIs by Resource",
                "",
            ])
            
            for resource, count in sorted(
                summary['missing_by_resource'].items(),
                key=lambda x: x[1],
                reverse=True
            ):
                lines.append(f"- **{resource}**: {count} missing")
            
            lines.append("")
        
        # Detailed missing APIs
        if self.missing_apis:
            lines.extend([
                "## Missing APIs Details",
                "",
                "### High Priority",
                "",
            ])
            
            high_priority = [
                a for a in self.missing_apis if a['priority'] >= 70
            ]
            
            if high_priority:
                for api in high_priority[:20]:  # Show top 20
                    lines.extend(self._format_missing_api(api))
            else:
                lines.append("*None*")
                lines.append("")
            
            lines.extend([
                "### Medium Priority",
                "",
            ])
            
            medium_priority = [
                a for a in self.missing_apis
                if 40 <= a['priority'] < 70
            ]
            
            if medium_priority:
                for api in medium_priority[:15]:  # Show top 15
                    lines.extend(self._format_missing_api(api))
            else:
                lines.append("*None*")
                lines.append("")
        
        # Extra APIs
        if self.extra_apis:
            lines.extend([
                "## Extra APIs (Not in Spec)",
                "",
            ])
            
            for api in self.extra_apis[:20]:  # Show first 20
                lines.append(
                    f"- `{api['method']} {api['path']}` "
                    f"({api['app']})"
                )
            
            lines.append("")
        
        return '\n'.join(lines)
    
    def _format_missing_api(self, api: Dict[str, Any]) -> List[str]:
        """Format single missing API for report."""
        lines = [
            f"#### {api['method']} {api['path']}",
            "",
            f"- **Operation**: {api['operation_id']}",
            f"- **Summary**: {api['summary'][:100]}...",
            f"- **Resource**: {api['resource']}",
            f"- **Priority**: {api['priority']}/100",
        ]
        
        # Add parameters info
        params = api.get('parameters', {})
        path_params = params.get('path', [])
        query_params = params.get('query', [])
        
        if path_params:
            param_names = [p['name'] for p in path_params]
            lines.append(f"- **Path Params**: {', '.join(param_names)}")
        
        if query_params:
            param_names = [p['name'] for p in query_params[:5]]
            lines.append(f"- **Query Params**: {', '.join(param_names)}")
        
        lines.append("")
        
        return lines


def main():
    """Test the comparator."""
    from openapi_parser import OpenAPIParser
    from existing_api_analyzer import ExistingAPIAnalyzer
    from pathlib import Path
    
    print("Testing API Comparator...")
    
    # Parse OpenAPI spec
    asana_spec_url = (
        "https://raw.githubusercontent.com/Asana/openapi/"
        "master/defs/asana_oas.yaml"
    )
    parser = OpenAPIParser(asana_spec_url)
    spec_data = parser.parse_spec()
    
    # Analyze existing APIs
    backend_dir = Path(__file__).parent.parent
    analyzer = ExistingAPIAnalyzer(str(backend_dir))
    existing = analyzer.get_normalized_endpoints()
    
    # Compare
    comparator = APIComparator(
        spec_data['endpoints'],
        existing
    )
    results = comparator.compare()
    
    # Generate report
    report_file = backend_dir / 'api_comparison_report.md'
    comparator.generate_report(str(report_file))
    
    print("\n" + "="*60)
    print("COMPARISON COMPLETE")
    print("="*60)
    print(f"\nReport saved to: {report_file}")


if __name__ == '__main__':
    main()

