from django.core.files.storage import default_storage
from django.test.utils import override_settings
from django.urls import reverse
from rest_framework import status

from core.tests import file_utils
from core.tests.mixins import TestDetailViewMixin, TestListViewMixin
from core.tests.test_utils import CrudTestBase
from formulas import views
from formulas.data_factories import PhotoFactory, generate_dict_factory
from formulas.models import (
    Photo,
    PhotoClassification,
    PhotoContext,
    Subject,
    Tag,
    user_photos_directory_path,
)


class PhotoTest(CrudTestBase, TestListViewMixin, TestDetailViewMixin):

    use_normal_token = True
    model = Photo
    model_factory = PhotoFactory

    def get_list_url(self):
        return reverse(views.PhotoList.name)

    def get_detail_url(self, pk):
        return reverse(views.PhotoDetail.name, args=[pk])

    def get_owner_user_dict(self):
        return self.normal_users[0]

    def get_owner_user(self):
        return self.get_owner_user_dict()["user"]

    def get_owner_profile(self):
        return self.get_owner_user_dict()["profile"]

    def get_extra_update_kwargs(self):
        return {"token": self.get_owner_user_dict()["token"]}

    def get_extra_delete_kwargs(self):
        return {"token": self.get_owner_user_dict()["token"]}

    def test_create(self):
        super().test_create()
        # check nested resources existence
        photo_cl_pk = self.json_response["photo_classification"]["pk"]
        photo_co_pk = self.json_response["photo_context"]["pk"]
        subject_name = self.json_response["photo_classification"]["subject"]
        self.assert_instance_exists(PhotoClassification, pk=photo_cl_pk)
        self.assert_instance_exists(PhotoContext, pk=photo_co_pk)
        self.assert_instance_exists(Subject, name=subject_name)
        # check tags
        tags = self.json_response["tags"]
        for tag_name in tags:
            self.assert_instance_exists(Tag, name=tag_name)

    def update_subject_name(self, photo_data):
        subject_name = photo_data["photo_classification"]["subject"]["name"]
        photo_data["photo_classification"]["subject"] = subject_name

    def get_data_for_post(self):
        dict_factory = generate_dict_factory(self.model_factory)
        data = dict_factory(file=None)
        data["tags"] = ["area", "volumen"]
        self.update_subject_name(data)
        return data

    def get_object_list(self):
        photos = PhotoFactory.create_batch(3, file=None, user=self.get_owner_user())
        return photos

    def get_detail_object(self):
        photo = PhotoFactory.create(file=None, user=self.get_owner_user())
        return photo

    def get_data_for_put(self):
        dict_factory = generate_dict_factory(self.model_factory)
        data = dict_factory(file=None)
        self.update_subject_name(data)
        return data

    def get_data_for_patch(self):
        dict_factory = generate_dict_factory(self.model_factory)
        data = dict_factory(file=None)
        data.pop("photo_context")
        data.pop("description")
        self.update_subject_name(data)
        return data

    @override_settings(DEFAULT_FILE_STORAGE="inmemorystorage.InMemoryStorage")
    def test_upload_photo(self):
        photo = PhotoFactory.create(file=None, user=self.get_owner_user())
        filename = "my_photo.png"
        created_file = file_utils.create_inmemory_image(filename)

        self.shortcut_patch(
            photo.pk,
            multipart=True,
            data={"file": created_file},
            token=self.get_owner_user_dict()["token"],
            status_code=status.HTTP_200_OK,
        )
        self.assertTrue(
            default_storage.exists(user_photos_directory_path(photo, filename))
        )

    def test_cannot_modify_other_users_photo(self):
        user1 = self.normal_users[0]["user"]
        user2_token = self.normal_users[1]["token"]
        photo = PhotoFactory.create(file=None, user=user1)

        self.shortcut_patch(
            photo.pk,
            data={"name": "random_name"},
            token=user2_token,
            status_code=status.HTTP_403_FORBIDDEN,
        )
        self.shortcut_delete(
            photo.pk, token=user2_token, status_code=status.HTTP_403_FORBIDDEN
        )

    def test_can_read_other_users_photo(self):
        user1 = self.normal_users[0]["user"]
        user2_token = self.normal_users[1]["token"]
        photo = PhotoFactory.create(file=None, user=user1)

        self.shortcut_get(photo.pk, token=user2_token, status_code=status.HTTP_200_OK)

    def test_subject_filter(self):
        def compare_subjects(s):
            return s == subject_name

        # The same subject can be in both photos due to randomness
        photo1 = PhotoFactory.create(file=None, user=self.get_owner_user())
        PhotoFactory.create(file=None, user=self.get_owner_user())
        subject_name = photo1.photo_classification.subject.name
        query = {"subject": subject_name}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        self.assertTrue(
            all(
                compare_subjects(item["photo_classification"]["subject"])
                for item in self.json_response["results"]
            )
        )

    def test_subject_exam_filter(self):
        # The same photo cl can be in both photos due to randomness
        photo1 = PhotoFactory.create(file=None, user=self.get_owner_user())
        PhotoFactory.create(file=None, user=self.get_owner_user())
        subject_name = photo1.photo_classification.subject.name
        exam_number = photo1.photo_classification.exam_number
        query = {"subject": subject_name, "exam_number": exam_number}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        self.assertTrue(
            all(
                item["photo_classification"]["subject"] == subject_name
                and item["photo_classification"]["exam_number"] == exam_number
                for item in self.json_response["results"]
            )
        )

    def test_photo_classification_filter(self):
        def compare_cl(pc):
            return pc == photo_classification.pk

        # The same photo classification can be in both photos due to randomness
        photo1 = PhotoFactory.create(file=None, user=self.get_owner_user())
        PhotoFactory.create(file=None, user=self.get_owner_user())
        photo_classification = photo1.photo_classification
        query = {"photo_classification": photo_classification.pk}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        self.assertTrue(
            all(
                compare_cl(item["photo_classification"]["pk"])
                for item in self.json_response["results"]
            )
        )

    def test_user_filter(self):
        photo1 = PhotoFactory.create(file=None, user=self.get_owner_user())
        PhotoFactory.create(file=None, user=self.normal_users[1]["user"])
        query = {"user": self.get_owner_user().pk}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        self.assertEqual(photo1.pk, self.json_response["results"][0]["pk"])
        self.assertEqual(1, self.json_response["count"])

    def test_tags_filter(self):
        t1 = Tag.objects.create(name="volume")
        t2 = Tag.objects.create(name="heat")
        PhotoFactory.create(file=None, user=self.get_owner_user(), tags=(t1,))
        PhotoFactory.create(file=None, user=self.get_owner_user(), tags=(t2,))
        p3 = PhotoFactory.create(file=None, user=self.get_owner_user(), tags=(t1, t2))
        query1 = [("tag", t1.name)]
        query2 = [("tag", t1.name), ("tag", t2.name)]

        self.shortcut_get(query=query1, status_code=status.HTTP_200_OK)
        self.assertTrue(
            all(t1.name in item["tags"] for item in self.json_response["results"])
        )

        self.shortcut_get(query=query2, status_code=status.HTTP_200_OK)
        self.assertEqual(p3.pk, self.json_response["results"][0]["pk"])
        self.assertEqual(1, self.json_response["count"])

    def test_search(self):
        photo1 = PhotoFactory.create(file=None, user=self.get_owner_user())
        photo1.name = "my custom name"
        photo1.save()
        photo2 = PhotoFactory.create(file=None, user=self.get_owner_user())
        photo2.description = "A special description"
        photo2.save()
        query1 = {"search": "my custom"}
        query2 = {"search": "special"}
        self.shortcut_get(query=query1, status_code=status.HTTP_200_OK)
        self.assertEqual(photo1.pk, self.json_response["results"][0]["pk"])
        self.assertEqual(1, self.json_response["count"])
        self.shortcut_get(query=query2, status_code=status.HTTP_200_OK)
        self.assertEqual(photo2.pk, self.json_response["results"][0]["pk"])
        self.assertEqual(1, self.json_response["count"])

    # and update ordering ?¿
    def test_created_ordering(self):

        photo1 = PhotoFactory.create(file=None, user=self.get_owner_user())
        photo2 = PhotoFactory.create(file=None, user=self.get_owner_user())

        # default ordering, newer photos appear first
        pk_list = [photo2.pk, photo1.pk]
        self.shortcut_get(status_code=status.HTTP_200_OK)
        results_pk_list = [item["pk"] for item in self.json_response["results"]]
        self.assertListEqual(pk_list, results_pk_list)

        pk_list = [photo1.pk, photo2.pk]
        query = {"ordering": "created_at"}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        results_pk_list = [item["pk"] for item in self.json_response["results"]]
        self.assertListEqual(pk_list, results_pk_list)


PhotoTest.__test__ = True
