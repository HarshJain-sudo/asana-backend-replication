from typing import Dict, Any
from asana_projects.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_projects.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetProjectTasksInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_project_tasks(
        self,
        project_gid: str,
        offset: int,
        limit: int
    ) -> Dict[str, Any]:
        tasks = self.storage.get_project_tasks(project_gid, offset, limit)
        return self.presenter.get_projects_response(tasks)

