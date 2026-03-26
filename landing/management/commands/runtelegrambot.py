from django.core.management.base import BaseCommand
from django.conf import settings
from asgiref.sync import sync_to_async
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
from landing.models import ContactRequest
from landing.telegram import build_request_message


MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton('Старт'), KeyboardButton('Необроблені')],
        [KeyboardButton('Усі заявки'), KeyboardButton('Остання заявка')],
        [KeyboardButton('Допомога')],
    ],
    resize_keyboard=True,
    is_persistent=True,
)

PAGE_SIZE = 20


def get_token():
    return settings.TELEGRAM_BOT_TOKEN


def get_admin_chat():
    return str(settings.TELEGRAM_ADMIN_CHAT_ID or '').strip()


async def ensure_admin_chat(update: Update):
    admin_chat = get_admin_chat()
    current_chat = str(update.effective_chat.id) if update.effective_chat else ''
    if admin_chat and current_chat != admin_chat:
        if update.effective_message:
            await update.effective_message.reply_text('Цей бот доступний лише для адміністратора.')
        return False
    return True


@sync_to_async
def fetch_requests_page(page: int, processed=None):
    qs = ContactRequest.objects.order_by('-created_at')
    if processed is not None:
        qs = qs.filter(processed=processed)

    total = qs.count()
    offset = max(page, 0) * PAGE_SIZE
    requests = list(qs[offset:offset + PAGE_SIZE])
    return total, requests


@sync_to_async
def mark_request_processed(request_id: int):
    try:
        request = ContactRequest.objects.get(pk=request_id)
    except ContactRequest.DoesNotExist:
        return False

    request.processed = True
    request.save(update_fields=['processed'])
    return True


@sync_to_async
def get_request_details(request_id: int):
    try:
        request = ContactRequest.objects.get(pk=request_id)
    except ContactRequest.DoesNotExist:
        return None
    return {
        'id': request.id,
        'name': request.name,
        'phone': request.phone,
        'message': build_request_message(request),
    }


@sync_to_async
def get_latest_request():
    request = ContactRequest.objects.order_by('-created_at').first()
    if not request:
        return None
    return {
        'id': request.id,
        'name': request.name,
        'phone': request.phone,
        'created_at': request.created_at.strftime('%Y-%m-%d %H:%M'),
        'processed': request.processed,
    }


def build_request_actions(request_id: int):
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton('📞 Контакт', callback_data=f'phone:{request_id}'),
            InlineKeyboardButton('🧾 Деталі', callback_data=f'details:{request_id}'),
        ],
        [
            InlineKeyboardButton('✅ Помітити', callback_data=f'mark:{request_id}'),
        ],
    ])


