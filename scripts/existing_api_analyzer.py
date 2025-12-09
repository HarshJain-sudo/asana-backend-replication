"""
Existing API Analyzer Module

Scans Django project to identify all implemented API endpoints
by analyzing URL patterns and view classes.
"""

import os
import re
import ast
from pathlib import Path
from typing import Dict, List, Any, Set
from importlib import import_module


class ExistingAPIAnalyzer:
    """Analyzes existing Django APIs in the project."""
    
    def __init__(self, backend_dir: str):
        """
        Initialize analyzer with backend directory.
        
        Args:
            backend_dir: Path to backend directory containing apps
        """
        self.backend_dir = Path(backend_dir)
        self.apps = []
        self.endpoints = []
        
    def discover_asana_apps(self) -> List[str]:
        """
        Discover all asana_* Django apps.
        
        Returns:
            List of app names
        """
        print("Discovering Django apps...")
        
        apps = []
        for item in self.backend_dir.iterdir():
            if (item.is_dir() and 
                item.name.startswith('asana_') and
                (item / 'urls.py').exists()):
                apps.append(item.name)
        
        self.apps = sorted(apps)
        print(f"✓ Found {len(self.apps)} asana apps")
        
        return self.apps
    
    def analyze_all_apps(self) -> List[Dict[str, Any]]:
        """
        Analyze all discovered apps.
        
        Returns:
            List of endpoint dictionaries
        """
        if not self.apps:
            self.discover_asana_apps()
        
        print("\nAnalyzing existing APIs...")
        
        for app_name in self.apps:
            app_endpoints = self.analyze_app(app_name)
            self.endpoints.extend(app_endpoints)
        
        print(f"✓ Found {len(self.endpoints)} existing endpoints")
        
        return self.endpoints
    
    def analyze_app(self, app_name: str) -> List[Dict[str, Any]]:
        """
        Analyze single Django app for endpoints.
        
        Args:
            app_name: Name of Django app
            
        Returns:
            List of endpoint dictionaries
        """
        app_path = self.backend_dir / app_name
        urls_file = app_path / 'urls.py'
        
        if not urls_file.exists():
            return []
        
        endpoints = []
        
        try:
            # Parse URL patterns
            url_patterns = self._parse_url_file(urls_file)
            
            for pattern_info in url_patterns:
                endpoint = {
                    'app': app_name,
                    'path': pattern_info['path'],
                    'methods': pattern_info['methods'],
                    'view_class': pattern_info['view_class'],
                    'view_file': pattern_info['view_file'],
                    'name': pattern_info['name'],
                    'resource': self._extract_resource(app_name)
                }
                endpoints.append(endpoint)
        
        except Exception as e:
            print(f"  Warning: Failed to parse {app_name}: {e}")
        
        return endpoints
    
    def _parse_url_file(self, urls_file: Path) -> List[Dict[str, Any]]:
        """
        Parse Django urls.py file to extract patterns.
        
        Args:
            urls_file: Path to urls.py file
            
        Returns:
            List of URL pattern information
        """
        patterns = []
        
        with open(urls_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse imports to track view classes
        view_imports = self._extract_view_imports(content)
        
        # Find all path() calls
        path_pattern = r"path\(['\"]([^'\"]+)['\"],\s*([^,]+)\.as_view\(\)"
        matches = re.finditer(path_pattern, content)
        
        for match in matches:
            url_path = match.group(1)
            view_name = match.group(2)
            
            # Extract name parameter if present
            name_match = re.search(
                r"name=['\"]([^'\"]+)['\"]",
                content[match.start():match.start()+200]
            )
            url_name = name_match.group(1) if name_match else ''
            
            # Determine view file and methods
            view_file = view_imports.get(view_name, '')
            methods = self._detect_view_methods(view_file)
            
            patterns.append({
                'path': url_path,
                'view_class': view_name,
                'view_file': view_file,
                'methods': methods,
                'name': url_name
            })
        
        return patterns
    
    def _extract_view_imports(self, content: str) -> Dict[str, str]:
        """
        Extract view class imports from urls.py.
        
        Args:
            content: Content of urls.py file
            
        Returns:
            Dict mapping view class names to file paths
        """
        imports = {}
        
        # Pattern: from app.views.xxx import YyyView
        pattern = r"from ([^\s]+) import ([A-Z][a-zA-Z]+)"
        matches = re.finditer(pattern, content)
        
        for match in matches:
            module_path = match.group(1)
            class_name = match.group(2)
            
            # Convert module path to file path
            file_path = module_path.replace('.', '/') + '.py'
            imports[class_name] = file_path
        
        return imports
    
    def _detect_view_methods(self, view_file: str) -> List[str]:
        """
        Detect HTTP methods supported by view.
        
        Args:
            view_file: Relative path to view file
            
        Returns:
            List of HTTP methods (GET, POST, PUT, DELETE, PATCH)
        """
        if not view_file:
            return ['UNKNOWN']
        
        full_path = self.backend_dir / view_file
        
        if not full_path.exists():
            return ['UNKNOWN']
        
        try:
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Look for method definitions
            methods = []
            for method in ['get', 'post', 'put', 'delete', 'patch']:
                pattern = rf"def {method}\(self"
                if re.search(pattern, content):
                    methods.append(method.upper())
            
            return methods if methods else ['UNKNOWN']
        
        except Exception:
            return ['UNKNOWN']
    
    def _extract_resource(self, app_name: str) -> str:
        """
        Extract resource name from app name.
        
        Args:
            app_name: Django app name (e.g., 'asana_projects')
            
        Returns:
            Resource name (e.g., 'projects')
        """
        if app_name.startswith('asana_'):
            return app_name[6:]  # Remove 'asana_' prefix
        return app_name
    
    def get_endpoints_by_resource(self) -> Dict[str, List[Dict]]:
        """
        Organize endpoints by resource.
        
        Returns:
            Dict mapping resource names to endpoint lists
        """
        if not self.endpoints:
            self.analyze_all_apps()
        
        by_resource = {}
        for endpoint in self.endpoints:
            resource = endpoint['resource']
            if resource not in by_resource:
                by_resource[resource] = []
            by_resource[resource].append(endpoint)
        
        return by_resource
    
    def get_endpoint_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of existing endpoints.
        
        Returns:
            Dict containing summary statistics
        """
        if not self.endpoints:
            self.analyze_all_apps()
        
        by_resource = self.get_endpoints_by_resource()
        
        # Count by method
        method_counts = {}
        for endpoint in self.endpoints:
            for method in endpoint['methods']:
                method_counts[method] = method_counts.get(method, 0) + 1
        
        # Get unique paths
        unique_paths = set(e['path'] for e in self.endpoints)
        
        return {
            'total_endpoints': len(self.endpoints),
            'unique_paths': len(unique_paths),
            'apps': len(self.apps),
            'resources': list(by_resource.keys()),
            'resource_counts': {
                k: len(v) for k, v in by_resource.items()
            },
            'method_counts': method_counts
        }
    
    def normalize_path(self, path: str) -> str:
        """
        Normalize Django URL path to match OpenAPI format.
        
        Args:
            path: Django URL path with <type:name> parameters
            
        Returns:
            Normalized path with {name} parameters
        """
        # Convert Django <str:param> to OpenAPI {param}
        normalized = re.sub(
            r'<(?:str|int|uuid|slug):([^>]+)>',
            r'{\1}',
            path
        )
        
        # Ensure leading slash
        if not normalized.startswith('/'):
            normalized = '/' + normalized
        
        # Remove trailing slash if present
        if normalized.endswith('/') and len(normalized) > 1:
            normalized = normalized[:-1]
        
        return normalized
    
    def get_normalized_endpoints(self) -> List[Dict[str, Any]]:
        """
        Get endpoints with normalized paths.
        
        Returns:
            List of endpoints with normalized paths
        """
        if not self.endpoints:
            self.analyze_all_apps()
        
        normalized = []
        for endpoint in self.endpoints:
            endpoint_copy = endpoint.copy()
            endpoint_copy['normalized_path'] = self.normalize_path(
                endpoint['path']
            )
            normalized.append(endpoint_copy)
        
        return normalized


def main():
    """Test the analyzer."""
    import sys
    
    # Get backend directory
    backend_dir = Path(__file__).parent.parent
    
    analyzer = ExistingAPIAnalyzer(str(backend_dir))
    endpoints = analyzer.analyze_all_apps()
    
    print("\n" + "="*60)
    print("EXISTING API SUMMARY")
    print("="*60)
    
    summary = analyzer.get_endpoint_summary()
    print(f"\nTotal Endpoints: {summary['total_endpoints']}")
    print(f"Unique Paths: {summary['unique_paths']}")
    print(f"Django Apps: {summary['apps']}")
    
    print("\nEndpoints by HTTP Method:")
    for method, count in sorted(summary['method_counts'].items()):
        print(f"  {method}: {count}")
    
    print("\nEndpoints by Resource (top 10):")
    sorted_resources = sorted(
        summary['resource_counts'].items(),
        key=lambda x: x[1],
        reverse=True
    )[:10]
    for resource, count in sorted_resources:
        print(f"  {resource}: {count}")
    
    # Show sample endpoints
    print("\nSample Endpoints (first 5):")
    for endpoint in endpoints[:5]:
        methods_str = ', '.join(endpoint['methods'])
        print(f"  [{methods_str}] {endpoint['path']}")


if __name__ == '__main__':
    main()

