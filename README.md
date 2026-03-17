# Foodgram

## Описание проекта

**Foodgram** — сервис для публикации и хранения рецептов.

Пользователи могут:
- публиковать рецепты;
- добавлять их в избранное;
- подписываться на авторов;
- формировать список покупок;
- скачивать список ингредиентов в текстовом формате.


## Развертывание проекта с Docker

Перед началом убедитесь, что Docker установлен и запущен:

```bash
sudo systemctl status docker
```

### Установка Docker

```bash
sudo apt update
sudo apt install curl

curl -fsSL https://get.docker.com -o install-docker.sh

sudo apt install docker-compose-plugin

sudo systemctl status docker
```


## Запуск проекта

```bash
mkdir foodgram
cd foodgram
```

Склонируйте репозиторий:

```bash
git clone https://github.com/AnnaHmelenko/foodgram.git
cd foodgram/infra
```

Запустите контейнеры:

```bash
sudo docker compose up -d
```


## Настройка переменных окружения

Создайте файл `.env` в папке `infra`:

```bash
cp .env.example .env
```


## 🛠 Первоначальная настройка

```bash
sudo docker compose exec backend python manage.py migrate
sudo docker compose exec backend python manage.py collectstatic --noinput
```


## Загрузка ингредиентов

```bash
sudo docker compose exec backend python manage.py load_ingredients
```


## Доступ к проекту

- http://localhost
- http://127.0.0.1


## Ссылка на развернутый проект

http://<ВАШ_IP_ИЛИ_ДОМЕН>


## Остановка проекта

```bash
sudo docker compose down
```


## Используемые технологии

- Python
- Django
- Django REST Framework
- React
- PostgreSQL / SQLite
- Docker
- Nginx
- Gunicorn


## Автор

Анна Хмеленко  
https://github.com/AnnaHmelenko/foodgram
