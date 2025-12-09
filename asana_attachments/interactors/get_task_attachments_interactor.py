from typing import Dict, Any
from asana_attachments.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_attachments.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_attachments.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
)


class GetTaskAttachmentsInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_task_attachments(
        self,
        task_gid: str,
        offset: int = DEFAULT_OFFSET,
        limit: int = DEFAULT_LIMIT
    ) -> Dict[str, Any]:
        attachments = self.storage.get_task_attachments(
            task_gid=task_gid,
            offset=offset,
            limit=limit
        )

        attachments_list = [
            {
                'gid': str(attachment.gid),
                'name': attachment.name,
                'task': {
                    'gid': str(attachment.task.gid),
                    'name': attachment.task.name
                },
                'resource_type': attachment.resource_type,
                'download_url': attachment.download_url,
                'view_url': attachment.view_url,
                'host': attachment.host,
                'file_size': attachment.file_size,
                'mime_type': attachment.mime_type,
                'created_at': attachment.created_at.isoformat(),
                'created_by': {
                    'gid': str(attachment.created_by.gid),
                    'name': attachment.created_by.name
                } if attachment.created_by else None,
            }
            for attachment in attachments
        ]

        return self.presenter.get_attachments_response(attachments_list)

