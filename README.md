# Лабораторная работа № 3

Посты и пользователи хранятся в PostgreSQL 17. Доступ к БД идёт через асинхронные сессии SQLAlchemy и репозитории. Первая миграция Alembic создаёт таблицы `post.post` и `users.user`.

## Запуск

В PowerShell из каталога проекта выполните команды.

```powershell
Copy-Item .env.example .env
docker compose up -d --build --wait
```

Первая команда нужна при первичной настройке. `.env` содержит параметры локальной базы. Compose запускает PostgreSQL, а контейнер приложения применяет миграции перед запуском Uvicorn.

Для локального PostgreSQL с созданной базой `blog_api` и настройками из `.env` можно запустить приложение напрямую.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements/requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn main:app
```

Для остановки контейнеров используйте `docker compose down`. Данные сохраняются в томе `postgres_data`.

## Проверка

Откройте Swagger UI по адресу http://127.0.0.1:8000/docs.

| Действие | Посты | Пользователи |
| --- | --- | --- |
| Создать | `POST /post` | `POST /user` |
| Получить список | `GET /post/many` | `GET /user/many` |
| Получить запись | `GET /post/{id}` | `GET /user/{id}` |
| Редактировать | `PUT /post/{id}` | `PUT /user/{id}` |
| Удалить | `DELETE /post/{id}` | `DELETE /user/{id}` |

Пример поста — `{"name":"Первый пост","authorName":"Bob","content":"Привет!"}`. Пример пользователя — `{"username":"Bob","email":"bob@example.com","login":"bob","password":"sample-pass-1"}`. При удалении запись помечается в БД и пропадает из выборок. Пароли в БД хешируются с bcrypt. Ответы на контрольные вопросы приведены в [CHANGELOG.md](CHANGELOG.md).
