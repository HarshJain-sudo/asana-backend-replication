from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_teams.interactors.get_teams_interactor import (
    GetTeamsInteractor
)
from asana_teams.storages.storage_implementation import (
    StorageImplementation
)
from asana_teams.presenters.get_teams_presenter_implementation import (
    GetTeamsPresenterImplementation
)
from asana_teams.serializers import (
    TeamListResponseSerializer,
    ErrorResponseSerializer
)
from asana_teams.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_users.exceptions.custom_exceptions import (
    UserDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid, validate_pagination_params
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetTeamsForUserView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='user_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the user.',
                required=True
            ),
            OpenApiParameter(
                name='offset',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Offset token. An offset to the next page returned by the API.',
                required=False
            ),
            OpenApiParameter(
                name='limit',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Results per page. The number of objects to return per page. The value must be between 1 and 100.',
                required=False
            ),
            OpenApiParameter(
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default.',
                required=False
            ),
            OpenApiParameter(
                name='opt_pretty',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Provides "pretty" output.',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=TeamListResponseSerializer,
                description="Returns the compact records for all teams the user has access to.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": [
                                {
                                    "gid": "12345",
                                    "resource_type": "team",
                                    "name": "Engineering Team"
                                }
                            ]
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="This usually occurs because of a missing or malformed parameter."
            ),
            401: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="A valid authentication token was not provided."
            ),
            403: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="The authentication and request syntax was valid but the server is refusing to complete the request."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist."
            ),
            500: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="There was a problem on Asana's end."
            ),
        },
        summary="Get teams for a user",
        description="Returns the compact records for all teams the user has access to.",
        tags=["Teams"]
    )
    def get(self, request, user_gid: str):
        import json
        
        opt_pretty = request.query_params.get('opt_pretty', 'false').lower() == 'true'
        
        try:
            validate_uuid(user_gid)
        except Exception:
            error_response = {
                'errors': [{
                    'message': 'user: Invalid GID format',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate pagination
        try:
            offset_param = request.query_params.get('offset', '0')
            try:
                offset = int(offset_param)
            except ValueError:
                offset = 0
            
            limit_param = request.query_params.get('limit')
            limit = int(limit_param) if limit_param else DEFAULT_LIMIT
            
            offset, limit = validate_pagination_params(
                offset=offset,
                limit=limit,
                max_limit=MAX_LIMIT
            )
        except Exception as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        storage = StorageImplementation()
        presenter = GetTeamsPresenterImplementation()
        interactor = GetTeamsInteractor(
            storage=storage,
            presenter=presenter
        )
        
        try:
            # Get teams for user
            teams = storage.get_teams_for_user(
                user_gid=user_gid,
                offset=offset,
                limit=limit
            )
            
            # Format teams matching TeamCompact schema
            teams_list = [
                {
                    'gid': str(team.gid),
                    'resource_type': 'team',
                    'name': team.name,
                }
                for team in teams
            ]
            
            response = presenter.get_teams_response(teams_list)
            
            if opt_pretty:
                response_data = json.dumps(response, indent=2, ensure_ascii=False)
                return Response(
                    json.loads(response_data),
                    status=status.HTTP_200_OK
                )
            
            return Response(response, status=status.HTTP_200_OK)
        except UserDoesNotExistException as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

