from django.contrib.postgres.search import SearchQuery, SearchVectorField
from django.db.models.expressions import RawSQL
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

    # no filter backends
    filter_backends = []

    def get_queryset(self):

        filter_kwargs = {
            "photo_classification__subject__name": self.kwargs["subject"],
        }
        exam_number_key = "photo_classification__exam_number"
        if "exam_number" in self.kwargs:
            filter_kwargs[exam_number_key] = self.kwargs.get("exam_number")

        query_set = Photo.objects.filter(**filter_kwargs)
        # search filter
        search_term = self.request.query_params.get("search")
        if search_term:
            sentences = search_term.split()
            sentences = map(lambda w: f"'{w}'", sentences)
            search_query = " & ".join(sentences)

            query_set = query_set.annotate(
                ts=RawSQL("search_vector", params=[], output_field=SearchVectorField())
            ).filter(ts=SearchQuery(search_query, search_type="raw", config="english"))

        return query_set
