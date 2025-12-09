from typing import Dict, Any
from asana_attachments.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_attachments.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)
from asana_attachments.exceptions.custom_exceptions import (
    AttachmentDoesNotExistException
)


class GetAttachmentInteractor:
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        self.storage = storage
        self.presenter = presenter

    def get_attachment(self, attachment_gid: str) -> Dict[str, Any]:
        attachment = self.storage.get_attachment(attachment_gid)

        if not attachment:
            raise AttachmentDoesNotExistException()

        attachment_dict = {
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

        return self.presenter.get_attachment_response(attachment_dict)

