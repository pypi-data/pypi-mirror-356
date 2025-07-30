from django.db import models

TRACKING_COOKIE_NAME = "omnibus"


class EventType(models.TextChoices):
    download = "download"
