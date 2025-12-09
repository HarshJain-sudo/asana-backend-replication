from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter
)
from asana_teams.interactors.create_team_interactor import (
    CreateTeamInteractor
)
from asana_teams.storages.storage_implementation import (
    StorageImplementation
)
from asana_teams.presenters.get_team_presenter_implementation import (
    GetTeamPresenterImplementation
)
from asana_teams.serializers import (
    TeamCreateRequestSerializer,
    TeamSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_teams.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException
)
from asana_teams.serializers import (
    TeamCreateRequestSerializer,
    TeamSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_backend.utils.decorators.ratelimit import ratelimit


class CreateTeamView(APIView):
    @ratelimit(key='ip', rate='5/m', method='POST')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.',
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
        request=TeamCreateRequestSerializer,
        responses={
            201: OpenApiResponse(
                response=TeamSingleResponseSerializer,
                description="Successfully created a new team.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "team",
                                "name": "Engineering Team",
                                "description": "Backend development team",
                                "workspace": {
                                    "gid": "98765",
                                    "resource_type": "workspace",
                                    "name": "My Workspace"
                                }
                            }
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
        summary="Create a team",
        description="Creates a new team in a workspace or organization.",
        tags=["Teams"]
    )
    def post(self, request):
        import json
        
        opt_pretty = request.query_params.get('opt_pretty', 'false').lower() == 'true'
        
        serializer = TeamCreateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = {
                'errors': [{
                    'message': f"team: {str(serializer.errors)}",
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        storage = StorageImplementation()
        presenter = GetTeamPresenterImplementation()
        interactor = CreateTeamInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.create_team(**serializer.validated_data)
            
            if opt_pretty:
                response_data = json.dumps(response, indent=2, ensure_ascii=False)
                return Response(
                    json.loads(response_data),
                    status=status.HTTP_201_CREATED
                )
            
            return Response(response, status=status.HTTP_201_CREATED)
        except WorkspaceDoesNotExistException as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        except ValueError as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

