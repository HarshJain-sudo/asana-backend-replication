from typing import List, Optional
from asana_attachments.models.attachment import Attachment
from asana_attachments.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)


class StorageImplementation(StorageInterface):
    def get_attachment(self, attachment_gid: str) -> Optional[Attachment]:
        try:
            return Attachment.objects.get(gid=attachment_gid)
        except Attachment.DoesNotExist:
            return None

    def get_task_attachments(
        self,
        task_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Attachment]:
        return list(
            Attachment.objects.filter(
                task__gid=task_gid
            ).order_by('-created_at')[offset:offset + limit]
        )

