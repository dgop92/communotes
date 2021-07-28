from django.test.testcases import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from core.tests.test_utils import TestApiBase
from formulas import views
from formulas.data_factories import UserFactory


class ProfileTest(TestApiBase, TestCase):
    def setUp(self):
        self.init()
        self.user = UserFactory.create()
        self.token = RefreshToken.for_user(self.user).access_token

    def get_detail_url(self):
        return reverse(views.ProfileDetail.name)

    def test_retrieve(self):

        self.get(
            self.get_detail_url(), token=self.token, status_code=status.HTTP_200_OK
        )
        self.assertEqual(self.user.profile.pk, self.json_response["pk"])

    def test_update(self):

        data = {"career_name": "some career"}
        self.patch(
            self.get_detail_url(),
            data=data,
            token=self.token,
            status_code=status.HTTP_200_OK,
        )
        self.user.refresh_from_db()
        self.assertEqual(self.user.profile.career_name, data["career_name"])


ProfileTest.__test__ = True
