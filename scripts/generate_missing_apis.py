#!/usr/bin/env python3
"""
Generate Missing APIs - Main Orchestrator Script

Coordinates OpenAPI parsing, existing API analysis, comparison,
and Django code generation.
"""

import argparse
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

from openapi_parser import OpenAPIParser
from existing_api_analyzer import ExistingAPIAnalyzer
from api_comparator import APIComparator
from django_code_generator import DjangoCodeGenerator
from generator_config import should_skip_endpoint


class MissingAPIGenerator:
    """Main orchestrator for missing API generation."""
    
    def __init__(
        self,
        spec_url: str,
        backend_dir: str,
        output_dir: str = None
    ):
        """
        Initialize generator.
        
        Args:
            spec_url: URL to OpenAPI specification
            backend_dir: Path to Django backend directory
            output_dir: Optional output directory for reports
        """
        self.spec_url = spec_url
        self.backend_dir = Path(backend_dir)
        
        if output_dir:
            self.output_dir = Path(output_dir)
        else:
            self.output_dir = self.backend_dir
        
        self.parser = None
        self.analyzer = None
        self.comparator = None
        self.generator = None
        
        self.spec_data = None
        self.existing_data = None
        self.comparison_results = None
    
    def run(
        self,
        report_only: bool = False,
        generate: bool = False,
        resource_filter: str = None,
        dry_run: bool = False,
        limit: int = None
    ) -> Dict[str, Any]:
        """
        Run the complete workflow.
        
        Args:
            report_only: Only generate comparison report
            generate: Generate code for missing APIs
            resource_filter: Filter by resource name
            dry_run: Show what would be generated
            limit: Limit number of APIs to generate
            
        Returns:
            Dict containing results
        """
        print("="*70)
        print("MISSING API GENERATOR")
        print("="*70)
        
        # Step 1: Parse OpenAPI spec
        print("\n[1/4] Parsing OpenAPI Specification...")
        self.parser = OpenAPIParser(self.spec_url)
        self.spec_data = self.parser.parse_spec()
        
        spec_summary = self.parser.get_endpoint_summary()
        print(f"  Found {spec_summary['total_endpoints']} endpoints")
        print(f"  Resources: {len(spec_summary['resources'])}")
        
        # Step 2: Analyze existing APIs
        print("\n[2/4] Analyzing Existing APIs...")
        self.analyzer = ExistingAPIAnalyzer(str(self.backend_dir))
        self.existing_data = self.analyzer.get_normalized_endpoints()
        
        existing_summary = self.analyzer.get_endpoint_summary()
        print(f"  Found {existing_summary['total_endpoints']} endpoints")
        print(f"  Apps: {existing_summary['apps']}")
        
        # Step 3: Compare
        print("\n[3/4] Comparing Specifications...")
        self.comparator = APIComparator(
            self.spec_data['endpoints'],
            self.existing_data
        )
        self.comparison_results = self.comparator.compare()
        
        summary = self.comparison_results['summary']
        print(f"  Coverage: {summary['coverage_percentage']}%")
        print(f"  Missing: {summary['total_missing']}")
        print(f"  Extra: {summary['total_extra']}")
        
        # Generate comparison report
        report_file = self.output_dir / 'api_comparison_report.md'
        self.comparator.generate_report(str(report_file))
        
        if report_only:
            print(f"\n✓ Report saved to: {report_file}")
            return {
                'report_file': str(report_file),
                'summary': summary
            }
        
        # Step 4: Generate code
        if generate:
            print("\n[4/4] Generating Code...")
            results = self._generate_code(
                resource_filter=resource_filter,
                dry_run=dry_run,
                limit=limit
            )
            
            return results
        
        # Default: show what would be generated
        print("\n[4/4] Preview Missing APIs...")
        self._preview_missing(
            resource_filter=resource_filter,
            limit=limit or 10
        )
        
        print("\n" + "="*70)
        print("To generate code, run with --generate flag")
        print("="*70)
        
        return {
            'report_file': str(report_file),
            'summary': summary,
            'preview': True
        }
    
    def _generate_code(
        self,
        resource_filter: str = None,
        dry_run: bool = False,
        limit: int = None
    ) -> Dict[str, Any]:
        """Generate Django code for missing APIs."""
        missing_apis = self.comparison_results['missing']
        
        # Filter by resource if specified
        if resource_filter:
            missing_apis = [
                api for api in missing_apis
                if api['resource'].lower() == resource_filter.lower()
            ]
            print(f"  Filtered to resource: {resource_filter}")
            print(f"  APIs to generate: {len(missing_apis)}")
        
        # Apply limit
        if limit:
            missing_apis = missing_apis[:limit]
            print(f"  Limited to: {limit} APIs")
        
        # Skip certain endpoints
        missing_apis = [
            api for api in missing_apis
            if not should_skip_endpoint(api)
        ]
        
        if not missing_apis:
            print("\n  No APIs to generate!")
            return {'generated': []}
        
        # Initialize generator
        self.generator = DjangoCodeGenerator(str(self.backend_dir))
        
        # Generate each API
        generated_apis = []
        errors = []
        
        for i, api in enumerate(missing_apis, 1):
            try:
                print(f"\n  [{i}/{len(missing_apis)}] Generating "
                      f"{api['method']} {api['path']}")
                
                generated_files = self.generator.generate_api(
                    api,
                    dry_run=dry_run
                )
                
                generated_apis.append({
                    'endpoint': f"{api['method']} {api['path']}",
                    'operation_id': api['operation_id'],
                    'files': generated_files
                })
                
            except Exception as e:
                error_info = {
                    'endpoint': f"{api['method']} {api['path']}",
                    'error': str(e)
                }
                errors.append(error_info)
                print(f"    ✗ Error: {e}")
        
        # Generate summary report
        summary_file = self._generate_summary_report(
            generated_apis,
            errors,
            dry_run
        )
        
        print(f"\n✓ Generation complete!")
        print(f"  Generated: {len(generated_apis)} APIs")
        print(f"  Errors: {len(errors)}")
        print(f"  Summary: {summary_file}")
        
        return {
            'generated': generated_apis,
            'errors': errors,
            'summary_file': str(summary_file)
        }
    
    def _preview_missing(
        self,
        resource_filter: str = None,
        limit: int = 10
    ):
        """Preview missing APIs without generating."""
        missing_apis = self.comparison_results['missing']
        
        # Filter
        if resource_filter:
            missing_apis = [
                api for api in missing_apis
                if api['resource'].lower() == resource_filter.lower()
            ]
        
        # Skip certain endpoints
        missing_apis = [
            api for api in missing_apis
            if not should_skip_endpoint(api)
        ]
        
        # Apply limit
        preview_apis = missing_apis[:limit]
        
        print(f"\n  Top {len(preview_apis)} Missing APIs "
              f"(of {len(missing_apis)} total):\n")
        
        for i, api in enumerate(preview_apis, 1):
            priority_label = self._get_priority_label(api['priority'])
            print(f"  {i}. [{priority_label}] "
                  f"{api['method']} {api['path']}")
            print(f"     Operation: {api['operation_id']}")
            print(f"     Resource: {api['resource']}")
            print(f"     Summary: {api['summary'][:60]}...")
            print()
    
    def _get_priority_label(self, priority: int) -> str:
        """Get priority label."""
        if priority >= 70:
            return "HIGH"
        elif priority >= 40:
            return "MED "
        else:
            return "LOW "
    
    def _generate_summary_report(
        self,
        generated_apis: List[Dict],
        errors: List[Dict],
        dry_run: bool
    ) -> str:
        """Generate summary report of code generation."""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f'code_generation_summary_{timestamp}.md'
        summary_file = self.output_dir / filename
        
        lines = [
            "# Code Generation Summary",
            "",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Mode: {'DRY RUN' if dry_run else 'ACTUAL GENERATION'}",
            "",
            "## Statistics",
            "",
            f"- **Total APIs Generated**: {len(generated_apis)}",
            f"- **Errors**: {len(errors)}",
            "",
        ]
        
        if generated_apis:
            lines.extend([
                "## Generated APIs",
                "",
            ])
            
            for api in generated_apis:
                lines.append(f"### {api['endpoint']}")
                lines.append("")
                lines.append(f"**Operation**: {api['operation_id']}")
                lines.append("")
                lines.append("**Files Generated**:")
                lines.append("")
                
                for component, filepath in api['files'].items():
                    lines.append(f"- {component}: `{filepath}`")
                
                lines.append("")
        
        if errors:
            lines.extend([
                "## Errors",
                "",
            ])
            
            for error in errors:
                lines.append(f"- **{error['endpoint']}**: {error['error']}")
            
            lines.append("")
        
        # Manual steps
        lines.extend([
            "## Next Steps",
            "",
            "After code generation, you need to:",
            "",
            "1. **Update URLs**: Add new view imports and URL patterns",
            "2. **Run Migrations**: If new models were created",
            "3. **Implement Logic**: Complete TODOs in generated code",
            "4. **Add Tests**: Create test cases for new endpoints",
            "5. **Review Code**: Ensure it follows project standards",
            "",
        ])
        
        report_content = '\n'.join(lines)
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return str(summary_file)


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Generate missing Django APIs from OpenAPI spec',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate comparison report only
  python generate_missing_apis.py --report-only
  
  # Preview what would be generated
  python generate_missing_apis.py
  
  # Generate code (dry run)
  python generate_missing_apis.py --generate --dry-run
  
  # Generate code for real
  python generate_missing_apis.py --generate
  
  # Generate only for specific resource
  python generate_missing_apis.py --generate --resource tasks
  
  # Generate first 5 missing APIs
  python generate_missing_apis.py --generate --limit 5
        """
    )
    
    parser.add_argument(
        '--spec-url',
        default=(
            'https://raw.githubusercontent.com/Asana/openapi/'
            'master/defs/asana_oas.yaml'
        ),
        help='OpenAPI specification URL'
    )
    
    parser.add_argument(
        '--output-dir',
        help='Output directory for reports (default: backend/)'
    )
    
    parser.add_argument(
        '--report-only',
        action='store_true',
        help='Only generate comparison report'
    )
    
    parser.add_argument(
        '--generate',
        action='store_true',
        help='Generate Django code for missing APIs'
    )
    
    parser.add_argument(
        '--resource',
        help='Filter by resource (e.g., projects, tasks)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without creating files'
    )
    
    parser.add_argument(
        '--limit',
        type=int,
        help='Limit number of APIs to generate'
    )
    
    args = parser.parse_args()
    
    # Determine backend directory
    backend_dir = Path(__file__).parent.parent
    
    # Create generator
    generator = MissingAPIGenerator(
        spec_url=args.spec_url,
        backend_dir=str(backend_dir),
        output_dir=args.output_dir
    )
    
    # Run
    try:
        results = generator.run(
            report_only=args.report_only,
            generate=args.generate,
            resource_filter=args.resource,
            dry_run=args.dry_run,
            limit=args.limit
        )
        
        sys.exit(0)
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user")
        sys.exit(1)
    
    except Exception as e:
        print(f"\n\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()

