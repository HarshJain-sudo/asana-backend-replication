"""
Django Code Generator Module

Generates Django views, interactors, storage, presenters, and
serializers following clean architecture pattern.
"""

import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from jinja2 import Environment, FileSystemLoader
import re

from generator_config import (
    get_app_name,
    get_model_name,
    get_operation_type,
    generate_class_name,
    generate_function_name,
    get_python_type,
    HTTP_METHOD_TO_FUNCTION,
    DEFAULT_RATE_LIMITS,
    SUCCESS_STATUS_CODES,
    ERROR_RESPONSE_FUNCTIONS,
    OPENAPI_TO_DRF_FIELD,
)


class DjangoCodeGenerator:
    """Generates Django code from OpenAPI specification."""
    
    def __init__(self, backend_dir: str, templates_dir: str = None):
        """
        Initialize code generator.
        
        Args:
            backend_dir: Path to Django backend directory
            templates_dir: Path to Jinja2 templates directory
        """
        self.backend_dir = Path(backend_dir)
        
        if templates_dir is None:
            templates_dir = Path(__file__).parent / 'templates'
        
        self.templates_dir = Path(templates_dir)
        
        # Setup Jinja2 environment
        self.jinja_env = Environment(
            loader=FileSystemLoader(str(self.templates_dir)),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        self.generated_files = []
    
    def generate_api(
        self,
        endpoint: Dict[str, Any],
        dry_run: bool = False
    ) -> Dict[str, str]:
        """
        Generate complete API implementation for endpoint.
        
        Args:
            endpoint: Endpoint data from OpenAPI spec
            dry_run: If True, don't write files
            
        Returns:
            Dict mapping component types to file paths
        """
        resource = endpoint['resource']
        app_name = get_app_name(resource)
        operation_id = endpoint['operation_id']
        
        print(f"\nGenerating {endpoint['method']} {endpoint['path']}")
        print(f"  App: {app_name}")
        print(f"  Operation: {operation_id}")
        
        # Prepare context data
        context = self._prepare_context(endpoint)
        
        generated = {}
        
        # Generate view
        view_path = self._generate_view(
            app_name,
            operation_id,
            context,
            dry_run
        )
        if view_path:
            generated['view'] = view_path
        
        # Generate interactor (for POST/PUT/DELETE)
        if endpoint['method'] in ['POST', 'PUT', 'DELETE', 'PATCH']:
            interactor_path = self._generate_interactor(
                app_name,
                operation_id,
                context,
                dry_run
            )
            if interactor_path:
                generated['interactor'] = interactor_path
        
        # Generate serializers if needed
        if endpoint.get('request_body') or endpoint.get('responses'):
            serializer_path = self._generate_serializers(
                app_name,
                operation_id,
                context,
                dry_run
            )
            if serializer_path:
                generated['serializer'] = serializer_path
        
        return generated
    
    def _prepare_context(
        self,
        endpoint: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Prepare template context from endpoint data.
        
        Args:
            endpoint: Endpoint data
            
        Returns:
            Context dict for templates
        """
        resource = endpoint['resource']
        app_name = get_app_name(resource)
        operation_id = endpoint['operation_id']
        method = endpoint['method']
        path = endpoint['path']
        
        # Generate names
        view_class = generate_class_name(operation_id, 'View')
        interactor_class = generate_class_name(operation_id, 'Interactor')
        presenter_class = generate_class_name(
            operation_id,
            'PresenterImplementation'
        )
        method_name = HTTP_METHOD_TO_FUNCTION.get(method, 'get')
        interactor_method = generate_function_name(operation_id)
        
        # Parse parameters
        path_params = self._parse_parameters(
            endpoint.get('parameters', {}).get('path', [])
        )
        query_params = self._parse_parameters(
            endpoint.get('parameters', {}).get('query', [])
        )
        
        # Parse request body
        request_body = endpoint.get('request_body')
        has_request_body = request_body is not None
        request_serializer = None
        
        if has_request_body:
            request_serializer = self._generate_serializer_name(
                operation_id,
                'Request'
            )
        
        # Parse responses
        responses = self._parse_responses(
            endpoint.get('responses', {}),
            operation_id
        )
        
        # Determine operation type
        operation_type = get_operation_type(operation_id, method, path)
        
        # Build context
        context = {
            # Basic info
            'app_name': app_name,
            'resource': resource,
            'resource_tag': resource.capitalize(),
            'operation_id': operation_id,
            'method': method,
            'path': path,
            'summary': endpoint.get('summary', ''),
            'description': endpoint.get('description', ''),
            
            # Class/function names
            'view_class': view_class,
            'interactor_class': interactor_class,
            'presenter_class': presenter_class,
            'method_name': method_name,
            'interactor_method': interactor_method,
            
            # Modules
            'interactor_module': self._to_snake_case(interactor_class),
            'presenter_module': self._to_snake_case(presenter_class),
            
            # Parameters
            'path_parameters': path_params,
            'query_parameters': query_params,
            
            # Request/Response
            'has_request_body': has_request_body,
            'request_body': request_body,
            'request_serializer': request_serializer,
            'responses': responses,
            
            # Configuration
            'rate_limit': DEFAULT_RATE_LIMITS.get(method, '5/s'),
            'success_status': SUCCESS_STATUS_CODES.get(
                method,
                '200_OK'
            ),
            
            # Flags
            'has_interactor': method in [
                'POST', 'PUT', 'DELETE', 'PATCH'
            ],
            'operation_type': operation_type,
            
            # Imports
            'serializers': [],
            'exceptions': [],
            'error_responses': ERROR_RESPONSE_FUNCTIONS,
            
            # Descriptions
            'view_description': endpoint.get('summary', ''),
            'action_description': self._generate_action_description(
                operation_id,
                resource
            ),
        }
        
        return context
    
    def _parse_parameters(
        self,
        params: List[Dict]
    ) -> List[Dict[str, Any]]:
        """Parse parameters for template."""
        parsed = []
        
        for param in params:
            schema = param.get('schema', {})
            param_type = schema.get('type', 'string')
            
            parsed.append({
                'name': param['name'],
                'type': 'str',  # For type hints
                'description': param.get('description', ''),
                'required': param.get('required', False),
                'schema_type': param_type,
            })
        
        return parsed
    
    def _parse_responses(
        self,
        responses: Dict[str, Any],
        operation_id: str
    ) -> Dict[str, Dict[str, Any]]:
        """Parse responses for template."""
        parsed = {}
        
        for status_code, response in responses.items():
            serializer_name = None
            
            # Generate response serializer name for success responses
            status_str = str(status_code)
            if status_str.startswith('2'):
                serializer_name = self._generate_serializer_name(
                    operation_id,
                    'Response'
                )
            
            examples = []
            response_examples = response.get('examples', {})
            for ex_name, ex_data in response_examples.items():
                examples.append({
                    'name': ex_name,
                    'value': ex_data.get('value', {})
                })
            
            parsed[status_code] = {
                'description': response.get('description', ''),
                'serializer': serializer_name,
                'examples': examples
            }
        
        return parsed
    
    def _generate_serializer_name(
        self,
        operation_id: str,
        suffix: str
    ) -> str:
        """Generate serializer class name."""
        base_name = generate_class_name(operation_id, '')
        return f"{base_name}{suffix}Serializer"
    
    def _generate_action_description(
        self,
        operation_id: str,
        resource: str
    ) -> str:
        """Generate human-readable action description."""
        action = generate_function_name(operation_id).replace('_', ' ')
        return f"{action} for {resource}"
    
    def _to_snake_case(self, text: str) -> str:
        """Convert PascalCase to snake_case."""
        # Insert underscore before capitals
        text = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', text)
        text = re.sub('([a-z0-9])([A-Z])', r'\1_\2', text)
        return text.lower()
    
    def _generate_view(
        self,
        app_name: str,
        operation_id: str,
        context: Dict[str, Any],
        dry_run: bool
    ) -> Optional[str]:
        """Generate view file."""
        template = self.jinja_env.get_template('view_template.py.j2')
        code = template.render(**context)
        
        # Determine file path
        view_name = self._to_snake_case(context['view_class'])
        view_dir = (
            self.backend_dir / app_name / 'views' / view_name
        )
        view_file = view_dir / f'{view_name}.py'
        
        if not dry_run:
            view_dir.mkdir(parents=True, exist_ok=True)
            
            with open(view_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Create __init__.py
            init_file = view_dir / '__init__.py'
            if not init_file.exists():
                init_file.touch()
            
            self.generated_files.append(str(view_file))
            print(f"  ✓ Generated view: {view_file}")
        else:
            print(f"  [DRY RUN] Would generate: {view_file}")
        
        return str(view_file)
    
    def _generate_interactor(
        self,
        app_name: str,
        operation_id: str,
        context: Dict[str, Any],
        dry_run: bool
    ) -> Optional[str]:
        """Generate interactor file."""
        template = self.jinja_env.get_template(
            'interactor_template.py.j2'
        )
        
        # Prepare interactor-specific context
        interactor_context = {
            'app_name': app_name,
            'class_name': context['interactor_class'],
            'class_description': context['action_description'],
            'method_name': context['interactor_method'],
            'method_description': context['description'],
            'parameters': [],  # TODO: Extract from request body
            'validation_logic': [],
            'storage_calls': [],
            'business_logic': [],
            'response_fields': [],
            'presenter_method': 'get_response',
            'exceptions': [],
            'raises': [],
            'exception_descriptions': {},
        }
        
        code = template.render(**interactor_context)
        
        # Determine file path
        interactor_name = self._to_snake_case(
            context['interactor_class']
        )
        interactor_file = (
            self.backend_dir / app_name / 'interactors' /
            f'{interactor_name}.py'
        )
        
        if not dry_run:
            interactor_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(interactor_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            self.generated_files.append(str(interactor_file))
            print(f"  ✓ Generated interactor: {interactor_file}")
        else:
            print(
                f"  [DRY RUN] Would generate: {interactor_file}"
            )
        
        return str(interactor_file)
    
    def _generate_serializers(
        self,
        app_name: str,
        operation_id: str,
        context: Dict[str, Any],
        dry_run: bool
    ) -> Optional[str]:
        """Generate or update serializers file."""
        serializer_file = (
            self.backend_dir / app_name / 'serializers.py'
        )
        
        # For now, just create a placeholder
        # In a full implementation, this would parse the schema
        # and generate complete serializers
        
        if not dry_run and not serializer_file.exists():
            content = '"""\nSerializers for {} API endpoints.\n"""\n'.format(
                context['resource']
            )
            content += 'from rest_framework import serializers\n\n'
            
            with open(serializer_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"  ✓ Created serializers file: {serializer_file}")
        
        return str(serializer_file)
    
    def generate_url_pattern(
        self,
        endpoint: Dict[str, Any]
    ) -> str:
        """
        Generate Django URL pattern for endpoint.
        
        Args:
            endpoint: Endpoint data
            
        Returns:
            URL pattern string
        """
        path = endpoint['path']
        operation_id = endpoint['operation_id']
        
        # Convert OpenAPI path to Django path
        django_path = path
        
        # Convert {param} to <str:param>
        django_path = re.sub(
            r'\{([^}]+)\}',
            r'<str:\1>',
            django_path
        )
        
        # Remove leading slash
        if django_path.startswith('/'):
            django_path = django_path[1:]
        
        # Generate view import and pattern
        view_class = generate_class_name(operation_id, 'View')
        view_name = self._to_snake_case(view_class)
        url_name = self._to_snake_case(operation_id)
        
        pattern = (
            f"path('{django_path}', "
            f"{view_class}.as_view(), "
            f"name='{url_name}'),"
        )
        
        return pattern
    
    def get_generated_files(self) -> List[str]:
        """Get list of generated file paths."""
        return self.generated_files


def main():
    """Test the generator."""
    from openapi_parser import OpenAPIParser
    
    print("Testing Django Code Generator...")
    
    # Parse OpenAPI spec
    asana_spec_url = (
        "https://raw.githubusercontent.com/Asana/openapi/"
        "master/defs/asana_oas.yaml"
    )
    parser = OpenAPIParser(asana_spec_url)
    spec_data = parser.parse_spec()
    
    # Get first non-deprecated endpoint
    test_endpoint = None
    for endpoint in spec_data['endpoints']:
        if not endpoint.get('deprecated', False):
            test_endpoint = endpoint
            break
    
    if test_endpoint:
        backend_dir = Path(__file__).parent.parent
        generator = DjangoCodeGenerator(str(backend_dir))
        
        # Generate in dry-run mode
        generated = generator.generate_api(test_endpoint, dry_run=True)
        
        print("\n" + "="*60)
        print("TEST GENERATION COMPLETE")
        print("="*60)
        print(f"\nTest endpoint: {test_endpoint['method']} "
              f"{test_endpoint['path']}")
        print(f"Operation: {test_endpoint['operation_id']}")
        print("\nWould generate:")
        for component, path in generated.items():
            print(f"  - {component}: {path}")


if __name__ == '__main__':
    main()

