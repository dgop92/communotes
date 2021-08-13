from drf_spectacular.utils import extend_schema_view
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from formulas.docs import custom_query_docs
from formulas.models import Photo
from formulas.serializers import PhotoSerializer


@extend_schema_view(get=custom_query_docs.custom_schema)
class SearchFormulaView(generics.ListAPIView):
    name = "search_formula"
    serializer_class = PhotoSerializer

    permission_classes = [
        IsAuthenticated,
    ]

    search_fields = (
        "$name",
        "$description",
    )

    def get_queryset(self):

        filter_kwargs = {
            "photo_classification__subject__name": self.kwargs["subject"],
        }
        exam_number_key = "photo_classification__exam_number"
        if "exam_number" in self.kwargs:
            filter_kwargs[exam_number_key] = self.kwargs.get("exam_number")

        return Photo.objects.filter(**filter_kwargs)
