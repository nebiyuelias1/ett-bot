from guide_addis_bot.models import Vehicle


def create_vehicle(**kwargs):
    return Vehicle.objects.create(**kwargs)
