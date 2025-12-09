from typing import Dict, Any
from asana_projects.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_projects.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class UpdateProjectInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def update_project(
        self,
        project_gid: str,
        **update_data
    ) -> Dict[str, Any]:
        project_details = self.storage.update_project(
            project_gid,
            **update_data
        )
        return self.presenter.get_project_response(project_details)

