from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiResponse, OpenApiExample
from asana_projects.models.project import Project
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit
from asana_backend.utils.error_responses import (
    not_found_error, 
    invalid_gid_error,
    server_error
)


class DeleteProjectView(APIView):
    """
    Delete a project.
    Matches Asana API: DELETE /projects/{project_gid}
    """
    
    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='project_gid',
                type=str,
                location=OpenApiParameter.PATH,
                description='The project to delete',
                required=True
            ),
        ],
        responses={
            200: OpenApiResponse(
                description="Project deleted successfully",
                examples=[
                    OpenApiExample(
                        'Success Response',
                        value={"data": {}}
                    )
                ]
            ),
            400: OpenApiResponse(
                description="Invalid GID format",
                examples=[
                    OpenApiExample(
                        'Bad Request',
                        value={
                            "errors": [
                                {
                                    "message": "project_gid: Invalid GID format",
                                    "help": "For more information..."
                                }
                            ]
                        }
                    )
                ]
            ),
            404: OpenApiResponse(
                description="Project not found",
                examples=[
                    OpenApiExample(
                        'Not Found',
                        value={
                            "errors": [
                                {
                                    "message": "project: Unknown object: 12345",
                                    "help": "For more information..."
                                }
                            ]
                        }
                    )
                ]
            ),
        },
        summary="Delete a project",
        description="Deletes a project permanently.",
        tags=["Projects"]
    )
    @ratelimit(key='ip', rate='5/s', method='DELETE')
    def delete(self, request, project_gid: str):
        # Validate project GID format
        try:
            validate_uuid(project_gid)
        except Exception:
            return Response(
                invalid_gid_error("project_gid"),
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if project exists
        try:
            project = Project.objects.get(gid=project_gid)
        except Project.DoesNotExist:
            return Response(
                not_found_error("project", project_gid),
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Delete project
        try:
            project.delete()
        except Exception as e:
            return Response(
                server_error(str(e)),
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
        return Response({'data': {}}, status=status.HTTP_200_OK)
