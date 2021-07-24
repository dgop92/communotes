import textwrap
from drf_spectacular.types import OpenApiTypes

from drf_spectacular.utils import OpenApiParameter

from formulas.data_factories import PhotoFactory
from formulas.docs.docs_utils import CustomSchemaHelper
from formulas.serializers import PhotoSerializer

p1 = OpenApiParameter(
    name="photo_classification",
    description="Photo Classification pk",
    type=OpenApiTypes.INT
)
p2 = OpenApiParameter(
    name="subject",
    description="Subject name",
)
p3 = OpenApiParameter(
    name="tag",
    description="Tag name",
    type=OpenApiTypes.STR
)
p4 = OpenApiParameter(
    name="user",
    description="User pk",
    type=OpenApiTypes.INT
)

class CustomPhotoSchema(CustomSchemaHelper):
    
    serializer = PhotoSerializer
    model_factory = PhotoFactory

    list_item_name = 'photos'
    detail_item_name = 'a photo'

    search_fields = (
        'name',
        'description',
    )
    ordering_fields = (
        'created_at',
        'updated_at',
    )

    def get_create_description(self):
        description = f"""
        {super().get_create_description()} <br><br>
        * images are uploaded by a patch method
        * photo classification, photo context and tags works by `get_or_create` functionality, in other words, if they don't exit there will be created
        """
        return textwrap.dedent(description)

    def get_list_description(self):
        description = f"""
        {super().get_list_description()} <br><br>
        * filter by multiple tags repeating the query param. ex: `tag=value1&tag=value2`

        * tags filtering is conjoined, in other wors use SQL AND 
        """
        return textwrap.dedent(description)

    def get_update_description(self):
        description = f"""
        {super().get_update_description()} <br><br>
        * if you're not the owner of the photo, this method will display a forbidden error
        """
        return textwrap.dedent(description)
    
    def get_delete_description(self):
        description = f"""
        {super().get_delete_description()} <br><br>
        * if you're not the owner of the photo, this method will display a forbidden error
        """
        return textwrap.dedent(description)

    def get_data(self):
        data = self.dictionary_factory(file = None)
        subject_name = data['photo_classification']['subject']['name']
        data['photo_classification']['subject'] = subject_name
        data['tags'] = ['area', 'volumen']
        return data

    def add_response_fields(self, data):
        data['user'] = 1
        data['created_at'] = "2021-07-07T16:18:29.206357Z"
        data['updated_at'] = "2021-07-07T16:18:29.206357Z"

    def get_custom_list_parameters(self):
        return [p1, p2, p3, p4]
    
custom_schema = CustomPhotoSchema()
