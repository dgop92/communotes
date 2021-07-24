from formulas.data_factories import generate_dict_factory
from drf_spectacular.utils import OpenApiExample, OpenApiParameter, extend_schema

PRIMARY_KEY_VALUE = 1



class CustomSchemaHelper:

    create_description_template = "This endpoint allows you to create {0}"
    list_description_template = "This endpoint allows you list all {0}"
    retrieve_description_template = "This endpoint allows you to retrieve {0} by its id"
    update_description_template = "This endpoint allows you to update an existing {0}"
    delete_description_template = "This endpoint allows you to delete {0}"

    def __init__(self):
        self.dictionary_factory = generate_dict_factory(
            self.get_model_factory()
        )

    def get_data(self):
        return self.dictionary_factory()

    def add_response_fields(self, data):
        pass

    def get_extra_responses(self):
        return {}
 
    def get_list_schema(self):
        return extend_schema(
            parameters=[
                self.get_search_param(),
                self.get_ordering_param(),
                *self.get_custom_list_parameters()
            ],
            description=self.get_list_description(),
            examples=[
                self.get_successful_list_example(),
                *self.get_custom_list_examples(),
            ],
        )

    def get_search_param(self):
        search_fields = getattr(self, 'search_fields', [])
        search_fields_str = ", ".join(search_fields)
        descp = ""
        if search_fields_str:
            descp = f"search fields: {search_fields_str}"
        return OpenApiParameter(
            name="search",
            description=f"A search term. {descp}",
            exclude=bool(not descp)
        )
    
    def get_ordering_param(self):
        order_fields = getattr(self, 'ordering_fields', [])
        order_fields_str = ", ".join(order_fields)
        descp = f"Options: {order_fields_str}" if order_fields_str else ""
        return OpenApiParameter(
            name="ordering",
            description=f"Which field to use when ordering the results. {descp}",
        )

    def get_custom_list_parameters(self):
        return []

    def get_list_description(self):
        list_item_name = getattr(self, 'list_item_name', "No Name")
        return self.list_description_template.format(list_item_name)

    def get_successful_list_example(self):
        item_data = {'pk': PRIMARY_KEY_VALUE}
        item_data.update(self.get_data())
        self.add_response_fields(item_data)
        return OpenApiExample(
            name='Successful response',
            value={
                "count": 1,
                "next": None,
                "previous": None,
                "results": [
                    item_data
                ]
            },
            response_only=True,
            status_codes=["200"]
        )
    
    def get_custom_list_examples(self):
        return []

    def get_create_schema(self):
        return extend_schema(
            description=self.get_create_description(),
            responses={
                201: self.get_serializer(),
                **self.get_extra_responses().get('post', {})
            },
            examples=[
                *self.get_successful_post_examples(),
                *self.get_custom_post_examples(),
            ],
        )

    def get_create_description(self):
        detail_item_name = getattr(self, 'detail_item_name', "No Name")
        return self.create_description_template.format(detail_item_name)
    
    def get_successful_post_examples(self):
        data = self.get_data()
        request_example = OpenApiExample(
            name='Successful request',
            value=data,
            request_only=True,
        )
        data_response = {'pk': PRIMARY_KEY_VALUE}
        data_response.update(data)
        self.add_response_fields(data_response)
        response_example = OpenApiExample(
            name='Successful response',
            value=data_response,
            response_only=True,
            status_codes=["201"]
        )
        return request_example, response_example
    
    def get_custom_post_examples(self):
        return []

    def get_list_view_schema(self):
        return {
            'get': self.get_list_schema(),
            'post': self.get_create_schema(),
        }

    def get_retrieve_schema(self):
        return extend_schema(
            description=self.get_retrieve_description(),
            examples=[
                self.get_successful_detail_example(),
                *self.get_custom_retrieve_examples(),
            ],
        )

    def get_retrieve_description(self):
        detail_item_name = getattr(self, 'detail_item_name', "No Name")
        return self.retrieve_description_template.format(detail_item_name)
    
    def get_successful_detail_example(self):
        data = {'pk': PRIMARY_KEY_VALUE}
        data.update(self.get_data())
        self.add_response_fields(data)
        return OpenApiExample(
            name='Successful response',
            value=data,
            response_only=True,
            status_codes=["200"]
        )

    def get_custom_retrieve_examples(self):
        return []

    def get_update_schema(self):
        return extend_schema(
            description=self.get_update_description(),
            examples=[
                *self.get_successful_update_examples(),
                *self.get_custom_update_examples(),
            ],
        )

    def get_update_description(self):
        detail_item_name = getattr(self, 'detail_item_name', "No Name")
        return self.update_description_template.format(
            detail_item_name.split(" ")[1]
        )

    def get_successful_update_examples(self):
        data = self.get_data()
        request_example = OpenApiExample(
            name='Successful request',
            value=data,
            request_only=True,
        )
        data_response = {'pk': PRIMARY_KEY_VALUE}
        data_response.update(data)
        self.add_response_fields(data_response)
        response_example = OpenApiExample(
            name='Successful response',
            value=data_response,
            response_only=True,
            status_codes=["200"]
        )
        return request_example, response_example

    def get_custom_update_examples(self):
        return []

    def get_delete_description(self):
        detail_item_name = getattr(self, 'detail_item_name', "No Name")
        return self.delete_description_template.format(detail_item_name)

    def get_detail_view_schema(self):
        return {
            'get': self.get_retrieve_schema(),
            'put': self.get_update_schema(),
            'patch': self.get_update_schema(),
            'delete': extend_schema(description=self.get_delete_description())
        }

    def get_serializer(self):
        assert self.serializer is not None, (
            "'%s' should either include a `serializer` attribute, "
            "or override the `get_serializer()` method."
            % self.__class__.__name__
        )

        return self.serializer

    def get_model_factory(self):
        assert self.model_factory is not None, (
            "'%s' should either include a `model_factory` attribute, "
            "or override the `get_model_factory()` method."
            % self.__class__.__name__
        )

        return self.model_factory

    def get_list_view(self):
        assert self.list_view is not None, (
            "'%s' should either include a `list_view` attribute, "
            "or override the `get_list_view()` method."
            % self.__class__.__name__
        )

        return self.list_view

