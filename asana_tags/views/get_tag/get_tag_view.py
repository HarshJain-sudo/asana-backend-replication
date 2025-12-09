from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiParameter,
    OpenApiExample
)
from asana_tags.interactors.get_tag_interactor import (
    GetTagInteractor
)
from asana_tags.interactors.update_tag_interactor import (
    UpdateTagInteractor
)
from asana_tags.interactors.delete_tag_interactor import (
    DeleteTagInteractor
)
from asana_tags.storages.storage_implementation import (
    StorageImplementation
)
from asana_tags.presenters.get_tag_presenter_implementation import (
    GetTagPresenterImplementation
)
from asana_tags.serializers import (
    TagUpdateRequestSerializer,
    TagSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_tags.exceptions.custom_exceptions import (
    TagDoesNotExistException,
    TagAlreadyExistsException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetTagView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='tag_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the tag.',
                required=True
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
                response=TagSingleResponseSerializer,
                description="Successfully retrieved the specified tag."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="This usually occurs because of a missing or malformed parameter."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist."
            ),
        },
        summary="Get a tag",
        description="Returns the complete tag record for a single tag.",
        tags=["Tags"]
    )
    def get(self, request, tag_gid: str):
        import json
        
        opt_pretty = request.query_params.get('opt_pretty', 'false').lower() == 'true'
        
        try:
            validate_uuid(tag_gid)
        except Exception:
            error_response = {
                'errors': [{
                    'message': 'tag: Invalid GID format',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)

        storage = StorageImplementation()
        presenter = GetTagPresenterImplementation()
        interactor = GetTagInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_tag(tag_gid)
            
            if opt_pretty:
                response_data = json.dumps(response, indent=2, ensure_ascii=False)
                return Response(
                    json.loads(response_data),
                    status=status.HTTP_200_OK
                )
            
            return Response(response, status=status.HTTP_200_OK)
        except TagDoesNotExistException as e:
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
    
    @ratelimit(key='ip', rate='5/m', method='PUT')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='tag_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the tag.',
                required=True
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
        request=TagUpdateRequestSerializer,
        responses={
            200: OpenApiResponse(
                response=TagSingleResponseSerializer,
                description="Successfully updated the specified tag."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="This usually occurs because of a missing or malformed parameter."
            ),
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist."
            ),
        },
        summary="Update a tag",
        description="Updates the properties of a tag. Only the fields provided in the data block will be updated.",
        tags=["Tags"]
    )
    def put(self, request, tag_gid: str):
        import json
        
        opt_pretty = request.query_params.get('opt_pretty', 'false').lower() == 'true'
        
        try:
            validate_uuid(tag_gid)
        except Exception:
            error_response = {
                'errors': [{
                    'message': 'tag: Invalid GID format',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = TagUpdateRequestSerializer(data=request.data)
        if not serializer.is_valid():
            error_response = {
                'errors': [{
                    'message': f"tag: {str(serializer.errors)}",
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        storage = StorageImplementation()
        presenter = GetTagPresenterImplementation()
        interactor = UpdateTagInteractor(
            storage=storage,
            presenter=presenter
        )
        
        try:
            response = interactor.update_tag(
                tag_gid=tag_gid,
                **serializer.validated_data
            )
            
            if opt_pretty:
                response_data = json.dumps(response, indent=2, ensure_ascii=False)
                return Response(
                    json.loads(response_data),
                    status=status.HTTP_200_OK
                )
            
            return Response(response, status=status.HTTP_200_OK)
        except TagDoesNotExistException as e:
            error_response = {
                'errors': [{
                    'message': str(e),
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_404_NOT_FOUND)
        except TagAlreadyExistsException as e:
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
    
    @ratelimit(key='ip', rate='5/m', method='DELETE')
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='tag_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='Globally unique identifier for the tag.',
                required=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Successfully deleted the specified tag.",
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
            404: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Either the request method and path supplied do not specify a known action in the API, or the object specified by the request does not exist."
            ),
        },
        summary="Delete a tag",
        description="A specific, existing tag can be deleted by making a DELETE request on the URL for that tag.",
        tags=["Tags"]
    )
    def delete(self, request, tag_gid: str):
        try:
            validate_uuid(tag_gid)
        except Exception:
            error_response = {
                'errors': [{
                    'message': 'tag: Invalid GID format',
                    'help': 'For more information on API status codes and how to handle them, read the docs on errors: https://asana.github.io/developer-docs/#errors',
                    'phrase': '6 sad squid snuggle softly'
                }]
            }
            return Response(error_response, status=status.HTTP_400_BAD_REQUEST)
        
        storage = StorageImplementation()
        interactor = DeleteTagInteractor(storage=storage)
        
        try:
            interactor.delete_tag(tag_gid)
            return Response({'data': {}}, status=status.HTTP_200_OK)
        except TagDoesNotExistException as e:
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

