from django.urls import path
from asana_attachments.views.get_attachment.get_attachment_view import (
    GetAttachmentView
)
from asana_attachments.views.get_task_attachments.get_task_attachments_view import (
    GetTaskAttachmentsView
)

app_name = 'asana_attachments'

urlpatterns = [
    path(
        'attachments/<str:attachment_gid>/',
        GetAttachmentView.as_view(),
        name='get_attachment'
    ),
    path(
        'tasks/<str:task_gid>/attachments/',
        GetTaskAttachmentsView.as_view(),
        name='get_task_attachments'
    ),
]

