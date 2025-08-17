# messaging_app/chats/filters.py

import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from chats.models import Message
from django.utils import timezone


class MessageFilter(django_filters.FilterSet):
    start_time = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='gte')
    end_time = django_filters.DateTimeFilter(field_name="sent_at", lookup_expr='lte')
    sender_id = django_filters.UUIDFilter(field_name="sender__user_id")
    conversation_id = django_filters.UUIDFilter(field_name="conversation__conversation_id")

    class Meta:
        model = Message
        fields = ['sender_id', 'conversation_id', 'start_time', 'end_time']
