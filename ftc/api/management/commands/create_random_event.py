from datetime import datetime, timedelta
import random

from django.core.management import BaseCommand

from events.models.dict import Type
from events.models.event import Event
from events.serializers.event import EventPostSerializer
from locations.models.location import Location
from sports.models.sport import Sport


class Command(BaseCommand):
    help = 'Создание события'
    MIN_DAY = 1
    MAX_DAY = 14
    MIN_HOUR = 6
    MAX_HOUR = 20
    MIN_DURATION = 60
    MAX_DURATION = 150


    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        now = datetime.now().astimezone()

        types = Type.objects.filter(active=True)
        sports = Sport.objects.all()
        locations = Location.objects.filter(active=True)

        replace_hour = random.randrange(self.MIN_HOUR, self.MAX_HOUR)
        timedelta_days = random.randrange(self.MIN_DAY, self.MAX_DAY)
        duration_minutes = random.randrange(self.MIN_DURATION, self.MAX_DURATION, 10)


        type = types[random.randrange(0, types.count())]
        sport = sports[random.randrange(0, sports.count())]
        location = locations[random.randrange(0, locations.count())]

        time_start = (now.replace(hour=replace_hour, minute=0) +
                      timedelta(days=timedelta_days))
        time_end = time_start + timedelta(minutes=duration_minutes)

        price = random.randrange(200, 15000, 100)
        # случайным образом будет бесплатное участие
        if (price / 100) % 5 == 0:
            price = None

        event = Event(
            type=type,
            sport=sport,
            location=location,
            time_start=time_start,
            time_end=time_end,
            price=price,
            )
        print(event)
        obj = EventPostSerializer(event)

        serializer = EventPostSerializer(data=obj.data)
        if serializer.is_valid():
            event.save()
        self.stdout.write(self.style.SUCCESS(
            f'Успешно создано событие  {event.id}'))

