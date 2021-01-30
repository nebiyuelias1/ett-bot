from django.db import models
from django.db.models import CASCADE

from django_tgbot.models import AbstractTelegramUser, AbstractTelegramChat, AbstractTelegramState


class TelegramUser(AbstractTelegramUser):
    pass


class TelegramChat(AbstractTelegramChat):
    pass


class TelegramState(AbstractTelegramState):
    telegram_user = models.ForeignKey(TelegramUser, related_name='telegram_states', on_delete=CASCADE, blank=True,
                                      null=True)
    telegram_chat = models.ForeignKey(TelegramChat, related_name='telegram_states', on_delete=CASCADE, blank=True,
                                      null=True)

    class Meta:
        unique_together = ('telegram_user', 'telegram_chat')


class Vehicle(models.Model):
    """A vehicle that is registered by bot users that can be rented."""

    # The telegram user that created registered the vehicle.
    telegram_user = models.ForeignKey(TelegramUser,
                                      related_name='+',
                                      on_delete=CASCADE,
                                      blank=True,
                                      null=True)

    # Whether or not this vehicle is approved for rent by the site admin.
    is_approved = models.BooleanField(default=False)

    # The make of the vehicle, for example, Toyota, Nissan, etc.
    make = models.CharField(max_length=50, null=False, blank=False)

    # The model of the card, for example, Toyota Corolla, Toyota Vitz, etc.
    model = models.CharField(max_length=100, null=False, blank=False)

    # A photograph for the vehicle uploaded by the owner.
    photo = models.ImageField(upload_to='vehicle_photos', null=True, blank=True)

    # The total number of seats in vehicle.
    number_of_seats = models.IntegerField(null=False, blank=False)
