# OpenAPI Scraper & Django Code Generator

A comprehensive tool that scrapes Asana's OpenAPI specification and generates Django code for missing APIs, following clean architecture patterns.

## Features

- **OpenAPI Parsing**: Downloads and parses Asana's OpenAPI YAML specification
- **Existing API Analysis**: Scans Django project to identify implemented APIs
- **Intelligent Comparison**: Identifies missing, extra, and matched APIs
- **Code Generation**: Generates complete Django code following clean architecture
  - Views with OpenAPI schema decorators
  - Interactors for business logic
  - Storage interfaces and implementations
  - Presenters for response formatting
  - Serializers for request/response validation
- **Priority-Based**: Ranks missing APIs by importance
- **Dry-Run Mode**: Preview changes before generating files

## Architecture

The tool follows a modular architecture:

```
scripts/
├── generate_missing_apis.py    # Main orchestrator with CLI
├── openapi_parser.py            # OpenAPI YAML parser
├── existing_api_analyzer.py    # Django project analyzer
├── api_comparator.py            # Comparison engine
├── django_code_generator.py    # Code generator
├── generator_config.py          # Configuration & mappings
└── templates/                   # Jinja2 templates
    ├── view_template.py.j2
    ├── interactor_template.py.j2
    ├── storage_interface_template.py.j2
    ├── storage_implementation_template.py.j2
    ├── presenter_template.py.j2
    └── serializer_template.py.j2
```

## Installation

1. **Install Dependencies**:

```bash
cd backend
pip install -r requirements.txt
```

Required packages:
- `pyyaml>=6.0`
- `jinja2>=3.1.0`
- `requests>=2.31.0`

2. **Make Script Executable**:

```bash
chmod +x scripts/generate_missing_apis.py
```

## Usage

### 1. Generate Comparison Report Only

Analyze what's missing without generating code:

```bash
python3 scripts/generate_missing_apis.py --report-only
```

**Output**:
- `api_comparison_report.md` - Detailed comparison report
- Shows coverage percentage, missing APIs by resource, priority distribution

### 2. Preview Missing APIs

See top missing APIs without generating:

```bash
python3 scripts/generate_missing_apis.py
```

Shows top 10 missing APIs with priorities.

### 3. Preview with Filters

```bash
# Limit to specific resource
python3 scripts/generate_missing_apis.py --resource projects

# Show top 20
python3 scripts/generate_missing_apis.py --limit 20
```

### 4. Generate Code (Dry Run)

Preview what would be generated:

```bash
python3 scripts/generate_missing_apis.py --generate --dry-run --limit 5
```

### 5. Generate Code (Actual)

Generate Django code for missing APIs:

```bash
# Generate first 10 missing APIs
python3 scripts/generate_missing_apis.py --generate --limit 10

# Generate all missing APIs for a specific resource
python3 scripts/generate_missing_apis.py --generate --resource tasks

# Generate everything (use with caution!)
python3 scripts/generate_missing_apis.py --generate
```

**Output**:
- Generated view files in `asana_{resource}/views/{endpoint_name}/`
- Generated interactor files in `asana_{resource}/interactors/`
- Updated/created serializers in `asana_{resource}/serializers.py`
- `code_generation_summary_{timestamp}.md` with details

## CLI Options

```
--spec-url URL          OpenAPI specification URL (default: Asana's URL)
--output-dir PATH       Output directory for reports (default: backend/)
--report-only           Only generate comparison report
--generate              Generate Django code for missing APIs
--resource NAME         Filter by resource (e.g., projects, tasks)
--dry-run               Show what would be generated without creating files
--limit N               Limit number of APIs to generate
```

## Examples

### Example 1: Check Coverage

```bash
$ python3 scripts/generate_missing_apis.py --report-only

======================================================================
MISSING API GENERATOR
======================================================================

[1/4] Parsing OpenAPI Specification...
✓ Parsed 217 endpoints
✓ Found 244 schema definitions

[2/4] Analyzing Existing APIs...
✓ Found 49 existing endpoints

[3/4] Comparing Specifications...
✓ Found 193 missing APIs
  Coverage: 11.06%
  
✓ Report saved to: api_comparison_report.md
```

### Example 2: Generate Missing Project APIs

```bash
$ python3 scripts/generate_missing_apis.py --generate --resource projects --limit 5

[4/4] Generating Code...
  Filtered to resource: projects
  APIs to generate: 5

  [1/5] Generating POST /projects
  ✓ Generated view: asana_projects/views/create_project_view/create_project_view.py
  ✓ Generated interactor: asana_projects/interactors/create_project_interactor.py

  [2/5] Generating PUT /projects/{project_gid}
  ✓ Generated view: asana_projects/views/update_project_view/update_project_view.py
  ✓ Generated interactor: asana_projects/interactors/update_project_interactor.py

✓ Generation complete!
  Generated: 5 APIs
  Summary: code_generation_summary_20251210_120000.md
```

## Generated Code Structure

For each missing API, the tool generates:

### View File
Location: `asana_{resource}/views/{endpoint_name}/{endpoint_name}_view.py`

Features:
- Complete APIView class with appropriate HTTP method
- `@extend_schema` decorator with OpenAPI documentation
- `@ratelimit` decorator for rate limiting
- Request validation with serializers
- Error handling with proper Asana error format
- Integration with interactor layer

