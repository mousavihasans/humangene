from django.core.exceptions import ValidationError
from django.db.models import SmallIntegerField
from django.utils.deconstruct import deconstructible

# Inspired by a gist that I don't remember the link XD
from rest_framework.fields import ChoiceField


@deconstructible
class IntEnumValidator:
    def __init__(self, enum):
        self.enum = enum

    def __call__(self, value):
        try:
            self.enum(value)
        except ValueError:
            raise ValidationError("%r is not a valid %s" % (value, self.enum.name))

    def __eq__(self, other):
        return isinstance(other, IntEnumValidator) and self.enum == other.enum


class IntEnumField(SmallIntegerField):
    """
    A simple Integer field that constrains its values to given IntEnum. I will simply works with Django admin.
    """
    def __init__(self, enum=None, *args, **kwargs):
        if enum is not None:
            # if check required for migrations (apparently)
            self.enum = enum
            kwargs["choices"] = tuple((m.value, m.name) for m in self.enum)
            kwargs["validators"] = [IntEnumValidator(self.enum)]
            if "default" in kwargs:
                kwargs["default"] = int(kwargs["default"])

        super().__init__(*args, **kwargs)

    # Don't convert integers fetched from DB to enum. It prevents Django admin from showing them in HTML selects.
    # Anyway you could say x.int_enum_field == MyEnum.value and it just works (because IntEnum will compare to int
    # as well).

    # def from_db_value(self, value, expression, connection, context):
    #     if value is not None:
    #         try:
    #             return self.enum(value)
    #         except ValueError:
    #             return value
    #     return value

class DrfIntEnumField(ChoiceField):
    default_error_messages = {
        'invalid': "No matching enum value."
    }

    def __init__(self, enum_class, **kwargs):
        self.enum_class = enum_class
        kwargs['choices'] = tuple((m.value, m.name) for m in enum_class)
        super().__init__(**kwargs)

    def to_internal_value(self, data):
        for choice in self.enum_class:
            if choice.name == data or choice.value == data:
                return choice
        self.fail('invalid')

    def to_representation(self, value):
        if value is None:
            return None
        if isinstance(value, int):
            return self.enum_class(value).name
        return value.name


class DrfIntEnumFieldMixin(object):
    """
    Mixin to add to your DRF ModelSerializers to use string representation of IntEnums instead of integer.
    """
    def build_standard_field(self, field_name, model_field):
        field_class, field_kwargs = super().build_standard_field(field_name, model_field)
        if isinstance(model_field, IntEnumField):
            field_class = DrfIntEnumField
            field_kwargs['enum_class'] = model_field.enum
        return field_class, field_kwargs

    # def build_field(self, field_name, info, model_class, nested_depth):
    #     r = super().build_field(field_name, info, model_class, nested_depth)
    #     return r
