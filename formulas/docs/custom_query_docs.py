from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import OpenApiParameter, extend_schema

subject_param = OpenApiParameter(
    name="subject",
    description="slug regex pattern [-a-zA-Z0-9_],",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
)

exam_number_param = OpenApiParameter(
    name="exam_number",
    description="regex pattern [1-6]),",
    type=OpenApiTypes.STR,
    location=OpenApiParameter.PATH,
)

custom_schema = extend_schema(
    parameters=[
        subject_param,
        exam_number_param,
    ],
    description="",
)
