# Лабораторная работа № 1

Приложение «Мой блог» на FastAPI.

## Запуск

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

## Запуск в Docker

```powershell
docker compose up -d --build --wait
```

Оба способа запуска используют порт 8000. Перед сменой способа остановите приложение. Для остановки контейнера выполните `docker compose down`.

## Проверка

| Запрос | Ожидаемый ответ |
| --- | --- |
| `GET /` | `{"message":"Привет, мир!"}` |
| `GET /about` | `{"name":"Мой блог","version":"1.0"}` |

«Атлас API» доступен по адресу http://127.0.0.1:8000/docs.

Оформление страницы /docs описано в [web/README.md](web/README.md).
