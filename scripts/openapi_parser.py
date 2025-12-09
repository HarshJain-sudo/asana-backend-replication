"""
OpenAPI Parser Module

Parses Asana's OpenAPI YAML specification to extract endpoint
information including paths, methods, parameters, request bodies,
and response schemas.
"""

import yaml
import requests
from typing import Dict, List, Any, Optional
from urllib.parse import urlparse


class OpenAPIParser:
    """Parses OpenAPI YAML specification."""
    
    def __init__(self, spec_url: str):
        """
        Initialize parser with OpenAPI specification URL.
        
        Args:
            spec_url: URL to OpenAPI YAML specification
        """
        self.spec_url = spec_url
        self.spec_data = None
        self.endpoints = []
        self.schemas = {}
        
    def download_spec(self) -> Dict[str, Any]:
        """
        Download OpenAPI specification from URL.
        
        Returns:
            Dict containing parsed YAML specification
        """
        print(f"Downloading OpenAPI spec from {self.spec_url}...")
        try:
            response = requests.get(self.spec_url, timeout=30)
            response.raise_for_status()
            self.spec_data = yaml.safe_load(response.text)
            print("✓ Successfully downloaded and parsed OpenAPI spec")
            return self.spec_data
        except requests.RequestException as e:
            raise Exception(
                f"Failed to download OpenAPI spec: {e}"
            )
        except yaml.YAMLError as e:
            raise Exception(f"Failed to parse YAML: {e}")
    
    def parse_spec(self) -> Dict[str, Any]:
        """
        Parse complete OpenAPI specification.
        
        Returns:
            Dict containing organized endpoint and schema data
        """
        if not self.spec_data:
            self.download_spec()
        
        print("\nParsing OpenAPI specification...")
        
        # Extract schemas/components
        self.schemas = self._extract_schemas()
        
        # Extract endpoints
        self.endpoints = self._extract_endpoints()
        
        print(f"✓ Parsed {len(self.endpoints)} endpoints")
        print(f"✓ Found {len(self.schemas)} schema definitions")
        
        return {
            'info': self.spec_data.get('info', {}),
            'servers': self.spec_data.get('servers', []),
            'endpoints': self.endpoints,
            'schemas': self.schemas,
            'tags': self.spec_data.get('tags', [])
        }
    
    def _extract_schemas(self) -> Dict[str, Any]:
        """Extract schema definitions from components."""
        components = self.spec_data.get('components', {})
        schemas = components.get('schemas', {})
        return schemas
    
    def _extract_endpoints(self) -> List[Dict[str, Any]]:
        """
        Extract all API endpoints from paths.
        
        Returns:
            List of endpoint dictionaries
        """
        paths = self.spec_data.get('paths', {})
        endpoints = []
        
        for path, path_item in paths.items():
            # Skip parameters at path level
            path_params = path_item.get('parameters', [])
            
            for method in ['get', 'post', 'put', 'delete', 'patch']:
                if method not in path_item:
                    continue
                
                operation = path_item[method]
                endpoint_data = self._parse_operation(
                    path,
                    method,
                    operation,
                    path_params
                )
                endpoints.append(endpoint_data)
        
        return endpoints
    
    def _parse_operation(
        self,
        path: str,
        method: str,
        operation: Dict[str, Any],
        path_params: List[Dict]
    ) -> Dict[str, Any]:
        """
        Parse individual operation details.
        
        Args:
            path: API endpoint path
            method: HTTP method
            operation: Operation object from OpenAPI spec
            path_params: Path-level parameters
            
        Returns:
            Dict containing parsed operation data
        """
        # Extract operation details
        operation_id = operation.get('operationId', '')
        summary = operation.get('summary', '')
        description = operation.get('description', '')
        tags = operation.get('tags', [])
        
        # Combine path and operation parameters
        all_params = path_params + operation.get('parameters', [])
        parameters = self._parse_parameters(all_params)
        
        # Parse request body
        request_body = self._parse_request_body(
            operation.get('requestBody', {})
        )
        
        # Parse responses
        responses = self._parse_responses(
            operation.get('responses', {})
        )
        
        # Determine resource type from tags or path
        resource = self._determine_resource(tags, path)
        
        return {
            'path': path,
            'method': method.upper(),
            'operation_id': operation_id,
            'summary': summary,
            'description': description,
            'tags': tags,
            'resource': resource,
            'parameters': parameters,
            'request_body': request_body,
            'responses': responses,
            'deprecated': operation.get('deprecated', False)
        }
    
    def _parse_parameters(
        self,
        params: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict]]:
        """
        Parse operation parameters.
        
        Args:
            params: List of parameter objects
            
        Returns:
            Dict organizing parameters by location
        """
        organized_params = {
            'path': [],
            'query': [],
            'header': [],
            'cookie': []
        }
        
        for param in params:
            # Handle parameter references
            if '$ref' in param:
                param = self._resolve_reference(param['$ref'])
            
            param_location = param.get('in', 'query')
            param_data = {
                'name': param.get('name', ''),
                'description': param.get('description', ''),
                'required': param.get('required', False),
                'schema': param.get('schema', {}),
                'example': param.get('example'),
                'deprecated': param.get('deprecated', False)
            }
            
            if param_location in organized_params:
                organized_params[param_location].append(param_data)
        
        return organized_params
    
    def _parse_request_body(
        self,
        request_body: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Parse request body schema."""
        if not request_body:
            return None
        
        content = request_body.get('content', {})
        json_content = content.get(
            'application/json',
            content.get('multipart/form-data', {})
        )
        
        if not json_content:
            return None
        
        schema = json_content.get('schema', {})
        
        return {
            'required': request_body.get('required', False),
            'description': request_body.get('description', ''),
            'schema': self._resolve_schema(schema)
        }
    
    def _parse_responses(
        self,
        responses: Dict[str, Any]
    ) -> Dict[str, Dict[str, Any]]:
        """
        Parse response definitions.
        
        Args:
            responses: Response objects from OpenAPI spec
            
        Returns:
            Dict mapping status codes to response details
        """
        parsed_responses = {}
        
        for status_code, response in responses.items():
            # Handle response references
            if '$ref' in response:
                response = self._resolve_reference(response['$ref'])
            
            content = response.get('content', {})
            json_content = content.get('application/json', {})
            
            parsed_responses[status_code] = {
                'description': response.get('description', ''),
                'schema': self._resolve_schema(
                    json_content.get('schema', {})
                ),
                'examples': json_content.get('examples', {})
            }
        
        return parsed_responses
    
    def _resolve_schema(self, schema: Dict[str, Any]) -> Dict[str, Any]:
        """
        Resolve schema with reference handling.
        
        Args:
            schema: Schema object possibly containing $ref
            
        Returns:
            Resolved schema dictionary
        """
        if not schema:
            return {}
        
        # Handle reference
        if '$ref' in schema:
            return self._resolve_reference(schema['$ref'])
        
        # Handle arrays
        if schema.get('type') == 'array':
            items = schema.get('items', {})
            schema['items'] = self._resolve_schema(items)
        
        # Handle object properties
        if schema.get('type') == 'object':
            properties = schema.get('properties', {})
            for prop_name, prop_schema in properties.items():
                properties[prop_name] = self._resolve_schema(prop_schema)
        
        # Handle allOf, anyOf, oneOf
        for keyword in ['allOf', 'anyOf', 'oneOf']:
            if keyword in schema:
                schema[keyword] = [
                    self._resolve_schema(s) for s in schema[keyword]
                ]
        
        return schema
    
    def _resolve_reference(self, ref: str) -> Dict[str, Any]:
        """
        Resolve $ref pointer to actual schema.
        
        Args:
            ref: Reference string (e.g., '#/components/schemas/Project')
            
        Returns:
            Referenced schema object
        """
        # Parse reference path
        parts = ref.split('/')
        
        # Navigate spec_data to find referenced object
        current = self.spec_data
        for part in parts:
            if part == '#':
                continue
            current = current.get(part, {})
        
        return current
    
    def _determine_resource(
        self,
        tags: List[str],
        path: str
    ) -> str:
        """
        Determine resource type from tags or path.
        
        Args:
            tags: Operation tags
            path: Endpoint path
            
        Returns:
            Resource name (e.g., 'projects', 'tasks')
        """
        # Use first tag if available
        if tags:
            return tags[0].lower()
        
        # Extract from path
        path_parts = [p for p in path.split('/') if p and not p.startswith('{')]
        if path_parts:
            return path_parts[0]
        
        return 'unknown'
    
    def get_endpoints_by_resource(self) -> Dict[str, List[Dict]]:
        """
        Organize endpoints by resource type.
        
        Returns:
            Dict mapping resource names to endpoint lists
        """
        if not self.endpoints:
            self.parse_spec()
        
        by_resource = {}
        for endpoint in self.endpoints:
            resource = endpoint['resource']
            if resource not in by_resource:
                by_resource[resource] = []
            by_resource[resource].append(endpoint)
        
        return by_resource
    
    def get_endpoint_summary(self) -> Dict[str, Any]:
        """
        Get summary statistics of parsed endpoints.
        
        Returns:
            Dict containing summary statistics
        """
        if not self.endpoints:
            self.parse_spec()
        
        by_resource = self.get_endpoints_by_resource()
        by_method = {}
        
        for endpoint in self.endpoints:
            method = endpoint['method']
            by_method[method] = by_method.get(method, 0) + 1
        
        return {
            'total_endpoints': len(self.endpoints),
            'resources': list(by_resource.keys()),
            'resource_counts': {
                k: len(v) for k, v in by_resource.items()
            },
            'method_counts': by_method,
            'deprecated_count': sum(
                1 for e in self.endpoints if e['deprecated']
            )
        }


def main():
    """Test the parser."""
    asana_spec_url = (
        "https://raw.githubusercontent.com/Asana/openapi/"
        "master/defs/asana_oas.yaml"
    )
    
    parser = OpenAPIParser(asana_spec_url)
    result = parser.parse_spec()
    
    print("\n" + "="*60)
    print("OPENAPI SPEC SUMMARY")
    print("="*60)
    
    summary = parser.get_endpoint_summary()
    print(f"\nTotal Endpoints: {summary['total_endpoints']}")
    print(f"Deprecated: {summary['deprecated_count']}")
    
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


if __name__ == '__main__':
    main()

