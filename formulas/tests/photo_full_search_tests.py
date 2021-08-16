from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from django.urls.base import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from core.tests.test_utils import TestApiBase
from formulas import query_views
from formulas.data_factories import PhotoFactory
from formulas.models import Photo, PhotoClassification, Subject

# url with slufigy


class PhotoFullSearchTest(TestApiBase, TestCase):
    @classmethod
    def setUpTestData(cls):

        cls.super_user = {}
        user = get_user_model().objects.create_superuser(
            "root", "root1234", "secret1234"
        )
        refresh = RefreshToken.for_user(user)

        cls.super_user["user"] = user
        cls.super_user["profile"] = user.profile
        cls.super_user["token"] = str(refresh.access_token)

        cls.subject1 = Subject.objects.create(name="calculus")
        cls.subject2 = Subject.objects.create(name="physics")

        cls.photo_classification1 = PhotoClassification.objects.create(
            subject=cls.subject1, exam_number=1
        )
        cls.photo_classification2 = PhotoClassification.objects.create(
            subject=cls.subject2, exam_number=1
        )
        cls.photo_classification3 = PhotoClassification.objects.create(
            subject=cls.subject2, exam_number=2
        )

    def setUp(self):
        self.init()

    def get_url(self, args, search_querys=None):
        url = reverse(query_views.SearchFormulaView.name, args=args)
        if search_querys:
            url += f"?{urlencode(search_querys)}"
        return url

    def test_subject_filter(self):
        photo = PhotoFactory(
            file=None,
            user=self.super_user["user"],
            photo_classification=self.photo_classification1,
        )
        PhotoFactory(
            file=None,
            user=self.super_user["user"],
            photo_classification=self.photo_classification2,
        )
        url = self.get_url(args=(self.subject1.name,))
        self.get(url, token=self.super_user["token"], status_code=status.HTTP_200_OK)
        self.assertEqual(1, self.json_response["count"])
        self.assertEqual(photo.pk, self.json_response["results"][0]["pk"])

    def test_subject_filter_with_exam_number(self):
        photo = PhotoFactory(
            file=None,
            user=self.super_user["user"],
            photo_classification=self.photo_classification2,
        )
        PhotoFactory(
            file=None,
            user=self.super_user["user"],
            photo_classification=self.photo_classification3,
        )
        url = self.get_url(args=(self.subject2.name, 1))
        self.get(url, token=self.super_user["token"], status_code=status.HTTP_200_OK)
        self.assertEqual(1, self.json_response["count"])
        self.assertEqual(photo.pk, self.json_response["results"][0]["pk"])

    def test_full_text_search(self):
        photo1 = Photo.objects.create(
            name="Electricity charge",
            description="Electric fields are important in physics",
            user=self.super_user["user"],
            photo_classification=self.photo_classification2,
        )
        PhotoFactory(
            name="Electromagnetism",
            description="Electromagnetism is a branch of physics involving the study of the electromagnetic force",
            file=None,
            user=self.super_user["user"],
            photo_classification=self.photo_classification3,
        )
        # retrieve the first photo
        url = self.get_url(
            args=(self.subject2.name,), search_querys={"search": "Electric fields"}
        )
        self.get(url, token=self.super_user["token"], status_code=status.HTTP_200_OK)
        self.assertEqual(1, self.json_response["count"])
        self.assertEqual(photo1.pk, self.json_response["results"][0]["pk"])

        # retrieve the both photos
        url = self.get_url(
            args=(self.subject2.name,), search_querys={"search": "physics"}
        )
        self.get(url, token=self.super_user["token"], status_code=status.HTTP_200_OK)
        self.assertEqual(2, self.json_response["count"])
