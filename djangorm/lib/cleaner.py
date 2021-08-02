from typing import List
from django.apps import apps
from .data import (
    KGenerator, KValidation, KField, DjangoField as DJ,
)


def get_field_generator(f) -> List[KGenerator]:
    ftype = DJ(f.get_internal_type())
    _allowed_list = [
        DJ.AutoField,
        DJ.BigAutoField,
        DJ.SmallAutoField,
        DJ.UUIDField,
        DJ.DateTimeField,
    ]

    if ftype not in _allowed_list:
        return [KGenerator.Noop]

    if ftype == DJ.DateTimeField:
        if f.auto_now:
            return [KGenerator.CREATE_DATETIME_GENERATOR]
        elif f.auto_now_add:
            return [KGenerator.MODIFY_DATETIME_GENERATOR]
        else:
            return [KGenerator.Noop]

    field_type_map = {
        DJ.AutoField: [KGenerator.AutoGenerator],
        DJ.BigAutoField: [KGenerator.AutoGenerator],
        DJ.SmallAutoField: [KGenerator.AutoGenerator],
        DJ.UUIDField: [KGenerator.UUIDGenerator],
    }
    return field_type_map[ftype]


def get_field_validation(f) -> [KValidation]:
    ftype = DJ(f.get_internal_type())
    field_type_map = {
        DJ.URLField: [KValidation.URLValidator],
        DJ.EmailField: [KValidation.EmailValidator],
        DJ.FloatField: [KValidation.EmailValidator],
        DJ.IPAddressField: [KValidation.IPValidator],
    }
    return field_type_map.get(ftype, [KValidation.Noop])


def get_field_type(f) -> KField:
    ftype = DJ(f.get_internal_type())
    field_type_map = {
        DJ.AutoField: KField.Int,
        DJ.BigAutoField: KField.Long,
        DJ.BigIntegerField: KField.Long,
        DJ.BinaryField: KField.ByteArray,
        DJ.BooleanField: KField.Boolean,
        DJ.CharField: KField.String,
        DJ.DateField: KField.LocalDate,
        DJ.DateTimeField: KField.LocalDateTime,
        DJ.DecimalField: KField.Double,
        DJ.DurationField: KField.String,
        DJ.EmailField: KField.String,
        DJ.FileField: KField.String,
        DJ.FilePathField: KField.String,
        DJ.FloatField: KField.Float,
        DJ.ImageField: KField.String,
        DJ.IntegerField: KField.String,
        DJ.GenericIPAddressField: KField.String,
        DJ.JSONField: KField.Json,
        DJ.NullBooleanField: KField.Boolean,
        DJ.PositiveBigIntegerField: KField.Int,
        DJ.PositiveIntegerField: KField.Int,
        DJ.PositiveSmallIntegerField: KField.Int,
        DJ.SlugField: KField.String,
        DJ.SmallAutoField: KField.Short,
        DJ.SmallIntegerField: KField.Int,
        DJ.TextField: KField.String,
        DJ.TimeField: KField.LocalTime,
        DJ.URLField: KField.String,
        DJ.UUIDField: KField.String,
        DJ.CommaSeparatedIntegerField: KField.String,
        DJ.IPAddressField: KField.String,
    }
    return field_type_map[ftype]


def get_java_field_name(fname):
    _jname = "".join([f.capitalize() for f in fname.split("_")])
    return "%s%s" % (_jname[0].lower(), _jname[1:])


def get_go_field_name(fname):
    return "".join([f.capitalize() for f in fname.split("_")])


def get_models(app_names):
    return [
        (m._meta.app_label, m)
        for m in apps.get_models()
        if any([m._meta.app_label == aname for aname in app_names])
    ]


def is_field_reversed(field):
    return field.__class__.__name__.endswith("Rel")
