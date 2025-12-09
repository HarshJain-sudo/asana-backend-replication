from django.urls import path
from asana_webhooks.views.get_webhook.get_webhook_view import (
    GetWebhookView
)
from asana_webhooks.views.get_webhooks.get_webhooks_view import (
    GetWebhooksView
)

app_name = 'asana_webhooks'

urlpatterns = [
    path('webhooks/', GetWebhooksView.as_view(), name='get_webhooks'),
    path(
        'webhooks/<str:webhook_gid>/',
        GetWebhookView.as_view(),
        name='get_webhook'
    ),
]

