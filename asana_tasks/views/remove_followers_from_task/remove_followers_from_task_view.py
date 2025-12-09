from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_tasks.interactors.remove_followers_from_task_interactor import (
    RemoveFollowersFromTaskInteractor
)
from asana_tasks.storages.storage_implementation import (
    StorageImplementation
)
from asana_tasks.presenters.get_task_presenter_implementation import (
    GetTaskPresenterImplementation
)
from asana_tasks.serializers import TaskFollowerSerializer
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class RemoveFollowersFromTaskView(APIView):
    @ratelimit(key='ip', rate='5/s', method='POST')
    def post(self, request, task_gid: str):
        try:
            validate_uuid(task_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid task GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TaskFollowerSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                {'errors': [{'message': str(serializer.errors)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetTaskPresenterImplementation()
        interactor = RemoveFollowersFromTaskInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            follower_gids = [str(gid) for gid in serializer.validated_data['followers']]
            response = interactor.remove_followers_from_task(task_gid, follower_gids)
            return Response(response, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_400_BAD_REQUEST
            )

