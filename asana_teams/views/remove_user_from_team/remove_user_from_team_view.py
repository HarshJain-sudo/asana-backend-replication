from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_teams.interactors.remove_user_from_team_interactor import (
    RemoveUserFromTeamInteractor
)
from asana_teams.storages.storage_implementation import (
    StorageImplementation
)
from asana_teams.serializers import (
    TeamRemoveUserRequestSerializer,
    ErrorResponseSerializer
)
from asana_teams.exceptions.custom_exceptions import (
    TeamDoesNotExistException,
    UserDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class RemoveUserFromTeamView(APIView):
    @ratelimit(key='ip', rate='5/m', method='POST')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='team_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the team.',
                required=True
            ),
        ],
        request=TeamRemoveUserRequestSerializer,
        responses={
            200: OpenApiResponse(
                description="Returns an empty data record.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={"data": {}}
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
        summary="Remove a user from a team",
        description="The user making this call must be a member of the team in order to remove themselves or others.",
        tags=["Teams"]
    )
    def post(self, request, team_gid: str):
        from drf_spectacular.utils import OpenApiExample
        
        try:
            validate_uuid(team_gid)
        except Exception:
            error_response = {
                'errors': [{
                    'message': 'team: Invalid GID format',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TeamRemoveUserRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = {
                'errors': [{
                    'message': f"user: {str(serializer.errors)}",
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        storage = StorageImplementation()
        interactor = RemoveUserFromTeamInteractor(storage=storage)
        
        try:
            interactor.remove_user_from_team(
                team_gid=team_gid,
                user=serializer.validated_data['user']
            )
            return Response({'data': {}}, status=status.HTTP_200_OK)
        except (TeamDoesNotExistException, UserDoesNotExistException) as e:
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

