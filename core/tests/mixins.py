import factory
from rest_framework import status

# lookup field support
class TestCreateMixin:
    
    def test_create(self):
        data = self.get_data_for_post()
        kwargs = {
            'data': data,
            'status_code': status.HTTP_201_CREATED,
        }
        kwargs.update(self.get_request_kwargs())
        kwargs.update(self.get_extra_create_kwargs())
        self.post(
            self.get_list_url(),
            **kwargs
        )
        self.assert_instance_exists(
            self.get_model(), 
            pk = self.json_response['pk']
        )

    def get_data_for_post(self):
        return factory.build(dict, FACTORY_CLASS=self.get_model_factory())

    def get_extra_create_kwargs(self):
        return {}

class TestListMixin:
    
    def test_list(self):
        obj_list = self.get_object_list() 
        n = len(obj_list)
        kwargs = {
            'status_code': status.HTTP_200_OK,
        }
        kwargs.update(self.get_request_kwargs())
        kwargs.update(self.get_extra_list_kwargs())
        self.get(
            self.get_list_url(),
            **kwargs
        )
        self.assertEqual(self.json_response['count'], n)
    
    def get_extra_list_kwargs(self):
        return {}

    def get_object_list(self):
        obj_list = self.get_model_factory().create_batch(3)
        return obj_list


class ObjectBaseMixin:

    def get_detail_object(self):
        return self.get_model_factory().create()

class TestRetrieveMixin(ObjectBaseMixin):
    
    def test_retrieve(self):
        object_detail = self.get_detail_object()
        pk = object_detail.pk
        kwargs = {
            'status_code': status.HTTP_200_OK,
        }
        kwargs.update(self.get_request_kwargs())
        kwargs.update(self.get_extra_retrieve_kwargs())
        self.get(
            self.get_detail_url(pk=pk),
            **kwargs
        )
        self.assertEqual(self.json_response['pk'], pk)
    
    def get_extra_retrieve_kwargs(self):
        return {}

class TestUpdateMixin(ObjectBaseMixin):
    
    def test_update(self):
        object_detail = self.get_detail_object()
        pk = object_detail.pk
        put_data = self.get_data_for_put()
        if put_data:
            kwargs = {
                'status_code': status.HTTP_200_OK,
                'data': put_data
            }
            kwargs.update(self.get_request_kwargs())
            kwargs.update(self.get_extra_update_kwargs())
            self.put(
                self.get_detail_url(pk=pk),
                **kwargs
            )
            self.assert_dict_contains_subset(self.json_response, put_data)
        
        patch_data = self.get_data_for_patch()
        if patch_data:
            kwargs = {
                'status_code': status.HTTP_200_OK,
                'data': patch_data
            }
            kwargs.update(self.get_request_kwargs())
            kwargs.update(self.get_extra_update_kwargs())
            self.patch(
                self.get_detail_url(pk=pk),
                **kwargs
            )
            self.assert_dict_contains_subset(self.json_response, patch_data)
    
    def get_data_for_put(self):
        return factory.build(dict, FACTORY_CLASS=self.get_model_factory())
    
    def get_data_for_patch(self):
        return {}

    def get_extra_update_kwargs(self):
        return {}

class TestDeleteMixin(ObjectBaseMixin):
    
    def test_delete(self):
        object_detail = self.get_detail_object()
        pk = object_detail.pk
        kwargs = {
            'status_code': status.HTTP_204_NO_CONTENT,
        }
        kwargs.update(self.get_request_kwargs())
        kwargs.update(self.get_extra_delete_kwargs())
        self.delete(
            self.get_detail_url(pk=pk),
            **kwargs
        )
        self.assert_instance_does_not_exist(
            self.get_model(),
            pk=pk
        )
        

    def get_extra_delete_kwargs(self):
        return {}

class TestListViewMixin(TestCreateMixin, TestListMixin):
    pass

class TestDetailViewMixin(TestRetrieveMixin, TestUpdateMixin, TestDeleteMixin):
    pass

TestCreateMixin.__test__ = False
TestListMixin.__test__ = False
TestRetrieveMixin.__test__ = False
TestUpdateMixin.__test__ = False
TestDeleteMixin.__test__ = False
    
    

    
    
