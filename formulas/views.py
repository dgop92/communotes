from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema_view
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from formulas.custom_filters import PhotoClassificationFilter, PhotoFilter, ReviewFilter
from formulas.custom_permissions import IsCurrentUserOwnerOrReadOnly
from formulas.docs import (
    photo_classification_docs,
    photo_context_docs,
    photo_docs,
    profile_docs,
    review_docs,
    subject_docs,
    tag_docs,
)
from formulas.models import (
    Photo,
    PhotoClassification,
    PhotoContext,
    Profile,
    Review,
    Subject,
    Tag,
)
from formulas.serializers import (
    PhotoClassificationSerializer,
    PhotoContextSerializer,
    PhotoSerializer,
    ProfileSerializer,
    ReviewSerializer,
    SubjectSerializer,
    TagSerializer,
)


@extend_schema_view(**photo_docs.custom_schema.get_list_view_schema())
class PhotoList(generics.ListCreateAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    name = "photo-list"

    permission_classes = [
        IsAuthenticated,
    ]

    filterset_class = PhotoFilter

    search_fields = (
        "$name",
        "$description",
    )
    ordering_fields = (
        "created_at",
        "updated_at",
    )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(**photo_docs.custom_schema.get_detail_view_schema())
class PhotoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer
    name = "photo-detail"

    permission_classes = [
        IsAuthenticated,
        IsCurrentUserOwnerOrReadOnly,
    ]

    def perform_destroy(self, instance):
        instance.file.delete()
        instance.delete()


@extend_schema_view(**photo_classification_docs.custom_schema.get_list_view_schema())
class PhotoClassificationList(generics.ListCreateAPIView):
    queryset = PhotoClassification.objects.all()
    serializer_class = PhotoClassificationSerializer
    name = "photoclassification-list"

    permission_classes = [
        IsAuthenticated,
    ]

    filterset_class = PhotoClassificationFilter

    ordering_fields = ("exam_number",)


@extend_schema_view(**photo_classification_docs.custom_schema.get_detail_view_schema())
class PhotoClassificationDetail(generics.RetrieveAPIView):
    queryset = PhotoClassification.objects.all()
    serializer_class = PhotoClassificationSerializer
    name = "photoclassification-detail"

    permission_classes = [
        IsAuthenticated,
    ]


@extend_schema_view(**photo_context_docs.custom_schema.get_list_view_schema())
class PhotoContextList(generics.CreateAPIView):
    queryset = PhotoContext.objects.all()
    serializer_class = PhotoContextSerializer
    name = "photocontext-list"

    permission_classes = [
        IsAuthenticated,
    ]


@extend_schema_view(**photo_context_docs.custom_schema.get_detail_view_schema())
class PhotoContextDetail(generics.RetrieveAPIView):
    queryset = PhotoContext.objects.all()
    serializer_class = PhotoContextSerializer
    name = "photocontext-detail"

    permission_classes = [
        IsAuthenticated,
    ]


@extend_schema_view(**profile_docs.custom_schema.get_detail_view_schema())
class ProfileDetail(generics.RetrieveUpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    name = "profile-detail"

    permission_classes = [
        IsAuthenticated,
    ]

    def get_object(self):
        return self.request.user.profile


@extend_schema_view(**review_docs.custom_schema.get_list_view_schema())
class ReviewList(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    name = "review-list"

    permission_classes = [
        IsAuthenticated,
    ]

    filterset_class = ReviewFilter

    ordering_fields = ("stars",)

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except IntegrityError:
            return Response(
                {"non_field_errors": [_("an user can only make one review per photo")]},
                status=status.HTTP_400_BAD_REQUEST,
            )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema_view(**review_docs.custom_schema.get_detail_view_schema())
class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    name = "review-detail"

    permission_classes = [
        IsAuthenticated,
        IsCurrentUserOwnerOrReadOnly,
    ]


@extend_schema_view(**subject_docs.custom_schema.get_list_view_schema())
class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    name = "subject-list"

    permission_classes = [
        IsAuthenticated,
    ]

    search_fields = ("$name",)
    ordering_fields = ("name",)


@extend_schema_view(**subject_docs.custom_schema.get_detail_view_schema())
class SubjectDetail(generics.RetrieveAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    name = "subject-detail"

    permission_classes = [
        IsAuthenticated,
    ]


@extend_schema_view(**tag_docs.custom_schema.get_list_view_schema())
class TagList(generics.ListCreateAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    name = "tag-list"

    permission_classes = [
        IsAuthenticated,
    ]

    search_fields = ("$name",)
    ordering_fields = ("name",)


@extend_schema_view(**tag_docs.custom_schema.get_detail_view_schema())
class TagDetail(generics.RetrieveAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    name = "tag-detail"

    permission_classes = [
        IsAuthenticated,
    ]
