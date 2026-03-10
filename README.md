# Foodgram

# Описание проекта

- Foodgram — сервис для публикации и хранения рецептов.

- Пользователи могут публиковать рецепты, добавлять их в избранное,
подписываться на авторов и формировать список покупок из выбранных
рецептов с возможностью скачать его в текстовом формате.

# Развертывание проекта Foodgram с использованием Docker
# Детали:
- Перед началом работы убедитесь, что Docker установлен и запущен:

sudo systemctl status docker

- Инструкция по установке Docker:

- Обновите пакеты и установите curl:

    ~ sudo apt update
    ~ sudo apt install curl

- Загрузите официальный скрипт установки Docker:

    ~ curl -fsSL https://get.docker.com -o install-docker.sh

- Установите Docker Compose:

    ~ sudo apt install docker-compose-plugin

- Проверьте статус Docker:

    ~ sudo systemctl status docker

- Если же возникают проблемы с установкой, то обратитесь на официальный сайт Docker.

# Запуск проекта

- Создайте директорию для проекта и перейдите в неё:

    ~ mkdir foodgram
    ~ cd foodgram

- Загрузите в созданную директорию проект;

- Загрузите файл docker-compose.yml и запустите контейнеры:

    ~ sudo docker compose -f docker-compose.yml up -d

Docker автоматически загрузит образы, создаст и запустит контейнеры, объединив их в единую сеть.

# Настройка переменных окружения

- Создайте в папке infra файл .env и заполните его по примеру .env.example.

- Важно: если нет необходимости использовать PostgreSQL, то просто скопируйте содержимое файла .env.example, в проекте имеется функция, которая загрузит все необходимые таблицы в дальнейших пунктах автоматически в файл db.sqlite3 и пока проект запущен - данные будут сохраняться в данном файле, после завершения или перезапуска проекта данные будут удалены. 
В противном случае заполните правильно данные вашей БД. Не забудьте поменять значение "USE_PGSQL" на значение True.

# Первоначальная настройка

- После запуска выполните миграции и сбор статических файлов:

    ~ sudo docker compose -f docker-compose.yml exec backend python manage.py migrate

    ~ sudo docker compose -f docker-compose.yml exec backend python manage.py collectstatic

    ~ sudo docker compose -f docker-compose.yml exec backend cp -r /app/collected_static/. /backend_static/static/

- После этого проект будет доступен по адресам:

    http://localhost
    http://localhost:8080
    http://127.0.0.1
    http://127.0.0.1:8080

- P.S.: Backend будет работать на 8000 порту.

# Загрузка ингредиентов для создания рецептов

- Для корректной работы с рецептами необходимо заполнить базу данных ингредиентами:

    ~ sudo docker compose -f docker-compose.production.yml exec backend python manage.py data_loader

- Если в базе отсутствуют нужные ингредиенты или теги, обратитесь к администратору.

# Остановка проекта

- Чтобы завершить работу контейнеров, выполните:

    ~ sudo docker compose -f docker-compose.yml down

# Используемые технологии:

- Python
- Django
- Django REST Framework
- React
- PostgreSQL / SQLite
- Docker
- Nginx
- Gunicorn

# Автор выполненного проекта:

- Хмеленко А.П.
- Ссылка на репозиторий Github: https://github.com/AnnaHmelenko/foodgram