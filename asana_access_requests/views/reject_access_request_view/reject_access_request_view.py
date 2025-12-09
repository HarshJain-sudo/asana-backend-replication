from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_access_requests.interactors.reject_access_request_interactor import (
    RejectAccessRequestInteractor
)
from asana_access_requests.storages.storage_implementation import (
    StorageImplementation
)
from asana_access_requests.presenters.reject_access_request_presenter_implementation import (
    RejectAccessRequestPresenterImplementation
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error,
    invalid_gid_error,
    missing_field_error,
    server_error,
)


class RejectAccessRequestView(APIView):
    """
    Reject an access request
    Matches Asana API: POST /access_requests/{access_request_gid}/reject
    """
    
    @ratelimit(key='ip', rate='5/s', method='POST')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='access_request_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the access request.',
                required=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=RejectAccessRequestResponseSerializer,
                description="Successfully rejected an access request.",
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
        summary="Reject an access request",
        description="",
        tags=["Access requests"]
    )
    def post(self, request, access_request_gid: str):
        # Validate access_request_gid format
        try:
            validate_uuid(access_request_gid)
        except Exception:
            return Response(
                invalid_gid_error("access_request_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize dependencies
        storage = StorageImplementation()
        presenter = RejectAccessRequestPresenterImplementation()
        interactor = RejectAccessRequestInteractor(
            storage=storage,
            presenter=presenter
        )
        
        try:
            # Execute business logic
            response = interactor.reject_access_request(
                access_request_gid=access_request_gid,
            )
            
            return Response(response, status=status.HTTP_201_CREATED)
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
