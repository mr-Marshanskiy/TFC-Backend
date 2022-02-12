from datetime import datetime

from django.core.management import BaseCommand

from events.models.event import Event


class Command(BaseCommand):
    help = 'Закрытие или отмена броней'

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        now = datetime.now().astimezone()
        close_count = 0
        cancel_count = 0

        open_events = Event.objects.filter(status_id=3,
                                           time_start__lte=now)
        new_events = Event.objects.filter(status_id=1,
                                          time_start__lte=now)
        for event in open_events:
            event.status_id = 4
            close_count += 1
            event.save()

        for event in new_events:
            event.status_id = 5
            cancel_count += 1
            event.save()

        self.stdout.write(self.style.SUCCESS(
            f'Успешно закрыто {close_count}, отменено {cancel_count}')
        )
