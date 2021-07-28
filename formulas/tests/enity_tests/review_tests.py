from django.urls import reverse
from rest_framework import status

from core.tests.mixins import TestDetailViewMixin, TestListViewMixin
from core.tests.test_utils import CrudTestBase
from formulas import views
from formulas.data_factories import PhotoFactory, ReviewFactory
from formulas.models import Review


class ReviewTest(CrudTestBase, TestListViewMixin, TestDetailViewMixin):

    use_normal_token = True
    model = Review
    model_factory = ReviewFactory

    def create_object_dependencies(self):
        self.photos = PhotoFactory.create_batch(
            3, file=None, user=self.normal_users[0]["user"]
        )

    def get_list_url(self):
        return reverse(views.ReviewList.name)

    def get_detail_url(self, pk):
        return reverse(views.ReviewDetail.name, args=[pk])

    # req kwargs could be a better solution

    def get_extra_create_kwargs(self):
        return {"token": self.normal_users[1]["token"]}

    def get_extra_update_kwargs(self):
        return {"token": self.normal_users[1]["token"]}

    def get_extra_delete_kwargs(self):
        return {"token": self.normal_users[1]["token"]}

    def get_data_for_post(self):
        data = super().get_data_for_post()
        data["photo"] = self.photos[0].pk
        return data

    def get_object_list(self):
        obj_list = []
        # owner photo cannot create a review
        for user_dict in self.normal_users[1:]:
            user = user_dict["user"]
            obj_list.append(ReviewFactory.create(photo=self.photos[0], user=user))
        return obj_list

    def get_detail_object(self):
        review = self.get_model_factory().create(
            photo=self.photos[0],
            user=self.normal_users[1]["user"],
        )
        return review

    def get_data_for_put(self):
        return self.get_data_for_post()

    def get_data_for_patch(self):
        return {"stars": 5}

    def test_review_made_by_photo_owner(self):

        data = self.get_data_for_post()
        owner_token = self.normal_users[0]["token"]

        self.shortcut_post(
            data=data, token=owner_token, status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_one_review_per_photo(self):
        # Create a review with user 1
        self.get_detail_object()

        token = self.normal_users[1]["token"]
        data = self.get_data_for_post()
        self.shortcut_post(
            data=data, token=token, status_code=status.HTTP_400_BAD_REQUEST
        )

    def test_stars_range(self):
        # owner photo cannot create a review
        for user_dict in self.normal_users[1:]:
            token = user_dict["token"]
            data = self.get_data_for_post()
            data["stars"] = 6
            self.shortcut_post(
                data=data, token=token, status_code=status.HTTP_400_BAD_REQUEST
            )

    def test_photo_filter(self):
        photo = self.photos[0]
        # owner photo cannot create a review
        for user_dict in self.normal_users[1:]:
            user = user_dict["user"]
            ReviewFactory.create(photo=photo, user=user)
            ReviewFactory.create(photo=self.photos[1], user=user)
        query = {"photo": photo.pk}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        self.assertEqual(2, self.json_response["count"])
        self.assertTrue(
            all(photo.pk == item["photo"] for item in self.json_response["results"])
        )

    def test_star_ordering(self):
        r1 = ReviewFactory.create(
            photo=self.photos[0], user=self.normal_users[0]["user"], stars=4
        )
        r2 = ReviewFactory.create(
            photo=self.photos[0], user=self.normal_users[1]["user"], stars=2
        )
        pk_list = [r2.pk, r1.pk]
        query = {"ordering": "stars"}
        self.shortcut_get(query=query, status_code=status.HTTP_200_OK)
        results_pk_list = [item["pk"] for item in self.json_response["results"]]
        self.assertListEqual(pk_list, results_pk_list)


ReviewTest.__test__ = True
