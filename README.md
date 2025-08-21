# Тестовое задание

## Для запуска приложения:

1. Для создания контейнера введите команду ``docker compose build``
2. Для запуска контейнера введите команду ``docker compose up``

## Для запуска тестов:

> Чтобы запустить тесты пропишите команду `pytest`

## Для просмотра документации перейдите http://localhost:8000/docs#/

## Для проверки эндпоинтов:

1. Вызовите метод POST "/tasks/" и передайте в него данные заметки
   <br>Curl:

> curl -X 'POST' \
'http://localhost:8000/tasks/' \
> -H 'accept: application/json' \
> -H 'Content-Type: application/json' \
> -d '{
"title": "string",
"description": "string",
"status": "Создано"
> }'
>
<br>Формат тела JSON:
> {
"title": "string",
"description": "string",
"status": "Создано"
> }
>

2. Вызовите метод GET "tasks/?status=?&skip=?&limit=?" для просмотра добавленных задач (заполните вопросительные знаки
   на нужные параметы)
   <br>Curl:

> curl -X 'GET' \
'http://localhost:8000/tasks/?status=%D0%A1%D0%BE%D0%B7%D0%B4%D0%B0%D0%BD%D0%BE&skip=0&limit=100' \
> -H 'accept: application/json'
>
>

3. Вызовите метод GET "tasks/?status=?&skip=?&limit=?" для просмотра добавленных задач (заполните вопросительные знаки
   на нужные параметы)
   <br>Curl:

> curl -X 'GET' \
'http://localhost:8000/tasks/a1015552-330a-4af0-bfdc-5d9488cdf73b' \
> -H 'accept: application/json'
>

4. Вызовите метод PUT "/tasks/{id}" для редактирования задачи по его id
   <br>Curl:

> curl -X 'PUT' \
'http://localhost:8000/tasks/a1015552-330a-4af0-bfdc-5d9488cdf73b' \
> -H 'accept: application/json' \
> -H 'Content-Type: application/json' \
> -d '{
"title": "string",
"description": "string",
"status": "Создано"
> }'
>
<br>Формат тела JSON:
> {
"title": "string",
"description": "string",
"status": "Создано"
> }
>

5. Вызовите метод DELETE "/tasks/{id}" для удаления задачи
   <br>Curl:

> curl -X 'DELETE' \
'http://localhost:8000/tasks/a1015552-330a-4af0-bfdc-5d9488cdf73b' \
> -H 'accept: application/json'
>
