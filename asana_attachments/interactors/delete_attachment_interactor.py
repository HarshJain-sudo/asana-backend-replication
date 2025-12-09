"""
Interactor for .
"""
from typing import Dict, Any, List, Optional
from asana_attachments.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_attachments.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class DeleteAttachmentInteractor:
    """delete attachment for attachments"""
    
    def __init__(
        self,
        storage: StorageInterface,
        presenter: PresenterInterface
    ):
        """
        Initialize interactor with dependencies.
        
        Args:
            storage: Storage interface implementation
            presenter: Presenter interface implementation
        """
        self.storage = storage
        self.presenter = presenter

    def delete_attachment(
        self,
    ) -> Dict[str, Any]:
        """
        
        
        Args:
        
        Returns:
            Dict containing response data
        """
        # Format response
        response_data = {
        }
        
        return self.presenter.get_response(response_data)
