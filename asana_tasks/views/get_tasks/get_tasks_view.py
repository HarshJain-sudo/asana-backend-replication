from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import (
    extend_schema, 
    OpenApiParameter,
    OpenApiResponse
)
from asana_tasks.interactors.get_tasks_interactor import (
    GetTasksInteractor
)
from asana_tasks.storages.storage_implementation import (
    StorageImplementation
)
from asana_tasks.presenters.get_tasks_presenter_implementation import (
    GetTasksPresenterImplementation
)
from asana_tasks.serializers import (
    TaskListResponseSerializer,
    TaskCreateRequestSerializer,
    TaskSerializer,
    TaskSingleResponseSerializer,
    ErrorResponseSerializer
)
from asana_tasks.interactors.create_task_interactor import (
    CreateTaskInteractor
)
from asana_tasks.presenters.get_task_presenter_implementation import (
    GetTaskPresenterImplementation
)
from asana_tasks.constants.constants import (
    DEFAULT_OFFSET,
    DEFAULT_LIMIT,
    MAX_LIMIT,
)
from asana_backend.utils.validators import validate_pagination_params
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetTasksView(APIView):
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='limit',
                type=int,
                location=OpenApiParameter.QUERY,
                description='Results per page. The number of objects to return per page. The value must be between 1 and 100.',
                required=False
            ),
            OpenApiParameter(
                name='offset',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Offset token. An offset to the next page returned by the API.',
                required=False
            ),
            OpenApiParameter(
                name='assignee',
                type=str,
                location=OpenApiParameter.QUERY,
                description='The assignee to filter tasks on. If searching for unassigned tasks, assignee.any = null can be specified. Note: If you specify assignee, you must also specify the workspace to filter on.',
                required=False
            ),
            OpenApiParameter(
                name='project',
                type=str,
                location=OpenApiParameter.QUERY,
                description='The project to filter tasks on.',
                required=False
            ),
            OpenApiParameter(
                name='section',
                type=str,
                location=OpenApiParameter.QUERY,
                description='The section to filter tasks on.',
                required=False
            ),
            OpenApiParameter(
                name='workspace',
                type=str,
                location=OpenApiParameter.QUERY,
                description='The workspace to filter tasks on. Note: If you specify workspace, you must also specify the assignee to filter on.',
                required=False
            ),
            OpenApiParameter(
                name='completed_since',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Only return tasks that are either incomplete or that have been completed since this time. Format: date-time (ISO 8601)',
                required=False
            ),
            OpenApiParameter(
                name='modified_since',
                type=str,
                location=OpenApiParameter.QUERY,
                description='Only return tasks that have been modified since the given time. Format: date-time (ISO 8601)',
                required=False
            ),
            OpenApiParameter(
                name='opt_fields',
                type=str,
                location=OpenApiParameter.QUERY,
                description='This endpoint returns a resource which excludes some properties by default. To include those optional properties, set this query parameter to a comma-separated list of the properties you wish to include.',
                required=False
            )
        ],
        responses={
            200: TaskListResponseSerializer,
            400: ErrorResponseSerializer
        },
        summary="Get multiple tasks",
        description="Returns the compact task records for some filtered set of tasks. Use one or more of the parameters provided to filter the tasks returned. You must specify a project or tag if you do not specify assignee and workspace.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request):
        try:
            # Handle offset - can be int or string token
            offset_param = request.query_params.get('offset', '0')
            try:
                offset = int(offset_param)
            except ValueError:
                # If it's a token, treat as 0 for now (token-based pagination not fully implemented)
                offset = 0
            
            limit_param = request.query_params.get('limit')
            limit = int(limit_param) if limit_param else DEFAULT_LIMIT
            
            offset, limit = validate_pagination_params(
                offset=offset,
                limit=limit,
                max_limit=MAX_LIMIT
            )
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Extract parameters matching API spec names
        workspace = request.query_params.get('workspace')
        assignee = request.query_params.get('assignee')
        project = request.query_params.get('project')
        section = request.query_params.get('section')
        completed_since = request.query_params.get('completed_since')
        modified_since = request.query_params.get('modified_since')
        opt_fields = request.query_params.get('opt_fields')

        storage = StorageImplementation()
        presenter = GetTasksPresenterImplementation()
        interactor = GetTasksInteractor(
            storage=storage,
            presenter=presenter
        )

        response = interactor.get_tasks(
            workspace=workspace,
            assignee=assignee,
            project=project,
            section=section,
            completed_since=completed_since,
            modified_since=modified_since,
            opt_fields=opt_fields,
            offset=offset,
            limit=limit
        )
        return Response(response, status=status.HTTP_200_OK)
    
    @extend_schema(
        request=TaskCreateRequestSerializer,
        responses={
            201: OpenApiResponse(
                response=TaskSingleResponseSerializer,
                description="Task created successfully."
            ),
            400: OpenApiResponse(
                response=ErrorResponseSerializer,
                description="Bad Request - Invalid input data."
            )
        },
        summary="Create a new task",
        description="Creates a new task in the specified workspace.",
        tags=["Tasks"]
    )
    @ratelimit(key='ip', rate='5/s', method='POST')
    def post(self, request):
        """Create a new task"""
        serializer = TaskCreateRequestSerializer(data=request.data)
        
        if not serializer.is_valid():
            # Fallback to legacy format
            legacy_serializer = TaskSerializer(data=request.data)
            if legacy_serializer.is_valid():
                serializer = legacy_serializer
            else:
                return Response(
                    {'errors': [{'message': str(serializer.errors)}]},
                    status=status.HTTP_400_BAD_REQUEST
                )

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = CreateTaskInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            validated_data = serializer.validated_data.copy()
            
            # Handle both formats
            if 'workspace' in validated_data:
                validated_data['workspace'] = validated_data['workspace']
            elif 'workspace_gid' in validated_data:
                validated_data['workspace'] = str(
                    validated_data['workspace_gid']
                )
            
            if 'assignee' in validated_data and validated_data['assignee']:
                validated_data['assignee'] = validated_data['assignee']
            elif 'assignee_gid' in validated_data:
                validated_data['assignee'] = str(
                    validated_data['assignee_gid']
                ) if validated_data['assignee_gid'] else None
            
            response = interactor.create_task(**validated_data)
            return Response(response, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
