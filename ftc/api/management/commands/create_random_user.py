from datetime import datetime, timedelta
import random
from random import choice
from string import digits

from django.core.management import BaseCommand

from events.models.dict import Type
from events.models.event import Event
from events.serializers.event import EventPostSerializer
from locations.models.location import Location
from sports.models.sport import Sport
from users.models import User


class Command(BaseCommand):
    help = 'Создание события'

    NAMES = ['Александра', 'Алина', 'Алла', 'Анастасия', 'Анжела', 'Анна', 'Антонина', 'Валентина', 'Валерия', 'Вероника', 'Виктория', 'Галина', 'Дарья', 'Евгения', 'Екатерина', 'Елена', 'Елизавета', 'Карина', 'Кира', 'Клавдия', 'Кристина', 'Ксения', 'Лидия', 'Любовь', 'Людмила', 'Маргарита', 'Марина', 'Мария', 'Надежда', 'Наталья', 'Нина', 'Оксана', 'Олеся', 'Ольга', 'Полина', 'Светлана', 'Таисия', 'Тамара', 'Татьяна', 'Эвелина', 'Эльвира', 'Юлиана', 'Юлия', 'Яна', 'Александр', 'Алексей', 'Анатолий', 'Андрей', 'Антон', 'Аркадий', 'Артем', 'Борислав', 'Вадим', 'Валентин', 'Валерий', 'Василий', 'Виктор', 'Виталий', 'Владимир', 'Вячеслав', 'Геннадий', 'Георгий', 'Григорий', 'Даниил', 'Денис', 'Дмитpий', 'Евгений', 'Егор', 'Иван', 'Игорь', 'Илья', 'Кирилл', 'Лев', 'Максим', 'Михаил', 'Никита', 'Николай', 'Олег', 'Семен', 'Сергей', 'Станислав', 'Степан', 'Федор', 'Юрий']
    LAST_NAMES = ['Смирнов', 'Иванов', 'Кузнецов', 'Соколов', 'Попов', 'Лебедев', 'Козлов', 'Новиков', 'Морозов', 'Петров', 'Волков', 'Соловьёв', 'Васильев', 'Зайцев', 'Павлов', 'Семёнов', 'Голубев', 'Виноградов', 'Богданов', 'Воробьёв', 'Фёдоров', 'Михайлов', 'Беляев', 'Тарасов', 'Белов', 'Комаров', 'Орлов', 'Киселёв', 'Макаров', 'Андреев', 'Ковалёв', 'Ильин', 'Гусев', 'Титов', 'Кузьмин', 'Кудрявцев', 'Баранов', 'Куликов', 'Алексеев', 'Степанов', 'Яковлев', 'Сорокин', 'Сергеев', 'Романов', 'Захаров', 'Борисов', 'Королёв', 'Герасимов', 'Пономарёв', 'Григорьев']

    def handle(self, *args, **options):
        options.setdefault('interactive', False)
        try:
            user = User(
                first_name=self.NAMES[random.randrange(len(self.NAMES))],
                last_name=self.LAST_NAMES[random.randrange(len(self.LAST_NAMES))],
                phone_number='+7988' + ''.join(choice(digits) for i in range(7)),
                email='guest_' + ''.join(choice(digits) for i in range(7)) + '@mail.ru',
            )
            user.save()

            self.stdout.write(self.style.SUCCESS(
                f'Успешно создан пользователь  {user.id}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(
                f'Ошибока создания пользователя: {e}'))