def build_pagination_markup(kind: str, page: int, total: int):
    total_pages = max((total + PAGE_SIZE - 1) // PAGE_SIZE, 1)
    buttons = []

    if page > 0:
        buttons.append(InlineKeyboardButton('⬅️ Назад', callback_data=f'page:{kind}:{page - 1}'))
    if page + 1 < total_pages:
        buttons.append(InlineKeyboardButton('➡️ Далі', callback_data=f'page:{kind}:{page + 1}'))

    if not buttons:
        return None
    return InlineKeyboardMarkup([buttons])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_admin_chat(update):
        return
    await update.effective_message.reply_text(
        'Бот запущений.\n'
        'Постійне меню вже внизу.\n'
        'Команди:\n'
        '/start - головне меню\n'
        '/list - показати необроблені заявки\n'
        '/help - підказка',
        reply_markup=MAIN_KEYBOARD,
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_admin_chat(update):
        return
    await update.effective_message.reply_text(
        'Доступні дії:\n'
        'Старт - показати головне меню\n'
        'Необроблені - список активних заявок\n'
        'Усі заявки - повний список з пагінацією\n'
        'Остання заявка - показати найновішу заявку\n'
        'Допомога - ця підказка\n'
        'У списку заявок є кнопки Контакт, Деталі та Помітити.',
        reply_markup=MAIN_KEYBOARD,
    )


async def latest_request(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_admin_chat(update):
        return
    request = await get_latest_request()
    if not request:
        await update.effective_chat.send_message('Заявок поки немає', reply_markup=MAIN_KEYBOARD)
        return

    status = '✅ Оброблена' if request['processed'] else '🟡 Необроблена'
    text = (
        f"Остання заявка #{request['id']}\n"
        f"Ім'я: {request['name']}\n"
        f"Телефон: {request['phone']}\n"
        f"Створено: {request['created_at']}\n"
        f"Статус: {status}"
    )
    await update.effective_chat.send_message(
        text,
        reply_markup=build_request_actions(request['id']),
    )


async def list_unprocessed(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_admin_chat(update):
        return
    await show_requests_page(update.effective_chat, 0, 'unprocessed')


async def show_requests_page(chat, page: int, kind: str):
    processed = None if kind == 'all' else False
    page = max(page, 0)
    total, requests = await fetch_requests_page(page, processed=processed)

    if not requests:
        text = 'Заявок поки немає' if kind == 'all' else 'Немає необроблених заявок'
        await chat.send_message(text, reply_markup=MAIN_KEYBOARD)
        return

    total_pages = max((total + PAGE_SIZE - 1) // PAGE_SIZE, 1)
    safe_page = min(page, total_pages - 1)
    if safe_page != page:
        total, requests = await fetch_requests_page(safe_page, processed=processed)
    current_page = safe_page + 1
    title = 'Усі заявки' if kind == 'all' else 'Необроблені заявки'
    summary = f'{title}\nСторінка {current_page} з {total_pages}\nВсього заявок: {total}'
    pagination_markup = build_pagination_markup(kind, safe_page, total)

    await chat.send_message(summary, reply_markup=pagination_markup or MAIN_KEYBOARD)

    for r in requests:
        status = '✅ Оброблена' if r.processed else '🟡 Необроблена'
        text = f"#{r.id} {r.name} — {r.phone} ({r.created_at.strftime('%Y-%m-%d %H:%M')})\nСтатус: {status}"
        await chat.send_message(text, reply_markup=build_request_actions(r.id))

    if pagination_markup:
        await chat.send_message(
            f'Навігація по сторінках: {current_page}/{total_pages}',
            reply_markup=pagination_markup,
        )


async def all_requests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_admin_chat(update):
        return
    await show_requests_page(update.effective_chat, 0, 'all')


async def menu_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_admin_chat(update):
        return

    text = (update.effective_message.text or '').strip().lower()
    if text == 'старт':
        await start(update, context)
    elif text == 'необроблені':
        await list_unprocessed(update, context)
    elif text == 'усі заявки':
        await all_requests(update, context)
    elif text == 'остання заявка':
        await latest_request(update, context)
    elif text == 'допомога':
        await help_command(update, context)


async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await ensure_admin_chat(update):
        return

    query = update.callback_query
    data = query.data or ''
    if data.startswith('mark:'):
        rid = int(data.split(':', 1)[1])
        try:
            updated = await mark_request_processed(rid)
            if updated:
                await query.answer('Заявку оновлено')
                await query.edit_message_text(f'Заявка #{rid} позначена як оброблена ✅')
            else:
                await query.answer('Заявка не знайдена', show_alert=True)
                await query.edit_message_text('Заявка не знайдена')
        except Exception:
            await query.answer('Помилка оновлення', show_alert=True)
            await query.edit_message_text('Не вдалося оновити заявку')
    elif data.startswith('phone:'):
        rid = int(data.split(':', 1)[1])
        details = await get_request_details(rid)
        if details:
            await update.effective_chat.send_contact(
                phone_number=details['phone'],
                first_name=details['name'],
            )
            await query.answer('Контакт відправлено')
        else:
            await query.answer('Контакт не знайдено', show_alert=True)
    elif data.startswith('details:'):
        rid = int(data.split(':', 1)[1])
        details = await get_request_details(rid)
        if details:
            await update.effective_chat.send_message(
                details['message'],
                reply_markup=build_request_actions(rid),
            )
            await query.answer('Деталі відправлено')
        else:
            await query.answer('Заявку не знайдено', show_alert=True)
    elif data.startswith('page:'):
        try:
            _, kind, page_str = data.split(':', 2)
            if kind not in {'all', 'unprocessed'}:
                raise ValueError('invalid kind')
            page = int(page_str)
        except (ValueError, TypeError):
            await query.answer('Некоректна сторінка', show_alert=True)
            return
        await query.answer('Завантажую сторінку')
        await show_requests_page(update.effective_chat, page, kind)
    elif data.startswith('list:'):
        await query.answer('Показую список')
        await show_requests_page(update.effective_chat, 0, 'unprocessed')


class Command(BaseCommand):
    help = 'Запускає Telegram бота (polling) для обробки callback кнопок'

    def handle(self, *args, **options):
        token = get_token()
        if not token:
            self.stdout.write(self.style.ERROR('TELEGRAM_BOT_TOKEN не налаштовано в settings.'))
            return
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(CommandHandler('list', list_unprocessed))
        app.add_handler(CommandHandler('all', all_requests))
        app.add_handler(CommandHandler('help', help_command))
        app.add_handler(CallbackQueryHandler(callback_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_message_handler))

        self.stdout.write(self.style.SUCCESS('Запускаю Telegram bot (polling)...'))
        app.run_polling()
