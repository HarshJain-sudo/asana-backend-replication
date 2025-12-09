from typing import Dict, Any, List
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetTasksPresenterImplementation(PresenterInterface):
    def get_task_response(
        self,
        task_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': task_dict
        }

    def get_tasks_response(
        self,
        tasks_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': tasks_list
        }

    def get_delete_response(self) -> Dict[str, Any]:
        return {
            'data': {}
        }

