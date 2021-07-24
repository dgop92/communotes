from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiExample
from formulas.data_factories import ProfileFactory
from formulas.docs.docs_utils import CustomSchemaHelper
from formulas.serializers import ProfileSerializer


class CustomProfileSchema(CustomSchemaHelper):
    
    retrieve_description_template = "This endpoint allows you to retrieve the current user's profile"
    update_description_template = "This endpoint allows you to update the current user's profile"

    serializer = ProfileSerializer
    model_factory = ProfileFactory

    def get_list_view_schema(self):
        return {}

    def get_detail_view_schema(self):
        schema = super().get_detail_view_schema()
        schema.pop('delete')
        return schema

    def get_data(self):
        data = self.dictionary_factory()
        data.pop('user')
        return data

    def add_response_fields(self, data):
        data['user'] = 1

custom_schema = CustomProfileSchema()