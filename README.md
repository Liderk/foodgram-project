![foodgram workflow](https://github.com/Liderk/foodgram-project/workflows/foodgram%20workflow/badge.svg)
# foodgram-project


## Описание
Онлайн-сервис, где пользователи могут сохранять и публиковать свои рецепты, 
подписываться на публикации других пользователей, добавлять 
понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать
сводный список продуктов, необходимых для приготовления одного или нескольких 
выбранных блюд

Cоздан в качестве дипломного проекта учебного курса Яндекс.Практикум.

## Стек технологий
- проект написан на Python с использованием веб-фреймворка Django.
- работа с изображениями - pillow
- деплой на сервере - nginx, ginicorn
- база данны PostgreSQL
- автоматическое развертывание проекта - Docker, docker-compose
- система управления версиями - git

## Установка и запуск

Для работы требуется **Docker** и **Docker-compose**

Клонируйте репозиторий. В директории с manage.py создайте файл .env со следующим
содержимым:

```  
DB_ENGINE=django.db.backends.postgresql
DB_NAME=(укажите название вашей БД, для подключения django)
POSTGRES_USER=(укажите имя пользователя вашей БД)
POSTGRES_PASSWORD=(укажите пароль к БД)
POSTGRES_DB=(укажите название вашей БД, для создания ее в PosgresQl
 в случае запуска проекта через контейнеры докера)
DB_HOST=db
DB_PORT=5432
SECRET_KEY=(укажите свой ключ)
```
Для локального запуска в контейнерах, измените строчку **image: liderk/foodgram_final:latest**

в docker-compose.yaml на  **build: .**

Для создания суперпользователя, выполните в командной строке:
```  
sudo docker exec -it app_web_1 sh
```
Далее создайте суперпользователя:
``` 
python manage.py createsuperuser
``` 