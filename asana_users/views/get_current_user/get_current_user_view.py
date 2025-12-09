"""
API view for retrieving current authenticated user.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_users.interactors.get_current_user_interactor import (
    GetCurrentUserInteractor
)
from asana_users.storages.storage_implementation import (
    StorageImplementation
)
from asana_users.presenters.get_user_presenter_implementation import (
    GetUserPresenterImplementation
)
from asana_users.exceptions.custom_exceptions import (
    UserNotAuthenticatedException
)
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetCurrentUserView(APIView):
    @ratelimit(key='ip', rate='5/m', method='GET')
    def get(self, request):
        # For now, we'll use a simple token-based approach
        # In production, this should use proper authentication
        user_gid = request.headers.get('X-User-Gid') or \
                   request.query_params.get('user_gid')

        storage = StorageImplementation()
        presenter = GetUserPresenterImplementation()
        interactor = GetCurrentUserInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_current_user(user_gid)
            return Response(response, status=status.HTTP_200_OK)
        except UserNotAuthenticatedException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_401_UNAUTHORIZED
            )

