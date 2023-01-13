
# Журнал Дежурства

Система совместной работы над задачами для сменных работников.

## Для чего

Сменные работники, особенно когда они не встречаются лично; "передача смены".


## Features

- Совместная работа над задачами
- Контроль ознакомления пользователей с задачами и сообщениями о ходе их выполнения
- Архив задач и комментариев (пользователи не могут их удалить бесследно)
- Личные задачи пользователей

## Tech stack used

- Python 3.10 / Django 4 / Gunicorn 
- Bootstrap 5 / Font Awesome
- HTMX 1.8.4
- SQLite
- Nginx
- Docker Compose
- Rollbar


## Deployment

To deploy this project run

```bash
  git clone ...
  sudo docker compose up -d
```


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`API_KEY`

`ANOTHER_API_KEY`

## Структура проекта Django

Описание apps и папок в проекте.


## Running Tests

To run tests, run the following command

```bash
  npm run test
```


## FAQ

#### Question 1

Answer 1

#### Question 2

Answer 2

