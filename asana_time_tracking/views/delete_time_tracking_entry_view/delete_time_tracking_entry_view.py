from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_time_tracking.interactors.delete_time_tracking_entry_interactor import (
    DeleteTimeTrackingEntryInteractor
)
from asana_time_tracking.storages.storage_implementation import (
    StorageImplementation
)
from asana_time_tracking.presenters.delete_time_tracking_entry_presenter_implementation import (
    DeleteTimeTrackingEntryPresenterImplementation
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error,
    invalid_gid_error,
    missing_field_error,
    server_error,
)


class DeleteTimeTrackingEntryView(APIView):
    """
    Delete a time tracking entry
    Matches Asana API: DELETE /time_tracking_entries/{time_tracking_entry_gid}
    """
    
    @ratelimit(key='ip', rate='3/s', method='DELETE')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='time_tracking_entry_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the time tracking entry.',
                required=True
            ),
            OpenApiParameter(
                name='opt_pretty',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Provides “pretty” output.
Provides the response in a “pretty” format. In the case of JSON this means doing proper line breaking and indentation to make it readable. This will take extra time and increase the response size so it is advisable only to use this during debugging.',
                required=False
            ),
        ],
        responses={
            200: OpenApiResponse(
                response=DeleteTimeTrackingEntryResponseSerializer,
                description="Successfully deleted the specified time tracking entry.",
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
        summary="Delete a time tracking entry",
        description="",
        tags=["Time tracking entries"]
    )
    def delete(self, request, time_tracking_entry_gid: str):
        # Validate time_tracking_entry_gid format
        try:
            validate_uuid(time_tracking_entry_gid)
        except Exception:
            return Response(
                invalid_gid_error("time_tracking_entry_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize dependencies
        storage = StorageImplementation()
        presenter = DeleteTimeTrackingEntryPresenterImplementation()
        interactor = DeleteTimeTrackingEntryInteractor(
            storage=storage,
            presenter=presenter
        )
        
        try:
            # Execute business logic
            response = interactor.delete_time_tracking_entry(
                time_tracking_entry_gid=time_tracking_entry_gid,
            )
            
            return Response(response, status=status.HTTP_204_NO_CONTENT)
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
