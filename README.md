# Лабораторные работы по разработке серверных приложений

Учебный блог на FastAPI. Каждая ветка содержит результат своего этапа и инструкцию для его запуска.

| Ветка | Что реализовано |
| --- | --- |
| `feature/lab1` | `GET /`, `GET /about`, Dockerfile и Docker Compose |
| `feature/lab2` | Pydantic DTO, роутер, контроллер, зависимости и CRUD постов в памяти |
| `feature/lab3` | Асинхронный PostgreSQL 17, миграция Alembic и CRUD пользователей и постов |
| `feature/lab4` | Регистрация, вход, OAuth2, access и refresh JWT, обновление и отзыв сеанса |

## Запуск четвёртой работы

При первой настройке создайте `.env` и сгенерируйте ключ JWT с помощью Python 3.12.

```powershell
Copy-Item .env.example .env
$jwtKey = py -3.12 -c "from secrets import token_hex; print(token_hex(32))"
Add-Content -Path .env -Value "JWT_SECRET_KEY=$jwtKey"
docker compose up -d --build --wait
```

Compose поднимает базу PostgreSQL 17. Контейнер блога применяет обе миграции перед запуском API. Swagger UI доступен по адресу http://127.0.0.1:8000/docs. Для остановки выполните `docker compose down`. Данные остаются в томе PostgreSQL.

Если PostgreSQL уже запущен локально, создайте пустую базу `blog_api`, укажите параметры базы в `.env` и выполните команды.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements/requirements.txt
.\.venv\Scripts\python.exe -m alembic upgrade head
.\.venv\Scripts\python.exe -m uvicorn main:app
```

## Проверка JWT в Swagger

1. Вызовите `POST /authorization/register` с JSON `{"username":"Bob","email":"bob@example.com","login":"bob","password":"sample-pass-1"}`. Сохраните возвращённый ID пользователя.
2. Вызовите `POST /authorization/login` с JSON `{"login":"bob","password":"sample-pass-1"}`. Ответ содержит `accessToken` и `refreshToken`.
3. Передайте `{"accessToken":"<accessToken>"}` в `POST /authentication/verify_access_token`. Ожидается HTTP 200. Для доступа к защищённым маршрутам также можно нажать **Authorize** и ввести свой логин в поле **username**, а пароль в поле **password**. Swagger получит отдельную пару через `POST /authorization/token`.
4. Вызовите `POST /authentication/refresh_tokens` с JSON `{"refreshToken":"<refreshToken>"}`. Оба JWT прежней пары перестанут работать. Повторное обновление с прежним refresh-токеном вернёт HTTP 401.
5. Вызовите `POST /authentication/logout` с новым refresh-токеном. Ожидается HTTP 200 с телом `{}`. После этого проверка соответствующего access-токена вернёт HTTP 401.

По умолчанию access-токен действует 15 минут, refresh-токен — 7 дней. БД хранит идентификаторы токенов, сроки действия и связи между записями. Пароли хешируются через bcrypt.

## Маршруты блога

| Метод и путь | Действие |
| --- | --- |
| `GET /post/many`, `GET /post/{id}` | Читать посты |
| `POST /post`, `PUT /post/{id}`, `DELETE /post/{id}` | Создавать, изменять и удалять посты с access-токеном |
| `POST /user` | Зарегистрировать пользователя через тот же контроллер, что и `/authorization/register` |
| `GET /user/many` | Получить ID и имена пользователей с access-токеном |
| `GET /user/{id}`, `PUT /user/{id}`, `DELETE /user/{id}` | Читать, изменять и удалять собственный профиль |

Пример JSON поста — `{"name":"Первый пост","authorName":"Bob","content":"Привет!"}`. При изменении пароля или удалении аккаунта все сеансы пользователя отзываются. Для привязки постов к аккаунтам в методичке предусмотрен отдельный этап.

## Ветки и сдача

Ветки `feature/lab1`–`feature/lab4` содержат последовательные результаты. Целевая ветка для всех Merge Request — `develop`. Рассматривайте их в порядке от первой работы к четвёртой. После принятия предыдущей работы diff следующего запроса будет содержать её собственные изменения.

Ответы на вопросы лабораторных № 2–4 приведены в [CHANGELOG.md](CHANGELOG.md). Описание разработки и форматы API сверены с [документацией FastAPI](https://fastapi.tiangolo.com/tutorial/first-steps/), [SQLAlchemy](https://docs.sqlalchemy.org/en/20/dialects/postgresql.html), [Alembic](https://alembic.sqlalchemy.org/en/latest/cookbook.html) и [Docker Compose](https://docs.docker.com/reference/cli/docker/compose/up/).
