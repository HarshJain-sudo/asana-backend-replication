from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_projects.interactors.get_project_interactor import (
    GetProjectInteractor
)
from asana_projects.storages.storage_implementation import (
    StorageImplementation
)
from asana_projects.presenters.get_project_presenter_implementation import (
    GetProjectPresenterImplementation
)
from asana_projects.exceptions.custom_exceptions import (
    ProjectDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetProjectView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, project_gid: str):
        # Validate UUID format
        try:
            validate_uuid(project_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid project GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetProjectPresenterImplementation()
        interactor = GetProjectInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_project(project_gid)
            return Response(response, status=status.HTTP_200_OK)
        except ProjectDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

