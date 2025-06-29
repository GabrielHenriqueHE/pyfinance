import uuid

from django.db import models
from django.utils import timezone


class BaseModel(models.Model):

    id = models.UUIDField(
        primary_key=True, db_column="id", name="id", default=uuid.uuid4, editable=False
    )

    created_at = models.DateTimeField(
        db_column="created_at",
        name="created_at",
        null=False,
        default=timezone.now,
        editable=False,
    )

    updated_at = models.DateTimeField(
        db_column="updated_at", name="updated_at", auto_now=True
    )

    class Meta:
        abstract = True
