import json
import random
from urllib.parse import urlencode

from django.contrib.auth import get_user_model
from django.test.testcases import TestCase
from core.tests.assertions import InstanceAssertionsMixin
from formulas.data_factories import UserFactory
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken

class TestApiBase:
    
    def init(self):

        self.client = APIClient()
        self.json_response = {}
        self.print_output = True

    def send_request(self, request_method, *args, **kwargs):
        request_func = getattr(self.client, request_method)
        status_code = None

        if 'multipart' not in kwargs:
            if 'content_type' not in kwargs and request_method != 'get':
                kwargs['content_type'] = 'application/json'
                if 'data' in kwargs:
                    data = kwargs.get('data', '')
                    kwargs['data'] = json.dumps(data)
        else:
            kwargs.pop('multipart')

        if 'status_code' in kwargs:
            status_code = kwargs.pop('status_code')

        if 'token' in kwargs:
            kwargs['HTTP_AUTHORIZATION'] = \
                'Bearer %s' % kwargs.pop('token')
        
        self.response = request_func(*args, **kwargs)

        is_json = bool(
            'content-type' in self.response._headers and
            [x for x in self.response._headers['content-type'] if 'json' in x]
        )

        if is_json and self.response.content:
            self.json_response = self.response.json()
            if self.print_output:
                print(json.dumps(
                    self.json_response, indent=4, ensure_ascii=False
                ))

        if status_code:
            assert self.response.status_code == status_code

        return self.response

    def post(self, *args, **kwargs):
        return self.send_request('post', *args, **kwargs)

    def get(self, *args, **kwargs):
        return self.send_request('get', *args, **kwargs)

    def put(self, *args, **kwargs):
        return self.send_request('put', *args, **kwargs)

    def patch(self, *args, **kwargs):
        return self.send_request('patch', *args, **kwargs)

    def delete(self, *args, **kwargs):
        return self.send_request('delete', *args, **kwargs)
    
    def compare_json_response_given_data(self, data: dict, 
        oppositive = False):
        for data_key in data.keys():
            if oppositive:
                assert self.json_response[data_key] != data[data_key]
            else:
                assert self.json_response[data_key] == data[data_key]

    def assert_dict_contains_subset(self, supersetdict, subsetdict):

        def is_subset(subset, superset):
            if isinstance(subset, dict):
                return all(key in superset and is_subset(val, superset[key]) for key, val in subset.items())

            if isinstance(subset, list) or isinstance(subset, set):
                return all(any(is_subset(subitem, superitem) for superitem in superset) for subitem in subset)

            return subset == superset
        
        return is_subset(subsetdict, supersetdict)
    

ADMIN_DATA = {
    "username": "admin_dp",
    "email": "admin_examaple@example.com",
    "password": "admin1234admin"
}

# lookup field support
class CrudTestBase(TestApiBase, InstanceAssertionsMixin, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.create_users(cls)
        cls.create_object_dependencies(cls)
    
    def setUp(self):
        self.init()
        self.execute_before_each_test()
    
    def create_users(self):

        # get super user
        User = get_user_model();
        self.super_user = {}
        user = User.objects.create_superuser(
            ADMIN_DATA["username"], 
            ADMIN_DATA["email"], 
            ADMIN_DATA["password"]
        )
        refresh = RefreshToken.for_user(user)

        self.super_user['user'] = user
        self.super_user['profile'] = user.profile
        self.super_user['token'] = str(refresh.access_token)

        # create random normal users
        self.normal_users = []
        users = UserFactory.create_batch(3)

        for user in users:
            normal_user = {}
            normal_user['user'] = user
            normal_user['profile'] = user.profile
            refresh = RefreshToken.for_user(user)
            normal_user['token'] = str(refresh.access_token)
            self.normal_users.append(normal_user)

    def get_random_normal_token(self):
        return random.choice(self.normal_users)['token']

    def get_list_url(self):
        raise NotImplementedError("get_list_url() must be implemented")
    
    def get_detail_url(self, pk):
        raise NotImplementedError("get_detail_url() must be implemented")

    def get_model(self):
        assert self.model is not None, (
            "'%s' should either include a `model` attribute, "
            "or override the `get_model()` method."
            % self.__class__.__name__
        )

        return self.model

    def get_model_factory(self):
        assert self.model_factory is not None, (
            "'%s' should either include a `model_factory` attribute, "
            "or override the `get_model_factory()` method."
            % self.__class__.__name__
        )

        return self.model_factory
    
    def get_request_kwargs(self):
        """
        If you override this method, ensure to mix your dict 
        with the return of the super statement
        """
        if getattr(self, 'use_normal_token', False):
            return {'token': self.get_random_normal_token()}
        return {}

    def execute_before_each_test(self):
        pass

    def create_object_dependencies(self):
        pass

    def shortcut_post(self, *args, **kwargs):
        req_kwargs = self.get_request_kwargs()
        req_kwargs.update(kwargs)
        self.post(self.get_list_url(), *args, **req_kwargs)
    
    def shortcut_get(self, pk = None, *args, **kwargs):
        url = self.get_detail_url(pk=pk) if pk else self.get_list_url()
        if not pk and 'query' in kwargs:
            query = urlencode(kwargs.pop('query'))
            url += f'?{query}'
        req_kwargs = self.get_request_kwargs()
        req_kwargs.update(kwargs)
        self.get(url, *args, **req_kwargs)
    
    def shortcut_put(self, pk, *args, **kwargs):
        req_kwargs = self.get_request_kwargs()
        req_kwargs.update(kwargs)
        self.put(self.get_detail_url(pk=pk), *args, **req_kwargs)
    
    def shortcut_patch(self, pk, *args, **kwargs):
        req_kwargs = self.get_request_kwargs()
        req_kwargs.update(kwargs)
        self.patch(self.get_detail_url(pk=pk), *args, **req_kwargs)
    
    def shortcut_delete(self, pk, *args, **kwargs):
        req_kwargs = self.get_request_kwargs()
        req_kwargs.update(kwargs)
        self.delete(self.get_detail_url(pk=pk), *args, **req_kwargs)