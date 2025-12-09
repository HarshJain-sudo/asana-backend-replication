"""
Interactor for getting all workspaces.
"""
from typing import Dict, Any, List, Optional
import base64
from asana_workspaces.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_workspaces.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_workspaces.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)


class GetWorkspacesInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_workspaces(
        self,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT,
        opt_fields: Optional[str] = None,
        request=None
    ) -> Dict[str, Any]:
        workspaces = self.storage.get_workspaces(
            offset=offset,
            limit=limit
        )

        # Parse opt_fields if provided
        requested_fields = set()
        if opt_fields:
            requested_fields = set(
                field.strip() for field in opt_fields.split(',')
            )

        # Format workspaces matching WorkspaceCompact schema
        # Default compact schema includes: gid, resource_type, name
        # Optional fields via opt_fields: email_domains, is_organization, offset, path, uri
        workspaces_list = []
        for workspace in workspaces:
            workspace_dict = {
                'gid': str(workspace.gid),
                'resource_type': 'workspace',
                'name': workspace.name,  # Always included in compact schema
            }
            
            # Optional fields - only include if explicitly requested via opt_fields
            if opt_fields:
                if 'is_organization' in requested_fields:
                    workspace_dict['is_organization'] = workspace.is_organization
                
                if 'email_domains' in requested_fields:
                    workspace_dict['email_domains'] = []  # Not in model, return empty
            # If opt_fields not specified, return compact schema only (gid, resource_type, name)
            
            workspaces_list.append(workspace_dict)

        # Generate next_page if there are more results
        next_page = None
        total_count = self.storage.get_workspaces_count()
        has_more = (offset + limit) < total_count
        
        if has_more and request:
            # Generate offset token (base64 encoded next offset)
            next_offset = offset + limit
            offset_token = base64.b64encode(
                str(next_offset).encode('utf-8')
            ).decode('utf-8')
            
            # Build next_page object
            base_path = '/api/asana_workspaces/workspaces/'
            query_params = f'limit={limit}&offset={offset_token}'
            if opt_fields:
                query_params += f'&opt_fields={opt_fields}'
            
            next_page = {
                'offset': offset_token,
                'path': f'{base_path}?{query_params}',
                'uri': f'{request.scheme}://{request.get_host()}{base_path}?{query_params}'
            }
            
            # Include next_page fields in opt_fields if requested
            if opt_fields:
                if 'offset' in requested_fields or 'path' in requested_fields or 'uri' in requested_fields:
                    # Already included above
                    pass

        response = self.presenter.get_workspaces_response(workspaces_list)
        
        # Add next_page to response if exists
        if next_page:
            response['next_page'] = next_page
        
        return response

