from typing import Dict, Any, List
from asana_tasks.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_tasks.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class RemoveFollowersFromTaskInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def remove_followers_from_task(
        self,
        task_gid: str,
        follower_gids: List[str]
    ) -> Dict[str, Any]:
        task = self.storage.remove_followers_from_task(task_gid, follower_gids)

        task_dict = {
            'gid': str(task.gid),
            'name': task.name,
        }

        return self.presenter.get_task_response(task_dict)

