# Free Team Club

Проект объениния людей для команндого участия в событиях. Создавайте события,
приглашаейте другей, создавайте команды и участвуйте в событиях вместе.

Требования
===

- Python 3.9
- Django==4.0

Установка
===

- Установка зависимостей `pip install -r requirements.txt`


## Правила написания коммитов
Это вольный перевод, упрощенный местами [Angular commit style](https://github.com/angular/angular.js/blob/master/DEVELOPERS.md#commits)

Каждое сообщение коммита состоит из заголовка, тела и колонтитула. Заголовок имеет специальный формат, который включает тип и тему:
```
<type>: <subject>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```
Заголовок является обязательным, остальное - необязательной (есть исключения).

Любая строка сообщения о фиксации не может быть длиннее 100 символов! Это позволяет легче читать сообщение на GitHub, а также в различных инструментах git.

### Типы (`<type>`)
 - **feat**: Новая функция
 - **fix**: Исправление ошибки
 - **docs**: Изменения только в документации.
 - **style**: Изменения, не влияющие на смысл кода (пробелы, форматирование, отсутствие точек с запятой и т. д.).
 - **refactor**: Изменение кода, которое не исправляет ошибку и не добавляет функции.
 - **perf**: Изменение кода, улучшающее производительность.
 - **test**: Добавление недостающих или исправление существующих тестов.
 - **chore**: Изменения в процессе сборки или вспомогательных инструментах и библиотеках, таких как создание документации.

### Заголовок (`<subject>`)
Тема содержит краткое описание изменения:
- не делайте первую букву заглавной
- нет ставьте точки (.) в конце

### Тело сообщения (`<body>`)
Тело должно включать мотивацию к изменению и противопоставлять это предыдущему поведению.

### Футер (`<footer>`)
Нижний колонтитул должен содержать любую информацию о критических изменениях, а также место для ссылки на проблемы GitHub, которые закрывает этот коммит. (Пулл запрос)

Критические изменения должны начинаться со слова **BREAKING CHANGE**: с пробела или двух символов новой строки. Затем для этого используется остальная часть сообщения фиксации. Подробное объяснение можно найти в этом документе.

### Примеры коммитов
```
docs: поправлен README.md
```
```
feat: новая точка в API

Добавлена новая точка для создания пользователя:
- можно создать пользоватя простого
- обязателен номер телефона
```
```
fix: поправлена регистрацию юзера

Теперь не падает, если не передать пол
```
```
fix: поправлена регистрацию юзера

Теперь не падает если не передать пол
```
```
fix: поправлена регистрацию юзера

Переделана логика регистрации

BREAKING CHANGE: поменялся набор полей, внимательнее к документации
```

## Built With

* [Django](https://www.djangoproject.com/) -  web framework written in Python.
* [Django REST](https://www.django-rest-framework.org/) - Django REST framework is a powerful and flexible toolkit for building Web APIs.
* [Djoser](https://djoser.readthedocs.io/en/latest/getting_started.html) - Token based authentication from DRF.
* [Simple JWT](https://github.com/SimpleJWT/django-rest-framework-simplejwt) - Simple JWT is a JSON Web Token authentication plugin for the Django REST Framework.
* [Django-filter](https://pypi.org/project/django-filter/) - Python library for declaratively add dynamic QuerySet filtering from URL parameters.
* [Django environ’s](https://django-environ.readthedocs.io/en/latest/) - Django-environ allows to utilize 12factor inspired environment variables to configure Django application.
* [drf-yasg](https://drf-yasg.readthedocs.io/en/stable/readme.html) - Generate real Swagger/OpenAPI 2.0 specifications from a Django Rest Framework API.
* [CORS](https://pypi.org/project/django-cors-headers/) - A Django App that adds Cross-Origin Resource Sharing (CORS) headers to responses.
* [Django Extensions](https://django-extensions.readthedocs.io/en/latest/index.html) - Django Extensions is a collection of custom extensions for the Django Framework.
* [Django-CRUM](https://django-crum.readthedocs.io/en/latest/) - Django-CRUM (Current Request User Middleware) captures the current request and user in thread local storage.

## Make команды

* **run** - запуск сервера разработки.
* **migrate** - синхронизация состояние базы данных с текущим состоянием моделей и миграций.
* **superuser** - создание администратора.
* **shell** - запуск интерактивного интерпретатора.
* **shell_plus** - запуск интерактивного интерпретатора для тестирования SQL запросов.
* **static** - инициализация статических файлов.
* **start** - инициализация тестовых данных.
* **get-packages** - запись списка используемых пакетов в проекте.
* **install-packages** - установка необходимых пакетов для проекта.


## Celery

Команда для запуска прослушивания очереди `celery -A club worker -E`
