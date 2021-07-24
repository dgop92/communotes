from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample, OpenApiParameter
from formulas.data_factories import ReviewFactory
from formulas.docs.docs_utils import CustomSchemaHelper
from formulas.serializers import ReviewSerializer

owner_review_error_examples = OpenApiExample(
    name='owner review response',
    value={
        "non_field_errors": [
            "Photo owner cannot make a review"
        ]
    },
    response_only=True,
    status_codes=["400"],
)


duplicate_review_error_example = OpenApiExample(
    name='duplicate review response',
    value={
        "non_field_errors": [
            "an user can only make one review per photo"
        ]
    },
    response_only=True,
    status_codes=["400"],
)

p1 = OpenApiParameter(
    name="photo",
    description="Photo pk",
    type=OpenApiTypes.INT
)

class CustomReviewSchema(CustomSchemaHelper):
    
    serializer = ReviewSerializer
    model_factory = ReviewFactory

    list_item_name = 'reviews'
    detail_item_name = 'a review'

    ordering_fields = (
        'stars',
    )

    def get_data(self):
        data = self.dictionary_factory(user=1, photo=2)
        return data
    
    def get_custom_post_examples(self):
        return [owner_review_error_examples, duplicate_review_error_example, ]

    def get_extra_responses(self):
        return {
            'post': {400: OpenApiTypes.OBJECT}
        }
    
    def get_custom_list_parameters(self):
        return [p1, ]

custom_schema = CustomReviewSchema()