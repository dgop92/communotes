from django_filters import AllValuesFilter, FilterSet
from django_filters.filters import AllValuesMultipleFilter

from formulas.models import Photo, PhotoClassification, Review


class PhotoClassificationFilter(FilterSet):

    subject = AllValuesFilter(
        field_name = 'subject__name',
    )

    exam_number = AllValuesFilter(
        field_name = 'exam_number',
    )

    class Meta:
        model = PhotoClassification
        fields = (
            'subject',
            'exam_number',
        )


class PhotoFilter(FilterSet):

    subject = AllValuesFilter(
        field_name = 'photo_classification__subject__name',
    )

    exam_number = AllValuesFilter(
        field_name = 'photo_classification__exam_number',
    )

    photo_classification = AllValuesFilter(
        field_name='photo_classification__pk'
    )

    tag = AllValuesMultipleFilter(field_name='tags__name', conjoined=True)

    user = AllValuesFilter(
        field_name = 'user__pk',
    )

    class Meta:
        model = Photo
        fields = (
            'subject',
            'exam_number',
            'photo_classification',
            'tag',
            'user'
        )

class ReviewFilter(FilterSet):

    photo = AllValuesFilter(
        field_name = 'photo__pk',
    )

    class Meta:
        model = Review
        fields = (
            'photo',
        )

