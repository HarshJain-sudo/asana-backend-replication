from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from asana_attachments.interactors.get_attachment_interactor import (
    GetAttachmentInteractor
)
from asana_attachments.storages.storage_implementation import (
    StorageImplementation
)
from asana_attachments.presenters.get_attachment_presenter_implementation import (
    GetAttachmentPresenterImplementation
)
from asana_attachments.exceptions.custom_exceptions import (
    AttachmentDoesNotExistException
)
from asana_backend.utils.validators import validate_uuid
from asana_backend.utils.decorators.ratelimit import ratelimit


class GetAttachmentView(APIView):
    @ratelimit(key='ip', rate='5/s', method='GET')
    def get(self, request, attachment_gid: str):
        # Validate UUID format
        try:
            validate_uuid(attachment_gid)
        except Exception:
            return Response(
                {'errors': [{'message': 'Invalid attachment GID format'}]},
                status=status.HTTP_400_BAD_REQUEST
            )

        storage = StorageImplementation()
        presenter = GetAttachmentPresenterImplementation()
        interactor = GetAttachmentInteractor(
            storage=storage,
            presenter=presenter
        )

        try:
            response = interactor.get_attachment(attachment_gid)
            return Response(response, status=status.HTTP_200_OK)
        except AttachmentDoesNotExistException as e:
            return Response(
                {'errors': [{'message': str(e)}]},
                status=status.HTTP_404_NOT_FOUND
            )

