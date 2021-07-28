import textwrap

from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter

from formulas.data_factories import PhotoClassificationFactory
from formulas.docs.docs_utils import CustomSchemaHelper
from formulas.serializers import PhotoClassificationSerializer

exam_number_error_examples = [
    OpenApiExample(
        name="Invalid number",
        value={"name": "calculus", "exam_number": 8},
        request_only=True,
    ),
    OpenApiExample(
        name="Invalid number response",
        value={"exam_number": ["Ensure this value is less than or equal to 6."]},
        response_only=True,
        status_codes=["400"],
    ),
]

p1 = OpenApiParameter(
    name="subject",
    description="Subject name",
)


class CustomPhotoClassificationSchema(CustomSchemaHelper):

    serializer = PhotoClassificationSerializer
    model_factory = PhotoClassificationFactory

    list_item_name = "photo classifications"
    detail_item_name = "a photo classification"

    ordering_fields = ("exam_number",)

    def get_create_description(self):
        description = f"""
        {super().get_create_description()} <br><br>
        This endpoint will not create duplicates, if you try to post an already existing item you will receive the proper 'get' response for that item
        """
        return textwrap.dedent(description)

    def get_data(self):
        data = self.dictionary_factory()
        data["subject"] = data["subject"]["name"]
        return data

    def get_custom_post_examples(self):
        return [
            *exam_number_error_examples,
        ]

    def get_extra_responses(self):
        return {"post": {400: OpenApiTypes.OBJECT}}

    def get_detail_view_schema(self):
        return {
            "get": self.get_retrieve_schema(),
        }

    def get_custom_list_parameters(self):
        return [
            p1,
        ]


custom_schema = CustomPhotoClassificationSchema()
