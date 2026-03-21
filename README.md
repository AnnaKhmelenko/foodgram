# Foodgram

## Описание проекта

Foodgram — сервис для публикации и хранения рецептов.

Пользователи могут:
- публиковать рецепты;
- добавлять рецепты в избранное;
- подписываться на авторов;
- формировать список покупок;
- скачивать список ингредиентов в текстовом формате.

## Развертывание проекта с Docker

Перед началом работы убедитесь, что Docker установлен и запущен:

```bash
sudo systemctl status docker

## Установка Docker

```bash
sudo apt update
sudo apt install curl
curl -fsSL https://get.docker.com -o install-docker.sh
sudo apt install docker-compose-plugin
sudo systemctl status docker

## Запуск проекта

Создайте рабочую директорию и перейдите в нее:

```bash
mkdir foodgram
cd foodgram

Склонируйте репозитеорий и перейдите в папку infra:

```bash
git clone https://github.com/AnnaHmelenko/foodgram.git
cd foodgram/infra

Запустите контейнеры: 

```bash
sudo docker compose up -d
```

## Настройка переменных окружения
Создайте файл .env  в папке infra на основе примера:

```bash
cp .env.example .env
```

## Первоначальная настройка
Выполните миграции и соберите статические файлы:

```bash
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py collectstatic --noinput
```

## Загрузка ингридиентов
Для загрузки ингридиентов выполните команду:

```bash
sudo docker compose exec backend python manage.py load_ingredients
```

## Доступ к проекту

Проект доступен по следующим адресам:

http://localhost
http://127.0.0.1

## Ссылка на развернутый проект
https://embassy-minority-band-acquisition.trycloudflare.com

## Остановка проекта

Для остановки контейнеров выполните команду:
sudo docker compose down

## Используемые технологии
- Python
- Django
- Django REST Framework
- React
- PostgreSQL
- Docker
- Nginx
- Gunicorn

## Автор

Анна Хмеленко
https://github.com/AnnaHmelenko/foodgram
