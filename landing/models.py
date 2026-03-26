from io import BytesIO
from pathlib import Path

from django.db import models
from django.core.files.base import ContentFile
from django.utils.text import slugify
from django.urls import reverse
from PIL import Image

# Create your models here.


def convert_image_to_webp(field_file, quality: int = 86):
    if not field_file:
        return None

    image = Image.open(field_file)
    if image.mode not in ('RGB', 'RGBA'):
        image = image.convert('RGB')

    if image.mode == 'RGBA':
        background = Image.new('RGBA', image.size, (255, 255, 255, 255))
        background.alpha_composite(image)
        image = background.convert('RGB')

    output = BytesIO()
    image.save(output, format='WEBP', quality=quality, method=6)
    output.seek(0)

    file_name = f"{Path(field_file.name).stem}.webp"
    return file_name, ContentFile(output.read())

class EquipmentRental(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва техніки")
    description = models.TextField(verbose_name="Опис")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна (грн)")
    price_unit = models.CharField(max_length=100, verbose_name="Одиниця вимірювання (година/зміна/кв.м і т.д.)")
    min_hours = models.PositiveIntegerField(blank=True, null=True, verbose_name="Мінімум годин")
    image = models.ImageField(upload_to='equipment/', blank=True, null=True, verbose_name="Зображення")
    image_url = models.URLField(blank=True, null=True, verbose_name="Посилання на зображення (якщо немає файлу)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Оренда техніки"
        verbose_name_plural = "Оренда техніки"


class AsphaltType(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва асфальту")
    description = models.TextField(verbose_name="Опис")
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Ціна за кв.м (грн)")
    image = models.ImageField(upload_to='asphalt/', blank=True, null=True, verbose_name="Зображення")
    image_url = models.URLField(blank=True, null=True, verbose_name="Посилання на зображення (якщо немає файлу)")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Тип асфальту"
        verbose_name_plural = "Типи асфальту"


class ContactRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Ім'я")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    message = models.TextField(blank=True, null=True, verbose_name="Повідомлення")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    processed = models.BooleanField(default=False, verbose_name="Оброблено")

    def __str__(self):
        return f"Заявка від {self.name} ({self.phone})"

    class Meta:
        verbose_name = "Заявка"
        verbose_name_plural = "Заявки"


class BlogPost(models.Model):
    title = models.CharField(max_length=200, verbose_name="Назва статті")
    slug = models.SlugField(unique=True, blank=True, verbose_name="Слаг")
    short_description = models.TextField(verbose_name="Короткий опис")
    full_description = models.TextField(verbose_name="Повний опис")
    image = models.ImageField(upload_to='blog/', blank=True, null=True, verbose_name="Зображення")
    image_url = models.URLField(blank=True, null=True, verbose_name="Посилання на зображення (якщо немає файлу)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Стаття блогу"
        verbose_name_plural = "Статті блогу"
        ordering = ['-created_at']


class CompanyInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name="Назва компанії", default="ROADTECH")
    address = models.CharField(max_length=400, verbose_name="Адреса", blank=True)
    phone_primary = models.CharField(max_length=30, verbose_name="Телефон 1", blank=True)
    phone_secondary = models.CharField(max_length=30, verbose_name="Телефон 2", blank=True)
    working_hours = models.CharField(max_length=200, verbose_name="Графік роботи", blank=True,
                                     help_text="Наприклад: Пн-Пт 08:00-18:00; Сб 09:00-13:00")
    show_on_site = models.BooleanField(default=True, verbose_name="Показувати на сайті")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Оновлено")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Інформація про компанію"
        verbose_name_plural = "Інформація про компанію"


class WorkProcessStep(models.Model):
    title = models.CharField(max_length=200, verbose_name="Заголовок кроку")
    short_description = models.CharField(max_length=255, verbose_name="Короткий опис")
    full_description = models.TextField(verbose_name="Розгорнутий опис")
    image = models.ImageField(upload_to='process_steps/', blank=True, null=True, verbose_name="Зображення")
    image_url = models.URLField(blank=True, null=True, verbose_name="Посилання на зображення")
    image_alt = models.CharField(max_length=255, blank=True, verbose_name="Alt для SEO")
    order = models.PositiveIntegerField(default=0, verbose_name="Порядок")
    featured = models.BooleanField(default=False, verbose_name="Виділений крок")

    def save(self, *args, **kwargs):
        if self.image and not self.image.name.lower().endswith('.webp'):
            converted = convert_image_to_webp(self.image)
            if converted:
                file_name, content = converted
                self.image.save(file_name, content, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Крок процесу"
        verbose_name_plural = "Кроки процесу"
        ordering = ['order', 'id']
