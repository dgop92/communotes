from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from formulas.data_factories import SubjectFactory
from formulas.docs.docs_utils import CustomSchemaHelper
from formulas.serializers import SubjectSerializer

pagination_description = """
For this example let's suppose your query is the following ?page=2.
Note: remember default page size is 10, however in this example not all items are included
"""

pagination_example = OpenApiExample(
    'Pagination',
    value={
        "count": 35,
        "next": "{{baseUrl}}/formulas/subjects/?page=3",
        "previous": "{{baseUrl}}/formulas/subjects/?page=1",
        "results": [
            {
                "pk": 11,
                "name": "calculus"
            },
            {
                "pk": 12,
                "name": "physics"
            }
        ]
    },
    description=pagination_description,
    response_only=True,
    status_codes=["200"]
)

slug_error_examples = [
    OpenApiExample(
        name='Invalid name',
        value={
            'name': 'phy$5+ca'
        },
        request_only=True,
    ),
    OpenApiExample(
        name='Invalid name response',
        value={
            "name": [
                "Enter a valid \"slug\" consisting of letters, numbers, underscores or hyphens."
            ]
        },
        response_only=True,
        status_codes=["400"],
    )
]

unique_error_examples = [
    OpenApiExample(
        name='Unique name response',
        value={
            "name": [
               "subject with this name already exists."
            ]
        },
        response_only=True,
        status_codes=["400"],
    )
]

class CustomSubjectSchema(CustomSchemaHelper):
    
    serializer = SubjectSerializer
    model_factory = SubjectFactory

    list_item_name = 'subjects'
    detail_item_name = 'a subject'

    search_fields = (
        'name',
    )
    ordering_fields = (
        'name',
    )

    def get_custom_list_examples(self):
        return [pagination_example, ]

    def get_custom_post_examples(self):
        return [*slug_error_examples, *unique_error_examples, ]

    def get_detail_view_schema(self):
        return {
            'get': self.get_retrieve_schema(),
        }

    def get_extra_responses(self):
        return {
            'post': {400: OpenApiTypes.OBJECT}
        }

custom_schema = CustomSubjectSchema()