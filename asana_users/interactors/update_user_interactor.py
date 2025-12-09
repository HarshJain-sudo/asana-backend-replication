"""
Interactor for .
"""
from typing import Dict, Any, List, Optional
from asana_users.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_users.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class UpdateUserInteractor:
    """update user for users"""
    
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

    def update_user(
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
