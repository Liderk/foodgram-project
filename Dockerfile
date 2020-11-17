FROM python:3.8-alpine
LABEL author='vismoke@yandex.ru' version=1.0 project='foodgram'
WORKDIR /code
COPY requirements.txt .
# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev jpeg-dev zlib-dev libjpeg wkhtmltopdf xvfb msttcorefonts-installer fontconfig ttf-dejavu font-cronyx-cyrillic \
                  && fc-cache -f \
                  && pip install --upgrade pip \
                  && pip install -r requirements.txt \
                  && rm -rf .cache/pip
COPY . /code
RUN export SECRET_KEY=test_SECRET_KEY && python manage.py collectstatic --noinput