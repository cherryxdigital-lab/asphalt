from django.contrib import admin
from django.utils.html import format_html
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

@admin.register(EquipmentRental)
class EquipmentRentalAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'price_unit', 'min_hours', 'image_preview')
    list_filter = ('price_unit', 'min_hours')
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'description'),
        }),
        ('Ціна та умови', {
            'fields': ('price', 'price_unit', 'min_hours'),
        }),
        ('Зображення', {
            'fields': ('image', 'image_url', 'image_preview'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image_url)
        return "Немає зображення"
    image_preview.short_description = "Попередній перегляд"

@admin.register(AsphaltType)
class AsphaltTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'price_per_sqm', 'image_preview')
    list_filter = ('price_per_sqm',)
    search_fields = ('name', 'description')
    ordering = ('name',)
    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Основна інформація', {
            'fields': ('name', 'description'),
        }),
        ('Ціна', {
            'fields': ('price_per_sqm',),
        }),
        ('Зображення', {
            'fields': ('image', 'image_url', 'image_preview'),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image_url)
        return "Немає зображення"
    image_preview.short_description = "Попередній перегляд"

@admin.register(ContactRequest)
class ContactRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'processed', 'created_at')
    list_filter = ('processed', 'created_at',)
    search_fields = ('name', 'phone', 'email', 'message')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    fieldsets = (
        ('Контактна інформація', {
            'fields': ('name', 'phone', 'email'),
        }),
        ('Повідомлення', {
            'fields': ('message',),
        }),
        ('Статус', {
            'fields': ('processed',),
        }),
        ('Дата', {
            'fields': ('created_at',),
        }),
    )

    actions = ['mark_as_processed']

    def mark_as_processed(self, request, queryset):
        updated = queryset.update(processed=True)
        self.message_user(request, 'Заявки позначені як оброблені.')
    mark_as_processed.short_description = "Позначити як оброблені"

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'created_at', 'image_preview')
    list_filter = ('created_at',)
    search_fields = ('title', 'short_description', 'full_description')
    ordering = ('-created_at',)
    readonly_fields = ('image_preview', 'created_at')
    prepopulated_fields = {'slug': ('title',)}

    fieldsets = (
        ('Основна інформація', {
            'fields': ('title', 'slug'),
        }),
        ('Описи', {
            'fields': ('short_description', 'full_description'),
        }),
        ('Зображення', {
            'fields': ('image', 'image_url', 'image_preview'),
        }),
        ('Дата', {
            'fields': ('created_at',),
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image.url)
        elif obj.image_url:
            return format_html('<img src="{}" style="max-width: 100px; max-height: 100px;" />', obj.image_url)
        return "Немає зображення"
    image_preview.short_description = "Попередній перегляд"


@admin.register(CompanyInfo)
class CompanyInfoAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone_primary', 'phone_secondary', 'show_on_site', 'updated_at')
    list_editable = ('show_on_site',)
    readonly_fields = ('updated_at',)
    search_fields = ('name', 'address', 'phone_primary', 'phone_secondary')
    fieldsets = (
        ('Основна', {'fields': ('name', 'address', 'phone_primary', 'phone_secondary', 'working_hours', 'show_on_site')}),
        ('Системні', {'fields': ('updated_at',)}),
    )


@admin.register(WorkProcessStep)
class WorkProcessStepAdmin(admin.ModelAdmin):
    list_display = ('order', 'title', 'featured', 'image_preview')
    list_display_links = ('title',)
    list_editable = ('order', 'featured')
    ordering = ('order', 'id')
    search_fields = ('title', 'short_description', 'full_description', 'image_alt')
    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Контент', {'fields': ('title', 'short_description', 'full_description')}),
        ('Зображення', {'fields': ('image', 'image_url', 'image_alt', 'image_preview')}),
        ('Налаштування', {'fields': ('order', 'featured')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 120px; max-height: 90px; border-radius: 10px;" />', obj.image.url)
        if obj.image_url:
            return format_html('<img src="{}" style="max-width: 120px; max-height: 90px; border-radius: 10px;" />', obj.image_url)
        return "Немає зображення"
    image_preview.short_description = "Попередній перегляд"


@admin.register(EvacuatorSection)
class EvacuatorSectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'cta_text', 'show_on_site', 'updated_at')
    list_editable = ('show_on_site',)
    readonly_fields = ('updated_at',)
    search_fields = ('eyebrow', 'title', 'description', 'cta_text')
    fieldsets = (
        ('Контент секції', {'fields': ('eyebrow', 'title', 'description', 'cta_text', 'show_on_site')}),
        ('Системні', {'fields': ('updated_at',)}),
    )


@admin.register(EvacuatorOffer)
class EvacuatorOfferAdmin(admin.ModelAdmin):
    list_display = ('order', 'name', 'price_text', 'featured', 'show_on_site', 'image_preview')
    list_display_links = ('name',)
    list_editable = ('order', 'featured', 'show_on_site')
    ordering = ('order', 'id')
    search_fields = ('name', 'subtitle', 'description', 'price_text', 'image_alt')
    readonly_fields = ('image_preview',)

    fieldsets = (
        ('Контент', {'fields': ('name', 'subtitle', 'description', 'price_text')}),
        ('Зображення', {'fields': ('image', 'image_url', 'image_alt', 'image_preview')}),
        ('Налаштування', {'fields': ('order', 'featured', 'show_on_site')}),
    )

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width: 120px; max-height: 90px; border-radius: 10px;" />', obj.image.url)
        if obj.image_url:
            return format_html('<img src="{}" style="max-width: 120px; max-height: 90px; border-radius: 10px;" />', obj.image_url)
        return "Немає зображення"
    image_preview.short_description = "Попередній перегляд"
