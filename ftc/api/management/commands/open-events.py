from datetime import datetime

from django.core.management import BaseCommand

from api.models import Event


class Command(BaseCommand):
    help = 'Открытие брони'

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        now = datetime.now().astimezone()
        count = 0

        wait_events = Event.objects.filter(status_id=2,
                                           time_start__lte=now)
        for event in wait_events:
            event.status_id = 3
            count += 1
            event.save()

        self.stdout.write(self.style.SUCCESS(
            f'Успешно открыто {count}')
        )
