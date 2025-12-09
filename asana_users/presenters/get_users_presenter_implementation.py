"""
Presenter implementation for multiple users response.
"""
from typing import Dict, Any, List
from asana_users.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetUsersPresenterImplementation(PresenterInterface):
    def get_user_response(
        self,
        user_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': user_dict
        }

    def get_users_response(
        self,
        users_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': users_list
        }

    def get_user_workspaces_response(
        self,
        workspaces_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': workspaces_list
        }

