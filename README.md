# Дипломный проект FOODGRAM

Доступен по адресу: <http://51.250.19.66/>

Доступ в админку:
    email: admin@admin.ru
    pass: admin
------

![status workflow](https://github.com/petrzakharov/foodgram-project-react/actions/workflows/backend.yml/badge.svg)

## Описание

В данном проекте реализован API функционал для проекта FOODGRAM и настроен CI/CD с помощью Github Actions.
>После того, как сделан пуш в основную ветку:

* Разворачивается окружение;
* Прогоняются тесты;
* Cобирается DOCKER образ и пушится в DockerHub;
* На удаленном сервере запускаются команды из файла docker-compose.yaml которые поднимают 3 контейнера (db, web, nginx). Эти команды описаны в файле: backend_workflow.yml.

## Перед деплоем на удаленный сервер

1. Установить Docker и Docker-compose

```sudo apt install docker.io```
2. Добавить env переменные в Github Actions

    ```python
    DB_ENGINE
    DB_HOST
    DB_NAME
    DB_PORT
    DOCKER_PASSWORD
    DOCKER_USERNAME
    HOST
    PASSPHRASE
    POSTGRES_PASSWORD
    POSTGRES_USER
    SSH_KEY
    TELEGRAM_TO
    TELEGRAM_TOKEN
    USER
    ```

3. Скопировать файлы docker-compose.yaml и nginx/default.conf из репозитория на сервер в home/<ваш_username>/docker-compose.yaml и home/<ваш_username>/nginx/default.conf

## После деплоя на сервер

1. Собрать docker-compose
```sudo docker-compose up -d --build```
2. Собрать статику
```sudo docker-compose exec backend python manage.py collectstatic --no-input```
3. Создать и применить миграции
```sudo docker-compose exec backend python manage.py makemigrations --noinput```

```sudo docker-compose exec backend python manage.py migrate --noinput```
4. Создать супер пользователя
```sudo docker-compose exec backend python manage.py createsuperuser```

## Используемая инфраструктура

1. Проект работает с СУБД PostgreSQL.
2. Проект запущен на сервере в Яндекс.Облаке в трёх Docker контейнерах: nginx, PostgreSQL и Django+Gunicorn.
3. Контейнер с проектом обновляется на Docker Hub.
4. В nginx настроена раздача статики, остальные запросы переадресуются в Gunicorn.
