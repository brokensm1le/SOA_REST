# SOA_REST


Это приложение-RESTсервис, который предоставляет возможность добавления, просмотра, редактирования и удаления следующей информации по профилю игрока.
+
Генерация статистики игрока в виде ``PDF``-файла.

## Интерфейс

- Запрос ``GET``(всего списка): получение информации об всех игроках;
- Запрос ``GET``(отдельного игрока): получение информации об одном игроке(по его ``nickname``);
- Запрос ``POST``: добавление информации об игроке;
- Запрос ``PUT``: обновление информации об игроке;
- Запрос ``DELETE``: удаление информации об игроке.

Хранение данных производится в файле ``todo.db``, представляющем собой базу данных SQLite3.


## Подготовка и настройка
### Подготовка
Перед запуском системы, необходимо:
- Установить [python3](https://www.python.org/download/releases/3.0/)
- При использовании Visual Studio Code, можно подготовить среду для разработки посредством материалов туториола: https://code.visualstudio.com/docs/python/tutorial-flask

### Запуск приложения
В корневой директории выполнить 
- ``pip install virtualenv``
- ``python -m venv flask-todo``
- ``virtualenv flask-todo``
- ``python -m pip install flask``
- ``python -m flask run``

### Работа с сервисом
Для отправки запросов можно использовать утилиту ``curl`` или ``postman``. Пример запросов (при условии, что сервер развернут по адресу ``http://127.0.0.1:5000``):
- получение информации об всех игроках: ``curl --location --request GET 'http://127.0.0.1:5000/todoapp/api/v1.0/todos'``
- получение информации об одном игроке: ``curl --location --request GET 'http://127.0.0.1:5000/todoapp/api/v1.0/todos'``
- добавление информации об игроке: ``curl --location --request POST 'http://127.0.0.1:5000/todoapp/api/v1.0/todos' --header 'Content-Type: application/json' --data-raw '{"description": "To test POST"}'``
- обновление информации об игроке: ``curl --location --request PUT 'http://127.0.0.1:5000/todoapp/api/v1.0/todos/3' --header 'Content-Type: application/json' --data-raw '{ "description": "To test POST", "status": "Started","uri": "http://127.0.0.1:5000/todoapp/api/v1.0/todos/3"}'``
- удаление информации об игроке: ``curl --location --request DELETE 'http://127.0.0.1:5000/todoapp/api/v1.0/todos/3'``

