import random
from functools import partial

import factory
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from factory.base import StubObject
from factory.django import DjangoModelFactory
from formulas.models import (Photo, PhotoClassification, PhotoContext, Profile,
                             Review, Subject, Tag)


@factory.django.mute_signals(post_save)
class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Profile

    career_name = factory.Faker('company')
    user = factory.SubFactory(
        'formulas.data_factories.UserFactory',
        profile=None
    )

@factory.django.mute_signals(post_save)
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.Sequence(lambda n: "user_%d" % n)
    password = factory.LazyFunction(lambda: make_password('secret1234'))
    email = factory.LazyAttribute(lambda obj: '%s@example.com' % obj.username)
    profile = factory.RelatedFactory(
        ProfileFactory, 
        factory_related_name='user'
    )


subject_names = [
    'physics',
    'calculus',
    'equations',
    'literaturezzz',
]

class SubjectFactory(DjangoModelFactory):
    class Meta:
        model = Subject
        django_get_or_create = ('name', )

    name = factory.Faker("random_element", elements=subject_names)
    
class PhotoClassificationFactory(DjangoModelFactory):
    class Meta:
        model = PhotoClassification
        django_get_or_create = ('subject', 'exam_number')

    subject = factory.SubFactory(SubjectFactory)
    exam_number = factory.Faker("pyint", min_value=1, max_value=4)


formula_types = [e[0] for e in PhotoContext.FormulaType.choices]

class PhotoContextFactory(DjangoModelFactory):
    class Meta:
        model = PhotoContext

    formula_type = factory.Faker("random_element", elements=formula_types)
    professor = factory.Faker("first_name")


tag_names = [
    'volumen',
    'heat',
    'work',
    'area',
]

class TagFactory(DjangoModelFactory):
    class Meta:
        model = Tag
        django_get_or_create = ('name', )


    name = factory.Faker("random_element", elements=tag_names)


image_paths = [
    'formulas/tests/test_images/testimage1.png', 
    'formulas/tests/test_images/testimage2.png', 
    'formulas/tests/test_images/testimage3.png'
]

def get_random_image_path():
    return random.choice(image_paths)


class PhotoFactory(DjangoModelFactory):
    class Meta:
        model = Photo
    
    name = factory.Sequence(lambda n: 'photo%d' % n)
    file = factory.django.ImageField(
        from_path=factory.LazyFunction(get_random_image_path)
    )
    description = factory.Faker("paragraph", nb_sentences=2)
    photo_classification = factory.SubFactory(PhotoClassificationFactory)
    photo_context = factory.SubFactory(PhotoContextFactory)

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)


# Must pass a photo and user
class ReviewFactory(DjangoModelFactory):
    class Meta:
        model = Review
    
    stars = factory.Faker("pyint", min_value=1, max_value=5)

def generate_dict_factory(factory):
    
    def convert_dict_from_stub(stub):
        stub_dict = stub.__dict__
        for key, value in stub_dict.items():
            if isinstance(value, StubObject):
                stub_dict[key] = convert_dict_from_stub(value)
        return stub_dict

    def dict_factory(factory, **kwargs):
        stub = factory.stub(**kwargs)
        stub_dict = convert_dict_from_stub(stub)
        return stub_dict

    return partial(dict_factory, factory)
