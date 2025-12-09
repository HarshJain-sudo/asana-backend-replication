from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_rules.interactors.trigger_rule_interactor import (
    TriggerRuleInteractor
)
from asana_rules.storages.storage_implementation import (
    StorageImplementation
)
from asana_rules.presenters.trigger_rule_presenter_implementation import (
    TriggerRulePresenterImplementation
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error,
    invalid_gid_error,
    missing_field_error,
    server_error,
)


class TriggerRuleView(APIView):
    """
    Trigger a rule
    Matches Asana API: POST /rule_triggers/{rule_trigger_gid}/run
    """
    
    @ratelimit(key='ip', rate='5/s', method='POST')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='rule_trigger_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The ID of the incoming web request trigger. This value is a path parameter that is automatically generated for the API endpoint.',
                required=True
            ),
        ],
        request=TriggerRuleRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=TriggerRuleResponseSerializer,
                description="Successfully triggered a rule.",
            ),
            400: OpenApiResponse(
                description="This usually occurs because of a missing or malformed parameter. Check the documentation and the syntax of your request and try again.",
            ),
            401: OpenApiResponse(
                description="A valid authentication token was not provided with the request, so the API could not associate a user with the request.",
            ),
            402: OpenApiResponse(
                description="The request was valid, but the queried object or object mutation specified in the request is above your current premium level.",
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
        summary="Trigger a rule",
        description="",
        tags=["Rules"]
    )
    def post(self, request, rule_trigger_gid: str):
        # Validate rule_trigger_gid format
        try:
            validate_uuid(rule_trigger_gid)
        except Exception:
            return Response(
                invalid_gid_error("rule_trigger_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Initialize dependencies
        storage = StorageImplementation()
        presenter = TriggerRulePresenterImplementation()
        interactor = TriggerRuleInteractor(
            storage=storage,
            presenter=presenter
        )
        
        # Validate request data
        serializer = TriggerRuleRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = {
                'errors': [{
                    'message': f"rules: {str(serializer.errors)}",
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
            response = interactor.trigger_rule(
                rule_trigger_gid=rule_trigger_gid,
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
