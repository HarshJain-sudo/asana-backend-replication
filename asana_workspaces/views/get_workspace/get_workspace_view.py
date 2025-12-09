"""
View for getting, updating, and deleting a workspace.
"""
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_workspaces.interactors.get_workspace_interactor import (
    GetWorkspaceInteractor
)
from asana_workspaces.interactors.update_workspace_interactor import (
    UpdateWorkspaceInteractor
)
from asana_workspaces.interactors.delete_workspace_interactor import (
    DeleteWorkspaceInteractor
)
from asana_workspaces.storages.storage_implementation import (
    StorageImplementation
)
from asana_workspaces.presenters.get_workspace_presenter_implementation import (
    GetWorkspacePresenterImplementation
)
from asana_workspaces.exceptions.custom_exceptions import (
    WorkspaceDoesNotExistException,
    InvalidWorkspaceGidException
)
from asana_workspaces.serializers import (
    WorkspaceUpdateSerializer,
    WorkspaceSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetWorkspaceView(APIView):
    @ratelimit(key='ip', rate='5/m', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the workspace or organization.',
                required=True,
                examples=[OpenApiExample('Example GID', value='12345')]
            ),
            OpenApiParameter(
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.',
                required=False,
                examples=[
                    OpenApiExample(
                        'Include all optional fields',
                        value='email_domains,is_organization,name'
                    )
                ]
            ),
            OpenApiParameter(
                name='opt_pretty',
                type=bool,
                location=OpenApiParameter.QUERY,
                description='Provides "pretty" output. Provides the response in a "pretty" format. In the case of JSON this means doing proper line breaking and indentation to make it readable.',
                required=False,
                examples=[OpenApiExample('Pretty output', value=True)]
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=WorkspaceSingleResponseSerializer,
                description="Return the full workspace record.",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={
                            "data": {
                                "gid": "12345",
                                "resource_type": "workspace",
                                "name": "My Company Workspace",
                                "email_domains": ["asana.com"],
                                "is_organization": False
                            }
                        }
                    )
                ]
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.",
                examples=[
                    OpenApiExample(
                        'Bad Request',
                        value={
                            "errors": [
                                {
                                    "message": "workspace: Missing input",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors",
                                    "phrase": "6 sad squid snuggle softly"
                                }
                            ]
                        }
                    )
                ]
            ),
            401: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="A valid authentication token was not provided with the request, so the API could not associate a user with the request."
            ),
            403: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={
                            "errors": [
                                {
                                    "message": "Workspace does not exist",
                                    "help": "For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors",
                                    "phrase": "6 sad squid snuggle softly"
                                }
                            ]
                        }
                    )
                ]
            ),
            500: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="There was a problem on Asana's end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error."
            ),
        },
        summary="Get a workspace",
        description="Returns the full workspace record for a single workspace."
    )
    def get(self, request, workspace_gid: str):
        import json
        
        # Validate UUID format
        try:
            validate_uuid(workspace_gid)
        except Exception:
            error_response = {
                'errors': [{
                    'message': 'workspace: Invalid GID format',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        # Get query parameters
        opt_fields = request.query_params.get('opt_fields')
        opt_pretty = request.query_params.get('opt_pretty', 'false').lower() == 'true'

        storage = StorageImplementation()
        presenter = GetWorkspacePresenterImplementation()
        interactor = GetWorkspaceInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_workspace(
                workspace_gid=workspace_gid,
                opt_fields=opt_fields
            )
            
            # Handle opt_pretty for pretty JSON formatting
            if opt_pretty:
                response_data = json.dumps(response, indent=2, ensure_ascii=False)
                return Response(
                    json.loads(response_data),
                    status=status.HTTP_200_OK
                )
            
            return Response(response, status=status.HTTP_200_OK)
        except WorkspaceDoesNotExistException as e:
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

    @ratelimit(key='ip', rate='5/s', method='PUT')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the workspace.'
            )
        ],
        request=WorkspaceUpdateSerializer,
        responses={
            200: OpenApiResponse(
                response=WorkspaceSingleResponseSerializer,
                description="Workspace updated successfully."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request - Invalid input data."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Not Found - Workspace does not exist."
            ),
        },
        summary="Update a workspace",
        description="Updates an existing workspace."
    )
    def put(self, request, workspace_gid: str):
        try:
            validate_uuid(workspace_gid)
        except ValueError as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = WorkspaceUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        storage = StorageImplementation()
        presenter = GetWorkspacePresenterImplementation()
        interactor = UpdateWorkspaceInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.update_workspace_wrapper(
                workspace_gid=workspace_gid,
                name=serializer.validated_data.get('name'),
                is_organization=serializer.validated_data.get(
                    'is_organization'
                )
            )
            return Response(response, status=status.HTTP_200_OK)
        except WorkspaceDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

    @ratelimit(key='ip', rate='5/s', method='DELETE')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the workspace.'
            )
        ],
        responses={
            204: OpenApiResponse(
                response=None,
                description="Workspace deleted successfully."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request - Invalid workspace GID format."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Not Found - Workspace does not exist."
            ),
        },
        summary="Delete a workspace",
        description="Deletes an existing workspace."
    )
    def delete(self, request, workspace_gid: str):
        try:
            validate_uuid(workspace_gid)
        except ValueError as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        interactor = DeleteWorkspaceInteractor(storage=storage)

        try:
            interactor.delete_workspace_wrapper(workspace_gid)
            return Response(status=status.HTTP_204_NO_CONTENT)
        except WorkspaceDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

