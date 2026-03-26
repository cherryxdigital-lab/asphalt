# Asphalt

Веб-проект на Django для компании по асфальтированию и дорожным работам.

Сайт включает:

- лендинг с описанием услуг;
- блок с видами асфальта и ценами;
- блок с арендой техники;
- форму заявок с валидацией данных;
- уведомления о новых заявках в Telegram;
- блог со списком статей и отдельными страницами материалов;
- админ-панель Django для управления контентом.

## Стек

- Python 3.11+
- Django 5
- SQLite
- Pillow
- python-telegram-bot
- requests
- python-dotenv

## Структура проекта

- `asphalt_project/` - настройки Django, маршруты, WSGI/ASGI
- `landing/` - основное приложение сайта
- `landing/templates/landing/` - HTML-шаблоны
- `landing/static/` - CSS, JS, изображения
- `media/` - загружаемые файлы
- `requirements.txt` - зависимости проекта

## Что умеет проект

### Главная страница

На главной странице выводятся:

- список техники в аренду;
- типы асфальта;
- этапы процесса работ;
- последние статьи блога;
- контактная информация компании.

### Заявки с сайта

Форма на главной странице:

- проверяет имя и номер телефона;
- сохраняет заявку в базу;
- умеет отвечать через обычный POST и AJAX;
- отправляет уведомление в Telegram после создания заявки.

### Блог

Реализованы:

- страница списка статей;
- страница отдельной статьи по `slug`.

## Запуск локально

### 1. Клонирование

```bash
git clone https://github.com/cherryxdigital-lab/asphalt.git
cd asphalt
```

### 2. Виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установка зависимостей

```bash
pip install -r requirements.txt
```

### 4. Переменные окружения

Создайте `.env` на основе шаблона:

```bash
cp .env.example .env
```

Заполните значения:

- `TELEGRAM_BOT_TOKEN`
- `TELEGRAM_ADMIN_CHAT_ID`
- `TELEGRAM_SITE_URL`

Если Telegram пока не нужен, можно оставить эти значения пустыми.

### 5. Миграции

```bash
python manage.py migrate
```

### 6. Создание администратора

```bash
python manage.py createsuperuser
```

### 7. Запуск сервера

```bash
python manage.py runserver
```

После запуска сайт будет доступен по адресу `http://127.0.0.1:8000/`.

## Наполнение тестовыми данными

В проекте есть management command для заполнения базы стартовыми данными:

```bash
python manage.py populate_data
```

## Админка

Админ-панель доступна по адресу:

```text
http://127.0.0.1:8000/admin/
```

Через админку можно управлять:

- видами асфальта;
- техникой;
- заявками;
- статьями блога;
- информацией о компании;
- этапами работ.

## Что важно не коммитить

В репозиторий не стоит отправлять:

- `.env`
- `venv/`
- `db.sqlite3`
- `media/`
- `__pycache__/`

Для этого в проект добавлен `.gitignore`.

## Команды для первой загрузки в GitHub

Если репозиторий ещё не инициализирован локально:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/cherryxdigital-lab/asphalt.git
git push -u origin main
```

Если после этого будете отправлять обновления:

```bash
git add .
git commit -m "Update project"
git push
```
