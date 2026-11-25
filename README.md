# Лабораторная работа № 2

Блог хранит посты в памяти процесса. FastAPI внедряет репозиторий в контроллер через `Depends`. После перезапуска данные возвращаются к исходному набору.

## Запуск в PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements/requirements.txt
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Для запуска в Docker выполните `docker compose up -d --build --wait`. Оба способа используют порт 8000. Для остановки контейнера выполните `docker compose down`.

## Проверка

В «Атлас API» по адресу http://127.0.0.1:8000/docs отправьте `POST /post` с JSON `{"authorName":"Bob","content":"Новый пост"}`. Используйте полученный ID в `GET /post/{id}`, `PUT /post/{id}` и `DELETE /post/{id}`. Список постов доступен по `GET /post/many`. Маршруты `GET /` и `GET /about` из первой работы также доступны.

Ответы на контрольные вопросы приведены в [CHANGELOG.md](CHANGELOG.md).

Оформление страницы /docs описано в [web/README.md](web/README.md).