### Interactor File
Location: `asana_{resource}/interactors/{action}_interactor.py`

Features:
- Business logic class with dependency injection
- Storage interface integration
- Presenter interface integration
- Type hints and documentation

### Serializers
Location: `asana_{resource}/serializers.py`

Features:
- DRF serializers for request/response validation
- Based on OpenAPI schemas
- Validation rules from spec

## Post-Generation Steps

After generating code, you need to:

1. **Update URL Patterns**:
   - Add view imports to `urls.py`
   - Add URL patterns for new endpoints

2. **Implement Business Logic**:
   - Complete TODOs in generated interactors
   - Add storage layer methods if needed

3. **Run Migrations**:
   - If new models were referenced
   - `python manage.py makemigrations`
   - `python manage.py migrate`

4. **Add Tests**:
   - Create test cases for new endpoints
   - Test request/response validation
   - Test error cases

5. **Review & Refine**:
   - Review generated code
   - Adjust to project standards
   - Add missing validations

## Generated Code Example

### View (Simplified)

```python
class CreateProjectView(APIView):
    @ratelimit(key='ip', rate='5/s', method='POST')
    @extend_schema(
        request=CreateProjectRequestSerializer,
        responses={201: CreateProjectResponseSerializer},
        summary="Create a project",
        tags=["Projects"]
    )
    def post(self, request):
        storage = StorageImplementation()
        presenter = CreateProjectPresenterImplementation()
        interactor = CreateProjectInteractor(storage, presenter)
        
        serializer = CreateProjectRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(errors, status=400)
        
        response = interactor.create_project(**serializer.validated_data)
        return Response(response, status=201)
```

## Configuration

### Resource Mappings

Edit `generator_config.py` to customize:

```python
RESOURCE_APP_MAPPING = {
    'tasks': 'asana_tasks',
    'projects': 'asana_projects',
    # Add your custom mappings
}
```

### Rate Limits

```python
DEFAULT_RATE_LIMITS = {
    'GET': '10/s',
    'POST': '5/s',
    # Customize as needed
}
```

### Skip Conditions

```python
def should_skip_endpoint(endpoint: Dict) -> bool:
    # Skip deprecated
    if endpoint.get('deprecated', False):
        return True
    # Add custom skip logic
    return False
```

## Troubleshooting

### Import Errors

If you get import errors:
```bash
# Ensure you're in the backend directory
cd backend
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python3 scripts/generate_missing_apis.py
```

### Missing Dependencies

```bash
pip install pyyaml jinja2 requests
```

### Network Issues

If OpenAPI spec download fails:
```bash
# Download manually and use local file
wget https://raw.githubusercontent.com/Asana/openapi/master/defs/asana_oas.yaml
python3 scripts/generate_missing_apis.py --spec-url file:///path/to/asana_oas.yaml
```

## Testing Individual Modules

Each module can be tested independently:

```bash
# Test OpenAPI parser
python3 scripts/openapi_parser.py

# Test existing API analyzer
python3 scripts/existing_api_analyzer.py

# Test comparator
python3 scripts/api_comparator.py

# Test code generator
python3 scripts/django_code_generator.py
```

## Comparison Report

The comparison report includes:

- **Summary**: Coverage percentage, total missing/extra APIs
- **Priority Distribution**: High/Medium/Low priority counts
- **Missing by Resource**: Breakdown of missing APIs per resource
- **Detailed List**: All missing APIs with:
  - HTTP method and path
  - Operation ID
  - Summary and description
  - Parameters required
  - Priority score

## Code Generation Summary

The generation summary includes:

- **Statistics**: Total APIs generated, errors encountered
- **Generated APIs**: For each API:
  - Endpoint (method + path)
  - Operation ID
  - Files generated with full paths
- **Next Steps**: Manual steps required after generation

## Best Practices

1. **Start Small**: Generate a few APIs first, test them, then generate more
2. **Use Dry Run**: Always preview with `--dry-run` first
3. **Filter by Resource**: Focus on one resource at a time
4. **Review Generated Code**: Generated code is a starting point
5. **Test Thoroughly**: Add comprehensive tests for generated endpoints
6. **Commit Incrementally**: Commit after each successful batch

## Limitations

- **Schema Parsing**: Complex nested schemas may need manual adjustment
- **Business Logic**: Generated interactors have placeholder logic
- **Model Creation**: Doesn't create Django models (assumes they exist)
- **Authentication**: Doesn't generate authentication logic
- **Relationships**: Complex model relationships need manual implementation

## Future Enhancements

- [ ] Full schema-to-serializer generation
- [ ] Model generation from OpenAPI schemas
- [ ] Test case generation
- [ ] URL pattern auto-updating
- [ ] Interactive mode for confirming each generation
- [ ] Support for custom templates
- [ ] Migration generation
- [ ] Documentation generation

## Contributing

To extend the tool:

1. **Add Templates**: Create new Jinja2 templates in `templates/`
2. **Update Config**: Modify `generator_config.py` for new mappings
3. **Extend Generator**: Add methods to `django_code_generator.py`
4. **Test Changes**: Run with `--dry-run` first

## License

Part of the Scalar Assignment project.

## Support

For issues or questions:
1. Check the comparison report for coverage details
2. Use `--dry-run` to preview changes
3. Test individual modules to isolate issues
4. Review generated code for TODOs and placeholders

