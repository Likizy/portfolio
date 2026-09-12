from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import ContactMessage, SiteContent


class PublicSiteTests(TestCase):
    def test_home_page_loads_with_default_content(self):
        response = self.client.get(reverse("index"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "index.html")
        self.assertTrue(SiteContent.objects.filter(pk=1).exists())
        self.assertContains(response, "assets/img/kiztech-tab-icon.")

    def test_valid_contact_submission_creates_a_message(self):
        response = self.client.post(
            reverse("index"),
            {
                "name": "Ada Lovelace",
                "email": "ada@example.com",
                "subject": "Project enquiry",
                "message": "I'd like to work together.",
            },
        )

        self.assertRedirects(response, f"{reverse('index')}#contact", fetch_redirect_response=False)
        message = ContactMessage.objects.get()
        self.assertEqual(message.email, "ada@example.com")
        self.assertFalse(message.is_read)

    def test_invalid_contact_submission_is_not_saved(self):
        response = self.client.post(
            reverse("index"),
            {
                "name": "Ada Lovelace",
                "email": "not-an-email",
                "subject": "Project enquiry",
                "message": "I'd like to work together.",
            },
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ContactMessage.objects.count(), 0)
        self.assertContains(response, "Please provide a valid name, email, subject, and message.")


class DashboardTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="admin-user",
            password="secure-test-password",
        )

    def test_dashboard_requires_authentication(self):
        response = self.client.get(reverse("portfolio_admin"))

        self.assertRedirects(response, f"{reverse('login')}?next={reverse('portfolio_admin')}")

    def test_user_can_mark_and_delete_messages(self):
        self.client.force_login(self.user)
        message = ContactMessage.objects.create(
            name="Grace Hopper",
            email="grace@example.com",
            subject="Hello",
            message="A test message.",
        )

        mark_response = self.client.post(reverse("mark_message_read", args=[message.pk]))
        self.assertRedirects(mark_response, reverse("portfolio_admin"))
        message.refresh_from_db()
        self.assertTrue(message.is_read)

        delete_response = self.client.post(reverse("delete_message", args=[message.pk]))
        self.assertRedirects(delete_response, reverse("portfolio_admin"))
        self.assertFalse(ContactMessage.objects.filter(pk=message.pk).exists())

    def test_dashboard_groups_content_fields_and_shows_unread_messages(self):
        self.client.force_login(self.user)
        ContactMessage.objects.create(
            name="Grace Hopper",
            email="grace@example.com",
            subject="Hello",
            message="A test message.",
        )

        response = self.client.get(reverse("portfolio_admin"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Brand &amp; hero")
        self.assertContains(response, "Unread messages")
        self.assertContains(response, "Mark as read")
