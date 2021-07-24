from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from formulas.data_factories import TagFactory
from formulas.docs.docs_utils import (CustomSchemaHelper)
from formulas.serializers import TagSerializer

unique_error_examples = [
    OpenApiExample(
        name='Unique name response',
        value={
            "name": [
               "tag with this name already exists."
            ]
        },
        response_only=True,
        status_codes=["400"],
    )
]

class CustomTagSchema(CustomSchemaHelper):
    
    serializer = TagSerializer
    model_factory = TagFactory

    list_item_name = 'tag'
    detail_item_name = 'a tag'

    search_fields = (
        'name',
    )
    ordering_fields = (
        'name',
    )

    def get_detail_view_schema(self):
        return {
            'get': self.get_retrieve_schema(),
        }
    
    def get_custom_post_examples(self):
        return [*unique_error_examples, ]

    def get_extra_responses(self):
        return {
            'post': {400: OpenApiTypes.OBJECT}
        }

custom_schema = CustomTagSchema()