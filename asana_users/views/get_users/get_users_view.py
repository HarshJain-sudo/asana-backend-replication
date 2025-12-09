from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter
)
from asana_users.interactors.get_users_interactor import GetUsersInteractor
from asana_users.interactors.create_user_interactor import CreateUserInteractor
from asana_users.storages.storage_implementation import StorageImplementation
from asana_users.presenters.get_users_presenter_implementation import (
    GetUsersPresenterImplementation
)
from asana_users.presenters.get_user_presenter_implementation import (
    GetUserPresenterImplementation
)
from asana_users.constants.constants import DEFAULT_OFFSET, DEFAULT_LIMIT, MAX_LIMIT
from asana_users.serializers import (
    UserCreateSerializer,
    UserListResponseSerializer,
    UserSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_backend.utils.validators import validate_pagination_params
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetUsersView(APIView):
    @ratelimit(key='ip', rate='5/m', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace',
                type=str,
                location=OpenApiParameter.QUERY,
                description='The workspace or organization ID to filter users on.',
                required=False
            ),
            OpenApiParameter(
                name='team',
                type=str,
                location=OpenApiParameter.QUERY,
                description='The team ID to filter users on.',
                required=False
            ),
            OpenApiParameter(
                name='limit',
                type=int,
                location=OpenApiParameter.QUERY,
                description=f'Results per page. The number of objects to return per page. The value must be between 1 and {MAX_LIMIT}.',
                required=False
            ),
            OpenApiParameter(
                name='offset',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Offset token. An offset to the next page returned by the API.',
                required=False
            ),
            OpenApiParameter(
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.',
                required=False
            )
        ],
        responses={
            200: OpenApiResponse(
                response=UserListResponseSerializer,
                description="List of users."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request."
            ),
        },
        summary="Get multiple users",
        description="Returns a list of users with pagination."
    )
    def get(self, request):
        try:
            # Handle offset - can be int or string token
            offset_param = request.query_params.get('offset', '0')
            try:
                offset = int(offset_param)
            except ValueError:
                # If it's a token, treat as 0 for now
                offset = 0
            
            limit_param = request.query_params.get('limit')
            limit = int(limit_param) if limit_param else DEFAULT_LIMIT
            
            offset, limit = validate_pagination_params(
                offset=offset,
                limit=limit,
                max_limit=MAX_LIMIT
            )
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract parameters matching API spec names
        workspace = request.query_params.get('workspace')
        team = request.query_params.get('team')
        opt_fields = request.query_params.get('opt_fields')

        storage = StorageImplementation()
        presenter = GetUsersPresenterImplementation()
        interactor = GetUsersInteractor(storage=storage, presenter=presenter)

        response = interactor.get_users(
            workspace=workspace,
            team=team,
            opt_fields=opt_fields,
            offset=offset,
            limit=limit
        )
        return Response(response, status=status.HTTP_200_OK)

    @ratelimit(key='ip', rate='5/m', method='POST')
    @extend_schema(
        request=UserCreateSerializer,
        responses={
            201: OpenApiResponse(
                response=UserSingleResponseSerializer,
                description="User created successfully."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request."
            ),
            409: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Conflict - Email already exists."
            ),
        },
        summary="Create a new user",
        description="Creates a new user."
    )
    def post(self, request):
        from django.db import IntegrityError
        
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        storage = StorageImplementation()
        presenter = GetUserPresenterImplementation()
        interactor = CreateUserInteractor(storage=storage, presenter=presenter)

        try:
            response = interactor.create_user_wrapper(
                name=serializer.validated_data['name'],
                email=serializer.validated_data['email'],
                photo=serializer.validated_data.get('photo')
            )
            return Response(response, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            # Duplicate email or other unique constraint violation
            return Response(
                {'errors': [{
                    'message': 'Email already exists',
                    'help': 'For more information, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]},
                status=status.HTTP_409_CONFLICT
            )
