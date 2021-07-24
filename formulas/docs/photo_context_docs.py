from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from formulas.data_factories import PhotoContextFactory
from formulas.docs.docs_utils import CustomSchemaHelper
from formulas.serializers import PhotoContextSerializer


formula_type_error_examples = [
    OpenApiExample(
        name="Invalid type",
        value={"professor": "Kelly", "formula_type": "kks2"},
        request_only=True,
    ),
    OpenApiExample(
        name="Invalid type response",
        value={
            "formula_type": ['"kks2" is not a valid choice.']
        },
        response_only=True,
        status_codes=["400"],
    ),
]


class CustomPhotoContextSchema(CustomSchemaHelper):

    serializer = PhotoContextSerializer
    model_factory = PhotoContextFactory

    detail_item_name = "a photo context"

    def get_custom_post_examples(self):
        return [
            *formula_type_error_examples
        ]

    def get_list_view_schema(self):
        return {
            "post": self.get_create_schema(),
        }

    def get_detail_view_schema(self):
        return {
            "get": self.get_retrieve_schema(),
        }

    def get_extra_responses(self):
        return {"post": {400: OpenApiTypes.OBJECT}}


custom_schema = CustomPhotoContextSchema()
