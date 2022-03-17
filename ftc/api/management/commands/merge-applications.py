from django.core.management import BaseCommand

from events.models.application import Application


class Command(BaseCommand):
    help = 'Убрать игрока и добавить юзера'

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        count = 0
        apps = Application.objects.all()
        for app in apps:
            if app.player and not app.user:
                app.user = app.player.user
                app.save()
                count += 1
        self.stdout.write(self.style.SUCCESS(
            f'Успешно изменено {count} заявок')
        )
