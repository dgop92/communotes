from django.urls import reverse
from rest_framework import status

from core.tests.mixins import TestListViewMixin, TestRetrieveMixin
from core.tests.test_utils import CrudTestBase
from formulas import views
from formulas.data_factories import SubjectFactory
from formulas.models import Subject


class SubjectTest(CrudTestBase, TestListViewMixin, TestRetrieveMixin):

    use_normal_token = True
    model = Subject
    model_factory = SubjectFactory

    def get_list_url(self):
        return reverse(views.SubjectList.name)

    def get_detail_url(self, pk):
        return reverse(views.SubjectDetail.name, args=[pk])

    def get_object_list(self):
        obj_list = SubjectFactory.create_batch(3)
        return set(obj_list)

    def test_invalid_names(self):

        data = {"name": "some%+weird"}
        self.shortcut_post(data=data, status_code=status.HTTP_400_BAD_REQUEST)

        data = {"name": "{ome: weird}"}
        self.shortcut_post(data=data, status_code=status.HTTP_400_BAD_REQUEST)

    def test_empty_required_data(self):

        self.shortcut_post(data={"name": ""}, status_code=status.HTTP_400_BAD_REQUEST)

        self.shortcut_post(status_code=status.HTTP_400_BAD_REQUEST)

    def test_unique_error(self):

        self.shortcut_post(
            data={"name": "subject_name"}, status_code=status.HTTP_201_CREATED
        )

        self.shortcut_post(
            data={"name": "subject_name"}, status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_order(self):
        s1 = SubjectFactory.create(name="c-name")
        s2 = SubjectFactory.create(name="a-name")
        pk_list = [s2.pk, s1.pk]
        query = {"ordering": "name"}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        results_pk_list = [item["pk"] for item in self.json_response["results"]]
        self.assertListEqual(pk_list, results_pk_list)

    def test_search(self):
        s = SubjectFactory.create(name="physics")
        SubjectFactory.create(name="calculus")
        query = {"search": "phy"}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        self.assertEqual(s.pk, self.json_response["results"][0]["pk"])
        self.assertEqual(1, self.json_response["count"])


SubjectTest.__test__ = True
