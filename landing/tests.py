from django.test import TestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
from io import BytesIO

from .models import BlogPost, CompanyInfo, EvacuatorOffer, EvacuatorSection


class HomePageEvacuatorTests(TestCase):
    def setUp(self):
        EvacuatorSection.objects.create(
            eyebrow="Евакуація техніки",
            title="Евакуатор для міста та області",
            description="Тестовий опис секції евакуатора.",
            cta_text="Замовити евакуатор",
        )
        EvacuatorOffer.objects.create(
            name="Малий евакуатор",
            subtitle="Тестова картка",
            description="Тестовий опис картки евакуатора.",
            price_text="від 3 000 грн",
            order=1,
        )

    def test_home_page_renders_evacuator_section(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Евакуатор для міста та області")
        self.assertContains(response, "Малий евакуатор")


class WebPConversionTests(TestCase):
    def test_blog_post_image_is_converted_to_webp(self):
        image_io = BytesIO()
        image = Image.new('RGB', (100, 100), color='red')
        image.save(image_io, format='JPEG')
        image_io.seek(0)

        uploaded = SimpleUploadedFile(
            'test-image.jpg',
            image_io.read(),
            content_type='image/jpeg',
        )

        post = BlogPost.objects.create(
            title='Test Blog Post',
            short_description='Short description',
            full_description='Full description',
            image=uploaded,
        )

        self.assertTrue(post.image.name.endswith('.webp'))


class SeoEndpointsTests(TestCase):
    def setUp(self):
        CompanyInfo.objects.create(
            name='Winkast',
            phone_primary='+380 97 339 83 24',
            address='Дніпро',
            working_hours='Пн–Сб: 08:00–19:00',
        )
        self.post = BlogPost.objects.create(
            title='Тестова SEO стаття',
            short_description='Короткий опис для sitemap.',
            full_description='Повний опис для sitemap.',
        )

    def test_robots_txt_contains_sitemap(self):
        response = self.client.get(reverse('robots_txt'))

        self.assertEqual(response.status_code, 200)
        self.assertIn('Sitemap:', response.content.decode())

    def test_sitemap_xml_contains_core_urls(self):
        response = self.client.get(reverse('sitemap_xml'))
        content = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn(reverse('home'), content)
        self.assertIn(reverse('blog_list'), content)
        self.assertIn(self.post.get_absolute_url(), content)
