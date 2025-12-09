from abc import ABC, abstractmethod
from typing import List, Optional
from asana_attachments.models.attachment import Attachment


class StorageInterface(ABC):
    @abstractmethod
    def get_attachment(self, attachment_gid: str) -> Optional[Attachment]:
        pass

    @abstractmethod
    def get_task_attachments(
        self,
        task_gid: str,
        offset: int = 0,
        limit: int = 50
    ) -> List[Attachment]:
        pass

