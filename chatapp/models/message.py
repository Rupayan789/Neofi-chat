import uuid

from django.core.exceptions import ValidationError
from django.db import models
from .user import User


def validate_message_content(content):
    if content is None or content == "" or content.isspace():
        raise ValidationError(
            'Content is empty/invalid',
            code='invalid',
            params={'content': content},
        )


class Message(models.Model):

    id = models.UUIDField(
        primary_key=True,
        null=False,
        default=uuid.uuid4,
        editable=False
    )
    author = models.ForeignKey(
        User,
        blank=False,
        null=False,
        related_name='author_messages',
        on_delete=models.CASCADE
    )
    content = models.TextField(validators=[validate_message_content])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    room_name = models.TextField(blank=True)

    def last_50_messages(self,room_name):
        return Message.objects.filter(room_name=room_name).order_by('created_at').all().values('id','content','author','room_name','created_at')[:50]
