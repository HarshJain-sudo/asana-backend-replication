from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_custom_fields.interactors.insert_enum_option_for_custom_field_interactor import (
    InsertEnumOptionForCustomFieldInteractor
)
from asana_custom_fields.storages.storage_implementation import (
    StorageImplementation
)
from asana_custom_fields.presenters.insert_enum_option_for_custom_field_presenter_implementation import (
    InsertEnumOptionForCustomFieldPresenterImplementation
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error,
    invalid_gid_error,
    missing_field_error,
    server_error,
)


class InsertEnumOptionForCustomFieldView(APIView):
    """
    Reorder a custom field's enum
    Matches Asana API: POST /custom_fields/{custom_field_gid}/enum_options/insert
    """
    
    @ratelimit(key='ip', rate='5/s', method='POST')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='custom_field_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the custom field.',
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
            OpenApiParameter(
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.',
                required=False
            ),
        ],
        request=InsertEnumOptionForCustomFieldRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=InsertEnumOptionForCustomFieldResponseSerializer,
                description="Custom field enum option successfully reordered.",
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
        summary="Reorder a custom field's enum",
        description="",
        tags=["Custom fields"]
    )
    def post(self, request, custom_field_gid: str):
        # Validate custom_field_gid format
        try:
            validate_uuid(custom_field_gid)
        except Exception:
            return Response(
                invalid_gid_error("custom_field_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize dependencies
        storage = StorageImplementation()
        presenter = InsertEnumOptionForCustomFieldPresenterImplementation()
        interactor = InsertEnumOptionForCustomFieldInteractor(
            storage=storage,
            presenter=presenter
        )
        
        # Validate request data
        serializer = InsertEnumOptionForCustomFieldRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = {
                'errors': [{
                    'message': f"custom fields: {str(serializer.errors)}",
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
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Execute business logic
            response = interactor.insert_enum_option_for_custom_field(
                custom_field_gid=custom_field_gid,
                **serializer.validated_data
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
