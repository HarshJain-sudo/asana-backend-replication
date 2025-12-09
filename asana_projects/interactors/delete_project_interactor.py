from typing import Dict, Any
from asana_projects.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_projects.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class DeleteProjectInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def delete_project(self, project_gid: str) -> Dict[str, Any]:
        self.storage.delete_project(project_gid)
        return {'data': {}}

