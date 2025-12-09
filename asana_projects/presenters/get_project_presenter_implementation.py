from typing import Dict, Any, List
from asana_projects.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetProjectPresenterImplementation(PresenterInterface):
    def get_project_response(
        self,
        project_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': project_dict
        }

    def get_projects_response(
        self,
        projects_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': projects_list
        }

