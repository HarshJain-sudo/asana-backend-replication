"""
Presenter implementation for get workspaces response.
"""
from typing import Dict, Any, List
from asana_workspaces.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetWorkspacesPresenterImplementation(PresenterInterface):
    def get_workspace_response(
        self,
        workspace_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': workspace_dict
        }

    def get_workspaces_response(
        self,
        workspaces_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': workspaces_list
        }
    
    def get_user_response(
        self,
        user_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Return user response format (for workspace-user operations)"""
        return {
            'data': user_dict
        }

