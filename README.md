
# Журнал Дежурства

Система совместной работы над задачами для сменных работников.

## Для чего?

 - Для совместной работы над задачами сменными работниками, особенно когда они не встречаются лично.
 - Учет выполнения задач.
 - "Передача смены" с генерацией отчета в формате Excel.
 - Ознакомление работников с задачами, поручениями и документами с фиксацией времени ознакомления.


## Features

- Контроль ознакомления пользователей с задачами и сообщениями о ходе их выполнения.
- Поток уведомлений (activity stream) о действиях пользователей в разделе "Журнал".
- Сохранение предыдущей версии задачи, комментария при их изменении.
- Архив задач и комментариев (пользователи не могут их удалить бесследно).
- Личные задачи пользователей.
- Быстрый поиск по задачам и комментариям к ним.
- Поддержка [Markdown](https://daringfireball.net/projects/markdown/basics) в задачах, комментариях и поручениях.

## Используемые технологии и библиотеки

### Backend

- Python 3.10 / [Django 4](https://www.djangoproject.com)
- - `whitenoise` - раздача статических файлов.
- - `django-notifications-hq` - журнал активности пользователей.
- - `XlsxWriter` - генерация отчетов в формате Excel.
- - `Markdown` - разметка Markdown в задачах, комментариях и поручениях.
- - `django-bleach` - очистка от HTML-тегов.
- - `djangorestframework` - API для Vue-фронтенда.
- [SQLite](https://sqlite.org/index.html) - проект не рассчитывался на значительное количество одновременно работающих 
пользователей, поэтому выбрана данная БД из-за её простоты, удобства отладки и резервного копирования. 
- Redis
- Celery
- [Nginx](https://www.nginx.com) / [Gunicorn](https://gunicorn.org) 
- [Docker Compose](https://docs.docker.com/compose/)
- [Coverage.py](https://coverage.readthedocs.io/en/7.2.1/)
- [Rollbar](https://rollbar.com)

### Frontend

- [Bootstrap 5](https://getbootstrap.com) / [Font Awesome](https://fontawesome.com)
- [HTMX 1.8.4](https://htmx.org)
- [Vue 3](https://vuejs.org) - используется в табличном виде задач используется для создания удобного реактивного интерфейса.
- [Axios](https://github.com/axios/axios)
- [Marked.js](https://marked.js.org)
- [DOMPurify](https://github.com/cure53/DOMPurify)


## Деплой

Для установки и запуска проекта, необходимо склонировать репозиторий,
создать файл `docker-compose.yml` по одному из прилагаемых шаблонов
(`dev` или `prod`), задать в нём корректные переменные окружения,
и затем запустить командой `sudo docker compose up -d`.
При первом запуске необходимо также выполнить команду миграции БД
и создать учетную запись администратора:

```bash
  git clone ttps://github.com/hazadus/journal
  cd ./journal
  cp ./docker-compose.prod.yml ./docker-compose.yml
  nano ./docker-compose.yml
  sudo docker compose up -d --build
  sudo docker exec journal-web python -m manage migrate
  sudo docker exec journal-web python -m manage createsuperuser
```


## Переменные окружения
Для корректного запуска проекта, необходимо установить следующие
переменные окружения в файле `docker-compose.yml`:

- `SECRET_KEY`: стандартный secret key для Django.
- `HOST_NAME`: адрес сайта вида `http://127.0.0.1` (без `/` на конце).
- `ROLLBAR_ACCESS_TOKEN`: токен [Rollbar](https://rollbar.com), необходимо получить на их сайте.
- `TELEGRAM_BOT_TOKEN`: токен телеграм-бота для информирования.
- `TELEGRAM_ADMIN_ID`: ID админа в телеграм, который будет получать уведомления о событиях на сайте.

## Структура проекта Django

Django apps:
- `journal`
- `documents`
- `users`
- `core`

Директории и файлы:
- `vue-tasks-table-view` - приложение на Vue для варианта табличного вида списка задач
- `static/vue/task-table-view` - сюда генерятся файлы при сборке приложения Vue командой `npm run build`.
- `db.sqlite3` - файл БД.
- `media/files` - файлы, загружаемые в качестве приложений к задачам и документам.
- `media/images` - изображения профилей пользователей.
- `media/reports` - отчеты, генерируемые командой `create_report`.
- `data/redis` - данные БД Redis.
- `docker/nginx/default.conf` - конфигурационный файл Nginx.
- `docker/nginx/logs/` - логи Nginx.
- `.coveragerc` - настройки `coverage.py`
- `htmlcov/` - отчеты `coverage.py` (генерируются при запуске `make up`, `make test`).

## Запуск тестов

Тесты запускаются стандартной для Django командой при запущенном в фоне (с опцией `-d`) проекте:

```bash
  docker exec journal-web python -m manage test
```

Для запуска с `coverage.py`:
```bash
  docker exec journal-web coverage run --source='.' -m manage test
  docker exec journal-web coverage html
```


## Планируемые доработки

Все запланированые изменения и доработки можно увидеть в разделе
[Issues](https://github.com/hazadus/journal/issues).

## Известные проблемы
- Из-за особенностей работы SQLite с кириллицей, поиск по задачам и комментариям к ним чувствителен к регистру 
кириллических символов в поисковом запросе.