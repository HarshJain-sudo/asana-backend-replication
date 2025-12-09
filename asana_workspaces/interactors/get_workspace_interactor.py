"""
Interactor for getting a workspace.
"""
from typing import Dict, Any, Optional, List
from asana_workspaces.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_workspaces.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)


class GetWorkspaceInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_workspace(
        self,
        workspace_gid: str,
        opt_fields: Optional[str] = None
    ) -> Dict[str, Any]:
        workspace = self.storage.get_workspace(workspace_gid)

        if not workspace:
            raise WorkspaceDoesNotExistException()

        # Parse opt_fields if provided
        requested_fields = set()
        if opt_fields:
            requested_fields = set(
                field.strip() for field in opt_fields.split(',')
            )

        # Default fields (always included - from WorkspaceCompact)
        workspace_dict = {
            'gid': str(workspace.gid),
            'resource_type': 'workspace',
            'name': workspace.name,  # Always included (part of compact schema)
        }

        # Optional fields from WorkspaceResponse
        # is_organization is in the response schema, include by default
        workspace_dict['is_organization'] = workspace.is_organization
        
        # email_domains is optional - only include if requested via opt_fields
        if opt_fields and 'email_domains' in requested_fields:
            # email_domains is not in our model, so we return empty array
            # In a full implementation, this would come from a related model
            workspace_dict['email_domains'] = []
        elif not opt_fields:
            # If opt_fields is not specified, include all default fields
            # email_domains is optional, but we'll include it as empty array
            # to match the spec example
            workspace_dict['email_domains'] = []

        return self.presenter.get_workspace_response(workspace_dict)

