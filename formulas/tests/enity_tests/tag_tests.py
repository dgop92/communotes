from django.urls import reverse
from rest_framework import status

from core.tests.mixins import TestListViewMixin, TestRetrieveMixin
from core.tests.test_utils import CrudTestBase
from formulas import views
from formulas.data_factories import TagFactory
from formulas.models import Tag


class TagTest(CrudTestBase, TestListViewMixin, TestRetrieveMixin):

    use_normal_token = True
    model = Tag
    model_factory = TagFactory

    def get_list_url(self):
        return reverse(views.TagList.name)

    def get_detail_url(self, pk):
        return reverse(views.TagDetail.name, args=[pk])

    def get_object_list(self):
        obj_list = TagFactory.create_batch(3)
        return set(obj_list)

    def test_empty_required_data(self):

        self.shortcut_post(data={"name": ""}, status_code=status.HTTP_400_BAD_REQUEST)

        self.shortcut_post(status_code=status.HTTP_400_BAD_REQUEST)

    def test_unique_error(self):

        self.shortcut_post(
            data={"name": "tag_name"}, status_code=status.HTTP_201_CREATED
        )

        self.shortcut_post(
            data={"name": "tag_name"}, status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_order(self):
        s1 = TagFactory.create(name="c-name")
        s2 = TagFactory.create(name="a-name")
        pk_list = [s2.pk, s1.pk]
        query = {"ordering": "name"}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        results_pk_list = [item["pk"] for item in self.json_response["results"]]
        self.assertListEqual(pk_list, results_pk_list)

    def test_search(self):
        s = TagFactory.create(name="volume")
        TagFactory.create(name="heat")
        query = {"search": "vol"}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        self.assertEqual(s.pk, self.json_response["results"][0]["pk"])


TagTest.__test__ = True
