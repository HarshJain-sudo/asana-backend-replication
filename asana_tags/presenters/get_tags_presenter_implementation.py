from typing import Dict, Any, List
from asana_tags.interactors.presenter_interfaces.presenter_interface import (
    PresenterInterface
)


class GetTagsPresenterImplementation(PresenterInterface):
    def get_tag_response(
        self,
        tag_dict: Dict[str, Any]
    ) -> Dict[str, Any]:
        return {
            'data': tag_dict
        }

    def get_tags_response(
        self,
        tags_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        return {
            'data': tags_list
        }

