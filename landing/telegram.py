import html
import os
import requests
from django.conf import settings
from django.urls import reverse

BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN') or getattr(settings, 'TELEGRAM_BOT_TOKEN', None)
ADMIN_CHAT_ID = os.getenv('TELEGRAM_ADMIN_CHAT_ID') or getattr(settings, 'TELEGRAM_ADMIN_CHAT_ID', None)
SITE_URL = (os.getenv('TELEGRAM_SITE_URL') or getattr(settings, 'TELEGRAM_SITE_URL', '')).rstrip('/')
BASE_API = f'https://api.telegram.org/bot{BOT_TOKEN}' if BOT_TOKEN else None

from .models import ContactRequest


def build_request_message(req: ContactRequest):
    parts = [f"Нова заявка #{req.id}"]
    parts.append(f"Ім'я: {html.escape(req.name)}")
    parts.append(f"Телефон: {html.escape(req.phone)}")
    if req.email:
        parts.append(f"Email: {html.escape(req.email)}")
    if req.message:
        parts.append(f"Повідомлення:\n{html.escape(req.message)}")
    parts.append(f"Створено: {req.created_at.strftime('%Y-%m-%d %H:%M')}")
    return "\n".join(parts)


def send_new_request_notification(request_id: int):
    if not BASE_API or not ADMIN_CHAT_ID:
        return False
    try:
        req = ContactRequest.objects.get(pk=request_id)
    except ContactRequest.DoesNotExist:
        return False

    text = build_request_message(req)

    # Inline keyboard: Call (url tel:), Mark processed (callback), View in admin (url)
    admin_url = ''
    try:
        admin_path = reverse('admin:landing_contactrequest_change', args=[req.id])
        if SITE_URL:
            admin_url = f'{SITE_URL}{admin_path}'
    except Exception:
        admin_url = ''

    keyboard = {
        'inline_keyboard': [
            [
                {'text': '📞 Показати номер', 'callback_data': f'phone:{req.id}'},
                {'text': '✅ Помітити обробленою', 'callback_data': f'mark:{req.id}'}
            ],
            [
                {'text': '🔎 Показати не оброблені', 'callback_data': 'list:unprocessed'}
            ]
        ]
    }

    if admin_url:
        keyboard['inline_keyboard'][0].append({'text': '🛠 В адмінці', 'url': admin_url})

    resp = requests.post(
        f"{BASE_API}/sendMessage",
        json={
            'chat_id': ADMIN_CHAT_ID,
            'text': text,
            'reply_markup': keyboard,
            'parse_mode': 'HTML',
        },
        timeout=10,
    )
    return resp.status_code == 200
