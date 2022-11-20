# QRkot_spreadsheets
___
Приложение для Благотворительного фонда поддержки котиков QRKot.
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
___
## Технологии
    Python v3.10
    Fastapi v0.78
    Fastapi-users[sqlalchemy] v10.0.4
    Sqlalchemy v1.4.36
    Uvicorn[standard] v0.17.6
    Aiogoogle v4.2.0
___
## Описание

Благотворительные проекты
В Фонде QRKot может быть открыто несколько целевых проектов. У каждого проекта есть название, описание и сумма, которую планируется собрать. После того, как нужная сумма собрана — проект закрывается.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

Пожертвования
Каждый пользователь может сделать пожертвование и сопроводить его комментарием. Пожертвования не целевые: они вносятся в фонд, а не в конкретный проект. Каждое полученное пожертвование автоматически добавляется в первый открытый проект, который ещё не набрал нужную сумму. Если пожертвование больше нужной суммы или же в Фонде нет открытых проектов — оставшиеся деньги ждут открытия следующего проекта. При создании нового проекта все неинвестированные пожертвования автоматически вкладываются в новый проект.

Отчет
В приложение QRKot добавлена возможность формирования отчёта в гугл-таблице. В таблице указаны закрытые проекты, отсортированные по скорости сбора средств — от тех, что закрылись быстрее всего, до тех, что долго собирали нужную сумму.


## Как запустить проект:

Клонируйте репозиторий и перейдите в корневую папку проекта:

    git clone https://github.com/okairon/cat_charity_fund
    cd cat_charity_fund

Создайте и активируйте виртуальное окружение:

    python3 -m venv env
    source venv/bin/activate

Обновите pip и установите зависимости в виртуальное окружение:

    python -m pip install --upgrade pip
    pip install -r requirements.txt

Запустите проект:

    uvicorn app.main:app --reload

Создайте и примените миграции alembic:

    alembic revision --autogenerate -m "Название миграции"
    alembic upgrade head / +1 

Для отправки тестовых запросов в swagger перейдите по адресу:
http://127.0.0.1:8000/docs

Так же к проекту прилагается документация в файле openapi.json.
Для просмотра документации достаточно загрузить её по адресу:
https://redocly.github.io/redoc/

### Лицензия
MIT License

Copyright (c) 2022 okairon

[![Build and Test](https://github.com/okairon/QRkot_spreadsheets/actions/workflows/main.yml/badge.svg)](https://github.com/okairon/QRkot_spreadsheets/actions/workflows/main.yml)
