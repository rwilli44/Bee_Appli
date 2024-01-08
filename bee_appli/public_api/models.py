# Third-party imports
from django.contrib.auth.models import User
from django.db import models
from django.db.models import CASCADE


class PublicContact(models.Model):
    """This model serves to store all Beekeepers who allow their
    contact information to be made public."""

    public_beekeeper_info = models.ForeignKey(
        User,
        on_delete=CASCADE,
        related_name="allows_public_contact",
    )
