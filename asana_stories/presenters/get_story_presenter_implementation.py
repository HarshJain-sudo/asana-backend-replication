from typing import Dict, Any, List
from asana_stories.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetStoryPresenterImplementation(PresenterInterface):
    def get_story_response(
        self,
        story_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': story_dict
        }

    def get_stories_response(
        self,
        stories_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': stories_list
        }

