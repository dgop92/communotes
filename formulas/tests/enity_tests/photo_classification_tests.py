from django.urls import reverse
from rest_framework import status

from core.tests.mixins import TestListViewMixin, TestRetrieveMixin
from core.tests.test_utils import CrudTestBase
from formulas import views
from formulas.data_factories import (
    PhotoClassificationFactory,
    SubjectFactory,
    generate_dict_factory,
)
from formulas.models import PhotoClassification


class PhotoClassificationTest(CrudTestBase, TestListViewMixin, TestRetrieveMixin):

    use_normal_token = True
    model = PhotoClassification
    model_factory = PhotoClassificationFactory

    def get_list_url(self):
        return reverse(views.PhotoClassificationList.name)

    def get_detail_url(self, pk):
        return reverse(views.PhotoClassificationDetail.name, args=[pk])

    def get_data_for_post(self):
        dict_factory = generate_dict_factory(self.model_factory)
        data = dict_factory()
        data["subject"] = data["subject"]["name"]
        return data

    def get_object_list(self):
        obj_list = PhotoClassificationFactory.create_batch(3)
        return set(obj_list)

    def test_invalid_names(self):
        data = {"subject": "some%+weird", "exam_number": 5}
        self.shortcut_post(data=data, status_code=status.HTTP_400_BAD_REQUEST)

        data = {"subject": "{ome: weird}", "exam_number": 5}
        self.shortcut_post(data=data, status_code=status.HTTP_400_BAD_REQUEST)

    def test_out_of_range_exam_number(self):
        data = {"subject": "calculus", "exam_number": 7}
        self.shortcut_post(data=data, status_code=status.HTTP_400_BAD_REQUEST)

        data = {"subject": "physics", "exam_number": 0}
        self.shortcut_post(data=data, status_code=status.HTTP_400_BAD_REQUEST)

    def test_get_or_create(self):

        photo_classification = PhotoClassificationFactory.create()

        data = {
            "subject": photo_classification.subject.name,
            "exam_number": photo_classification.exam_number,
        }
        self.shortcut_post(data=data, status_code=status.HTTP_201_CREATED)
        self.assertEqual(self.json_response["pk"], photo_classification.pk)

    def test_subject_filter(self):
        s1 = SubjectFactory.create(name="physics")
        s2 = SubjectFactory.create(name="calculus")
        pcl1 = PhotoClassificationFactory.create(subject=s1)
        PhotoClassificationFactory.create(subject=s2)
        query = {"subject": "physics"}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        self.assertEqual(pcl1.pk, self.json_response["results"][0]["pk"])
        self.assertEqual(1, self.json_response["count"])

    def test_exam_number_order(self):
        pcl1 = PhotoClassificationFactory.create(exam_number=2)
        pcl2 = PhotoClassificationFactory.create(exam_number=1)
        pk_list = [pcl2.pk, pcl1.pk]
        query = {"ordering": "exam_number"}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        results_pk_list = [item["pk"] for item in self.json_response["results"]]
        self.assertListEqual(pk_list, results_pk_list)


PhotoClassificationTest.__test__ = True
