# Проект QRKot - приложение для Благотворительного фонда поддержки котиков

## Функции проекта

* регистрация пользователей, возможность изменения данных о пользователе. 
* создание благотворительных проектов, их изменение и удаление
* возможность сделать пожертвование в фонд. Распределение пожертвований 
происходит автоматически.
* получение отчёта о скорости закрытия проектов в виде google-таблицы.

## Стек технологий
* [Python](https://www.python.org/)
* [FastAPI](https://fastapi.tiangolo.com/)
* [Aiogoogle](https://aiogoogle.readthedocs.io/en/latest/)
* [Alembic](https://alembic.sqlalchemy.org/en/latest/)
* [SQLite](https://www.sqlite.org/)
* [Uvicorn](https://www.uvicorn.org/)

## Как развернуть проект
1. Клонируйте репозиторий и перейдите в директорию QRkot_spreadsheets
```bash
git git@github.com:igorKolomitseff/QRkot_spreadsheets.git
cd QRkot_spreadsheets
```

2. Создайте виртуальное окружение и активируйте его:
```bash
python3 -m venv venv
source venv/bin/activate  # Для Linux и macOS
source venv/Scripts/activate  # Для Windows
```

3. Обновите pip и установите зависимости проекта:
```bash
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```
4. Создайте .env файл в корневой директории и заполните его данными в 
соответствии с файлом .env.example

5. Создайте файл базы данных и примените миграции командой:
```bash
alembic upgrade head
```

6. Запустите проект:
```bash
uvicorn app.main:app
```

Откройте браузер и перейдите по адресу 
[http://127.0.0.1:8000/](http://127.0.0.1:8000/) для доступа главной странице 
проекта

## Документация API

Техническая документация к API доступна при запущенном проекте по ссылкам:

* [Swagger](http://127.0.0.1:8000/docs)
* [ReDoc](http://127.0.0.1:8000/redoc)

Документация без развёртывания проекта:

[Техническая документация к API](https://github.com/igorKolomitseff/QRkot_spreadsheets/blob/main/openapi.json)

### Автор

[Игорь Коломыцев](https://github.com/igorKolomitseff)