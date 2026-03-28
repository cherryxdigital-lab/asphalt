from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
import re
from .models import (
    EquipmentRental,
    AsphaltType,
    ContactRequest,
    BlogPost,
    CompanyInfo,
    WorkProcessStep,
    EvacuatorSection,
    EvacuatorOffer,
)
from django.db.utils import OperationalError

# Create your views here.

NAME_RE = re.compile(r"^[A-Za-zА-Яа-яІіЇїЄєҐґ'\-\s]+$")
PHONE_DIGITS_RE = re.compile(r"\D")


def format_ukrainian_phone(phone: str) -> str:
    digits = PHONE_DIGITS_RE.sub('', phone)
    if digits.startswith('380'):
        digits = digits[:12]
    elif digits.startswith('80'):
        digits = f"3{digits[:11]}"
    elif digits.startswith('0'):
        digits = f"38{digits[:10]}"
    else:
        digits = digits[:12]

    if len(digits) != 12 or not digits.startswith('380'):
        return ''

    return f'+{digits[:3]} ({digits[3:5]}) {digits[5:8]}-{digits[8:10]}-{digits[10:12]}'

def home(request):
    if request.method == 'POST':
        name = (request.POST.get('name') or '').strip()
        phone = (request.POST.get('phone') or '').strip()
        email = (request.POST.get('email') or '').strip()
        message = (request.POST.get('message') or '').strip()
        is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'

        if not name or not phone:
            error_message = 'Будь ласка, заповніть ім’я та телефон.'
            if is_ajax:
                return JsonResponse({'ok': False, 'message': error_message}, status=400)
            messages.error(request, error_message)
            return redirect('home')

        normalized_name = re.sub(r'\s+', ' ', name)
        formatted_phone = format_ukrainian_phone(phone)

        if len(normalized_name) < 2 or not NAME_RE.fullmatch(normalized_name):
            error_message = 'Ім’я може містити лише літери, пробіли, апостроф та дефіс.'
            if is_ajax:
                return JsonResponse({'ok': False, 'message': error_message}, status=400)
            messages.error(request, error_message)
            return redirect('home')

        if not formatted_phone:
            error_message = 'Вкажіть коректний номер у форматі +380 (XX) XXX-XX-XX.'
            if is_ajax:
                return JsonResponse({'ok': False, 'message': error_message}, status=400)
            messages.error(request, error_message)
            return redirect('home')

        if len(message) < 10:
            error_message = 'Опишіть задачу щонайменше 10 символами.'
            if is_ajax:
                return JsonResponse({'ok': False, 'message': error_message}, status=400)
            messages.error(request, error_message)
            return redirect('home')

        ContactRequest.objects.create(
            name=normalized_name,
            phone=formatted_phone,
            email=email or None,
            message=message or None,
        )
        success_message = 'Заявку відправлено. Ми зв’яжемося з вами найближчим часом.'
        if is_ajax:
            return JsonResponse({'ok': True, 'message': success_message})

        messages.success(request, success_message)
        return redirect('home')

    equipment = EquipmentRental.objects.all()
    asphalt_types = AsphaltType.objects.all()
    blog_posts = BlogPost.objects.all()[:3]  # Показать последние 3 поста
    process_steps = WorkProcessStep.objects.all()
    evacuator_section = EvacuatorSection.objects.filter(show_on_site=True).order_by('-updated_at').first()
    evacuator_offers = EvacuatorOffer.objects.filter(show_on_site=True)
    try:
        company = CompanyInfo.objects.filter(show_on_site=True).order_by('-updated_at').first()
    except OperationalError:
        company = None
    context = {
        'equipment': equipment,
        'asphalt_types': asphalt_types,
        'blog_posts': blog_posts,
        'process_steps': process_steps,
        'evacuator_section': evacuator_section,
        'evacuator_offers': evacuator_offers,
        'company': company,
    }
    return render(request, 'landing/home.html', context)

def blog_list(request):
    blog_posts = BlogPost.objects.all()
    try:
        company = CompanyInfo.objects.filter(show_on_site=True).order_by('-updated_at').first()
    except OperationalError:
        company = None
    context = {
        'blog_posts': blog_posts,
        'company': company,
    }
    return render(request, 'landing/blog_list.html', context)

def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    try:
        company = CompanyInfo.objects.filter(show_on_site=True).order_by('-updated_at').first()
    except OperationalError:
        company = None
    context = {
        'post': post,
        'company': company,
    }
    return render(request, 'landing/blog_detail.html', context)
