from dataclasses import dataclass
from typing import List
from .cleaner import get_go_field_name
from .data import D2GField


@dataclass
class Field:
    name: str
    type: str
    orm: List[str]
    valid: List[str]


def render_go(struct, for_orm=True, for_validation=True) -> str:
    class_name = struct["class_name"]
    table = struct["model"]._meta.db_table
    go_code_fields = []

    for go_field, field in struct["fields"]:
        vname = get_go_field_name(field.name)
        vtype = go_field.gofield

        if go_field.orm:
            orm_tags = [go_field.orm]
        else:
            orm_tags = []

        if go_field.valid:
            valid_tags = [go_field.valid]
        else:
            valid_tags = []

        # print("-------------->> ", repr(go_field), field)

        if go_field == D2GField.ManyToOneRel:
            continue

        if go_field == D2GField.ManyToManyRel:
            vname = "%ss" % vname
            vtype = vtype % {'foreign_model': field.related_model._meta.model_name.title()}
            orm_tags[0] = orm_tags[0] % {'m2m_db_table': field.field.m2m_db_table()}

        if go_field == D2GField.ManyToManyField:
            vtype = vtype % {'foreign_model': field.related_model._meta.model_name.title()}
            orm_tags[0] = orm_tags[0] % {'m2m_db_table': field.m2m_db_table()}

        if go_field == D2GField.OneToOneRel:
            continue

        if go_field == D2GField.OneToOneField:
            vtype = vtype % {'foreign_model': field.related_model._meta.model_name.title()}
            orm_tags[0] = orm_tags[0] % {'foreign_model_id': get_go_field_name(field.column)}
            delete_behavior = field.deconstruct()[3]['on_delete'].__name__.replace("_", " ")
            orm_tags.append("constraint:OnDelete:%s" % delete_behavior)
            fk_field = '{:20s} {:25s} {:20s} '.format(
                get_go_field_name(field.column),
                "uint32",
                '`gorm:"index;unique"`'
            )
            # print(fk_field)
            go_code_fields.append(fk_field)

        if go_field == D2GField.ForeignKey:
            vtype = vtype % {'foreign_model': field.related_model._meta.object_name}
            orm_tags[0] = orm_tags[0] % {'foreign_model_id': get_go_field_name(field.column)}
            delete_behavior = field.deconstruct()[3]['on_delete'].__name__.replace("_", " ")
            orm_tags.append("constraint:OnDelete:%s" % delete_behavior)
            if for_orm:
                fk_field = '{:20s} {:25s} {:20s} '.format(
                    get_go_field_name(field.column),
                    "uint32",
                    '`gorm:"index"`'
                )
                # print(fk_field)
                go_code_fields.append(fk_field)

        if go_field == D2GField.CharField:
            orm_tags[0] = orm_tags[0] % {'max_length': field.max_length}
            valid_tags.append("max=%s" % field.max_length)

        if go_field.dfield.lower().find("positive") != -1:
            orm_tags[0] = orm_tags[0] % {'field_name': field.column}

        if not field.null:
           orm_tags.append("not null")

        if getattr(field, 'db_index', None) and field.db_index:
            orm_tags.append("index")

        if getattr(field, 'unique', None) and field.unique:
            orm_tags.append("unique")

        if getattr(field, 'blank', None) and not field.blank:
            valid_tags.append("required")

        if orm_tags and for_orm:
            vorm_tags = 'gorm:"%s"' % ";".join(orm_tags)
        else:
            vorm_tags = ""

        if valid_tags and for_validation:
            vvalid_tags = 'validate:"%s"' % ";".join(valid_tags)
        else:
            vvalid_tags = ""

        if vorm_tags or vvalid_tags:
            all_tags = "`%s`" % " ".join([i for i in [vorm_tags, vvalid_tags] if i])
        else:
            all_tags = ""

        field_verbose = '{:25s} {:12s} {:1s}'.format(vname, vtype, all_tags)

        # print(field_verbose)
        go_code_fields.append(field_verbose)


    code = """
type %(class_name)s struct {
%(fields)s
}

func(%(class_name)s) TableName() string {
    return "%(table)s"
}
""" % {
        "class_name": class_name,
        "table": table,
        "fields": "\n".join([
            "    %s" % f
            for f in go_code_fields
        ])
    }

    return code


def render_java(c) -> str:
    s = list()
    s.append("@Entity")
    s.append("class %s (" % c["class_name"])

    for p in c["primitive_fields"]:
        s.append("")
        if p.nullable:
            s.append("    @Column(nullable=true)")
        else:
            s.append("    @NotNull")

        for v in p.generator:
            if v.render():
                s.append("    %s" % v.render())
        for v in p.validation:
            if v.render():
                s.append("    %s" % v.render())
        s.append("    var %s: %s," % (p.name, p.type.name))

    for p in c["o2o_fields"]:
        s.append("")
        if p.nullable:
            s.append("    @Column(nullable=true)")
        else:
            s.append("    @NotNull")

        if p.reverse:
            s.append("    @OneToOne(mappedBy=\"%s\")" % p.reverse_field)
        else:
            s.append("    @OneToOne")
            s.append("    @JoinColumn(name=\"%s\")" % p.attname)

        s.append("    var %s: %s," % (p.name, p.model.__name__))

    for p in c["m2o_fields"]:
        s.append("")
        s.append("    @ManyToOne")
        s.append("    @JoinColumn(name=\"%s\")" % p.attname)
        s.append("    var %s: %s," % (p.name, p.model.__name__))

    for p in c["o2m_fields"]:
        s.append("")
        s.append("    @OneToMany(mappedBy=\"%s\")" % p.reverse_field)
        s.append("    var %s: List<%s>," % (p.name, p.model.__name__))

    for p in c["m2m_fields"]:
        s.append("")
        if p.reverse:
            s.append("    @ManyToMany(mappedBy=\"%s\")" % p.reverse_field)
            s.append("    var %s: List<%s>," % (p.name, p.model.__name__))
        else:
            s.append("    @ManyToMany")
            s.append("    @JoinTable(")
            s.append("        name= \"%s\"" % p.db_table)
            s.append("        joinColumns= @JoinColumn(name=\"%s\")" % p.column_id)
            s.append("        inverseJoinColumns= @JoinColumn(name=\"%s\")" % p.reverse_column_id)
            s.append("    )")
            s.append("    var %s: List<%s>," % (p.name, p.model.__name__))

    s.append(")")

    return "\n".join(s)
