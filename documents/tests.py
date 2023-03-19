from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model

from users.models import CustomUser
from .models import Document, DocumentCategory

NUMBER_ACTUAL_DOCS = 10
NUMBER_COMPLETED_DOCS = 5
NUMBER_ARCHIVED_DOCS = 7


class DocumentListViewTest(TestCase):
    """
    Test Document list view.
    """
    username = "testuser"
    password = "password"
    super_name = "superuser"
    super_password = "superword"

    @classmethod
    def setUpTestData(cls):
        # Create test users
        new_user = get_user_model().objects.create_user(cls.username, password=cls.password)
        super_user = get_user_model().objects.create_user(cls.super_name, password=cls.super_password,
                                                          is_superuser=True)

        category = DocumentCategory.objects.create(title="Misc", description="Miscellaneous stuff")

        for i_doc in range(NUMBER_ACTUAL_DOCS):
            doc = Document.objects.create(title=f"Document {i_doc}", category=category, body=f"Document {i_doc} body.",
                                          author=super_user, is_completed=False, is_archived=False)
            doc.users_acquainted.add(super_user)

        for i_doc in range(NUMBER_COMPLETED_DOCS):
            doc = Document.objects.create(title=f"Completed document {i_doc}", category=category,
                                          body=f"Completed document {i_doc} body.",
                                          author=super_user, is_completed=True, is_archived=False)
            doc.users_acquainted.add(super_user)

        for i_doc in range(NUMBER_ARCHIVED_DOCS):
            doc = Document.objects.create(title=f"Archived document {i_doc}", category=category,
                                          body=f"Archived document {i_doc} body.",
                                          author=super_user, is_completed=False, is_archived=True)
            doc.users_acquainted.add(super_user)

    def test_documents_list_url(self):
        """
        Ensure the "documents:document_list" view is inaccessible without login
        """
        # Redirect when not logged in
        url = reverse("documents:document_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_document_list_view_login(self):
        """
        Test the "documents:document_list" accessible with login
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        # Go to list page
        url = reverse("documents:document_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_document_list_view_docs_count(self):
        """
        Check number of Documents shown in the list
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        # Go to list page
        url = reverse("documents:document_list")
        response = self.client.get(url)

        self.assertEqual(len(response.context["document_list"]), NUMBER_ACTUAL_DOCS)

    def test_document_list_view_docs_by_category_count(self):
        """
        Check number of Documents shown in the list filtered by category
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)
        category = DocumentCategory.objects.first()
        # Go to list page
        url = reverse("documents:document_list") + "?category_id=" + str(category.id)
        response = self.client.get(url)

        # Since we have only one category, there must be all "actual" documents in the list.
        self.assertEqual(len(response.context["document_list"]), NUMBER_ACTUAL_DOCS)

    def test_document_detail_view(self):
        """
        Ensure that Document detail view works
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)

        doc = Document.objects.first()
        url = doc.get_absolute_url()
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)

    def test_document_detail_view_has_acquaint_button(self):
        """
        Check if not acquainted user has "Acquaint" button
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)

        doc = Document.objects.first()
        url = doc.get_absolute_url()
        response = self.client.get(url)

        self.assertContains(response, "Ознакомлен")

    def test_document_detail_view_has_no_acquaint_button(self):
        """
        Check if acquainted user hasn't "Acquaint" button
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)

        user = CustomUser.objects.get(username=self.username)
        doc = Document.objects.first()
        doc.users_acquainted.add(user)

        url = doc.get_absolute_url()
        response = self.client.get(url)

        self.assertNotContains(response, "Ознакомлен")

    def test_document_htmx_acquintance(self):
        """
        Check if HTMX acquaintance view works
        """
        # Login as usual user
        url = reverse("login")
        response = self.client.post(url, {"username": self.username, "password": self.password},
                                    follow=True)

        user = CustomUser.objects.get(username=self.username)
        doc = Document.objects.first()
        pk = doc.pk

        # `user` is not acquainted with `doc`, test `documents:document_acquaint` view:
        url = reverse("documents:document_acquaint", args=[pk])
        response = self.client.post(url, {}, follow=True)

        doc = Document.objects.get(pk=pk)

        self.assertEqual(response.status_code, 200)
        assert(user in doc.users_acquainted.all())
