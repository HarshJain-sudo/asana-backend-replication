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


class GetTimePeriodsView(APIView):
    """
    Get time periods
    Matches Asana API: GET /time_periods
    """
    
    @ratelimit(key='ip', rate='10/s', method='GET')
    @extend_schema(
        parameters=[
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
                name='start_on',
                type=str,
                location=OpenApiParameter.QUERY,
                description='ISO 8601 date string',
                required=False
            ),
            OpenApiParameter(
                name='end_on',
                type=str,
                location=OpenApiParameter.QUERY,
                description='ISO 8601 date string',
                required=False
            ),
            OpenApiParameter(
                name='workspace',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Globally unique identifier for the workspace.',
                required=True
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
                response=GetTimePeriodsResponseSerializer,
                description="Successfully retrieved the requested time periods.",
            ),
            400: OpenApiResponse(
                description="This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.",
            ),
            401: OpenApiResponse(
                description="A valid authentication token was not provided with the request, so the API could not associate a user with the request.",
            ),
            403: OpenApiResponse(
                description="The authentication and request syntax was valid but the server is refusing to complete the request. This can happen if you try to read or write to objects or properties that the user does not have access to.",
            ),
            404: OpenApiResponse(
                description="Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist.",
            ),
            500: OpenApiResponse(
                description="There was a problem on Asana’s end. In the event of a server error the response body should contain an error phrase. These phrases can be used by Asana support to quickly look up the incident that caused the server error. Some errors are due to server load, and will not supply an error phrase.",
            ),
        },
        summary="Get time periods",
        description="",
        tags=["Time periods"]
    )
    def get(self, request):
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
