from django.urls import reverse
from rest_framework import status

from core.tests.mixins import TestCreateMixin, TestRetrieveMixin
from core.tests.test_utils import CrudTestBase
from formulas import views
from formulas.data_factories import PhotoContextFactory
from formulas.models import PhotoContext


class PhotoContextTest(CrudTestBase, TestCreateMixin, TestRetrieveMixin):

    use_normal_token = True
    model = PhotoContext
    model_factory = PhotoContextFactory

    def get_list_url(self):
        return reverse(views.PhotoContextList.name)

    def get_detail_url(self, pk):
        return reverse(views.PhotoContextDetail.name, args=[pk])

    def test_out_of_choices(self):
        data = {"professor": "mary", "formula_type": "FM22"}
        self.shortcut_post(data=data, status_code=status.HTTP_400_BAD_REQUEST)


PhotoContextTest.__test__ = True
