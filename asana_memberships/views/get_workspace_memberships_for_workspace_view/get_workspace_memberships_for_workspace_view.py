from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error,
    invalid_gid_error,
    missing_field_error,
    server_error,
)


class GetWorkspaceMembershipsForWorkspaceView(APIView):
    """
    Get the workspace memberships for a workspace
    Matches Asana API: GET /workspaces/{workspace_gid}/workspace_memberships
    """
    
    @ratelimit(key='ip', rate='10/s', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='workspace_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the workspace or organization.',
                required=True
            ),
            OpenApiParameter(
                name='user',
                type=str,
                location=OpenApiParameter.QUERY,
                description='A string identifying a user. This can either be the string "me", an email, or the gid of a user.',
                required=False
            ),
            OpenApiParameter(
                name='opt_pretty',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Provides “pretty” output.
Provides the response in a “pretty” format. In the case of JSON this means doing proper line breaking and indentation to make it readable. This will take extra time and increase the response size so it is advisable only to use this during debugging.',
                required=False
            ),
            OpenApiParameter(
                name='limit',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Results per page.
The number of objects to return per page. The value must be between 1 and 100.',
                required=False
            ),
            OpenApiParameter(
                name='offset',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Offset token.
An offset to the next page returned by the API. A pagination request will return an offset token, which can be used as an input parameter to the next request. If an offset is not passed in, the API will return the first page of results.
*Note: You can only pass in an offset that was returned to you via a previously paginated request.*',
                required=False
            ),
            OpenApiParameter(
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=GetWorkspaceMembershipsForWorkspaceResponseSerializer,
                description="Successfully retrieved the requested workspace's memberships.",
            ),
        },
        summary="Get the workspace memberships for a workspace",
        description="",
        tags=["Workspace memberships"]
    )
    def get(self, request, workspace_gid: str):
        # Validate workspace_gid format
        try:
            validate_uuid(workspace_gid)
        except Exception:
            return Response(
                invalid_gid_error("workspace_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # TODO: Implement get logic
            return Response(
                {'data': {'message': 'Not implemented yet'}},
                status=status.HTTP_501_NOT_IMPLEMENTED
            )
        except Exception as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': (
                        'For more information on API status codes and '
                        'how to handle them, read the docs on errors: '
                        'https://asana.github.io/developer-docs/#errors'
                    ),
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(
                error_response,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
