"""
Interactor for .
"""
from typing import Dict, Any, List, Optional
from asana_goal_relationships.interactors.storage_interfaces.storage_interface import (
    StorageInterface
)
from asana_goal_relationships.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class RemoveSupportingRelationshipInteractor:
    """remove supporting relationship for goal relationships"""
    
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

    def remove_supporting_relationship(
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
