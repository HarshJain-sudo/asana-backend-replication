from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter
)
from asana_users.interactors.get_user_interactor import GetUserInteractor
from asana_users.interactors.update_user_interactor import UpdateUserInteractor
from asana_users.interactors.delete_user_interactor import DeleteUserInteractor
from asana_users.storages.storage_implementation import StorageImplementation
from asana_users.presenters.get_user_presenter_implementation import (
    GetUserPresenterImplementation
)
from asana_users.exceptions.custom_exceptions import UserDoesNotExistException
from asana_users.serializers import (
    UserUpdateSerializer,
    UserSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetUserView(APIView):
    @ratelimit(key='ip', rate='5/m', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the user.'
            )
        ],
        responses={
            200: OpenApiResponse(
                response=UserSingleResponseSerializer,
                description="User details."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Not Found."
            ),
        },
        summary="Get a single user",
        description="Returns the complete user record for a given GID."
    )
    def get(self, request, user_gid: str):
        try:
            validate_uuid(user_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid user GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetUserPresenterImplementation()
        interactor = GetUserInteractor(storage=storage, presenter=presenter)

        try:
            response = interactor.get_user(user_gid)
            return Response(response, status=status.HTTP_200_OK)
        except UserDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

    @ratelimit(key='ip', rate='5/m', method='PUT')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the user.'
            )
        ],
        request=UserUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=UserSingleResponseSerializer,
                description="User updated successfully."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Not Found."
            ),
        },
        summary="Update a user",
        description="Updates an existing user."
    )
    def put(self, request, user_gid: str):
        try:
            validate_uuid(user_gid)
        except ValueError as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = UserUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        storage = StorageImplementation()
        presenter = GetUserPresenterImplementation()
        interactor = UpdateUserInteractor(storage=storage, presenter=presenter)

        try:
            response = interactor.update_user_wrapper(
                user_gid=user_gid,
                name=serializer.validated_data.get('name'),
                email=serializer.validated_data.get('email'),
                photo=serializer.validated_data.get('photo')
            )
            return Response(response, status=status.HTTP_200_OK)
        except UserDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

    @ratelimit(key='ip', rate='5/m', method='DELETE')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the user.'
            )
        ],
        responses={
            204: OpenApiResponse(
                response=None,
                description="User deleted successfully."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Not Found."
            ),
        },
        summary="Delete a user",
        description="Deletes an existing user."
    )
    def delete(self, request, user_gid: str):
        try:
            validate_uuid(user_gid)
        except ValueError as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        interactor = DeleteUserInteractor(storage=storage)

        try:
            interactor.delete_user_wrapper(user_gid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except UserDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )
