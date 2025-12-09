from typing import Dict, Any
from asana_projects.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_projects.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class CreateProjectInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def create_project(
        self,
        name: str,
        workspace_gid: str,
        **kwargs
    ) -> Dict[str, Any]:
        project_details = self.storage.create_project(
            name=name,
            workspace_gid=workspace_gid,
            **kwargs
        )
        return self.presenter.get_project_response(project_details)

