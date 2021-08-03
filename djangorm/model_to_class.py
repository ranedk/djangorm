from .lib.data import (
    BasicField, M2MField, M2OField,
    O2OField, O2MField, D2GField
)
from .lib.cleaner import (
    get_java_field_name, get_field_validation, get_field_generator,
    get_field_type, get_models,
    is_field_reversed
)
from .lib.render import render_go, render_java


def get_struct_structure(app_name, model):
    return {
        "class_name": model.__name__,
        "model": model,
        "fields": [
            (D2GField[f.__class__.__name__], f)
            for f in model._meta.get_fields()
        ]
    }


def get_class_structure(app_name, model):
    class_name = model.__name__
    _all_fields = model._meta.get_fields()

    basic_fields = [f for f in _all_fields if not f.is_relation]
    _m2m_fields = [f for f in _all_fields if f.many_to_many]
    _o2m_fields = [f for f in _all_fields if f.one_to_many]
    _m2o_fields = [f for f in _all_fields if f.many_to_one]
    _o2o_fields = [f for f in _all_fields if f.one_to_one]

    primitive_fields = []
    for b in basic_fields:
        primitive_fields.append(BasicField(
            get_java_field_name(b.name),
            b.null,
            b.__class__.__name__,
            get_field_type(b),
            get_field_validation(b),
            get_field_generator(b)
        ))

    o2o_fields = []
    for _field in _o2o_fields:
        if is_field_reversed(_field):
            o2o_fields.append(
                O2OField(
                    _field.name, _field.related_model, _field.null, None, True, _field.field.name
                )
            )
        else:
            o2o_fields.append(O2OField(_field.name, _field.related_model, _field.null, _field.attname, False))

    m2o_fields = []
    for _field in _m2o_fields:
        if getattr(_field, "attname", None):     # Generic Foreign Key fails this test
            m2o_fields.append(M2OField(_field.name, _field.related_model, _field.attname))

    o2m_fields = []
    for _field in _o2m_fields:
        o2m_fields.append(O2MField(_field.get_accessor_name(), _field.related_model, _field.name))

    m2m_fields = []
    for _field in _m2m_fields:
        if is_field_reversed(_field):
            m2m_fields.append(M2MField(
                name=_field.get_accessor_name(),
                model=_field.related_model,
                reverse=True,
                reverse_field=_field.field.name))
        else:
            m2m_fields.append(M2MField(
                name=_field.name,
                model=_field.related_model,
                db_table=_field.m2m_db_table(),
                column_id=_field.m2m_column_name(),
                reverse_column_id=_field.m2m_reverse_name(),
            ))

    # print("\n\n------------------", class_name, "---------------")
    # print("O2O\n", o2o_fields, "\n")
    # print("M2O\n", m2o_fields, "\n")
    # print("O2M\n", o2m_fields, "\n")
    # print("M2M\n", m2m_fields, "\n")

    return {
        'app_name': app_name,
        'class_name': class_name,
        'primitive_fields': primitive_fields,
        'm2m_fields': m2m_fields,
        'm2o_fields': m2o_fields,
        'o2m_fields': o2m_fields,
        'o2o_fields': o2o_fields
    }


def convert_models(apps, lang, for_orm=True, for_validation=True):
    if lang == "go":
        convert_models_to_gorm(apps, for_orm, for_validation)
    if lang == "java":
        convert_models_to_java(apps)


def convert_models_to_java(apps):
    """
    Function to convert Django models into kotlin classes.
    :param apps: Apps for which the models are to be converted to kotlin classes
    :return: None (print out the kotlin classes)
    """
    models = get_models(apps)
    for app, model in models:
        class_structure = get_class_structure(app, model)
        print(render_java(class_structure))


def convert_models_to_gorm(apps, for_orm=True, for_validation=True):
    """
    Function to convert Django models into kotlin classes.
    :param apps: Apps for which the models are to be converted to kotlin classes
    :return: None (print out the gorm struct)
    """
    code = ""
    models = get_models(apps)
    for app, model in models:
        struct = get_struct_structure(app, model)
        # import pprint
        # pprint.pprint(struct)
        code += render_go(struct, for_orm, for_validation)
    print(code)
