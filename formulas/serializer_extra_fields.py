from rest_framework.relations import SlugRelatedField

""" copy from https://github.com/Hipo/drf-extra-fields/blob/master/drf_extra_fields/fields.py """


class SlugGetOrCreateRelatedField(SlugRelatedField):
    def __init__(self, slug_field=None, internal_validators=None, **kwargs):
        if not internal_validators:
            self.internal_validators = []
        else:
            self.internal_validators = internal_validators
        super().__init__(slug_field=slug_field, **kwargs)

    def to_internal_value(self, data):
        try:
            for internal_validator in self.internal_validators:
                internal_validator(data)
            return self.get_queryset().get_or_create(**{self.slug_field: data})[0]
        except (TypeError, ValueError):
            self.fail("invalid")
