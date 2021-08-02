import enum
from dataclasses import dataclass
from typing import NamedTuple, List


@dataclass
class Field:
    dfield: str
    gofield: str
    orm: str
    valid: str

    def __repr__(self):
        return 'Field(%r, %r, %r, %r)' % (self.dfield, self.gofield, self.orm, self.valid)


class D2GField(Field, enum.Enum):
    AutoField = "AutoField", "uint32", "primaryKey", None
    BigAutoField = "BigAutoField", "uint64", "primaryKey", None
    BigIntegerField = "BigIntegerField", "int64", None, "numeric"
    BinaryField = "BinaryField", None, None, None
    BooleanField = "BooleanField", "bool", None, "eq=True|eq=False"
    CharField = "CharField", "string", "type:varchar(%(max_length)s)", None
    DateField = "DateField", "datatypes.Date", None, None
    DateTimeField = "DateTimeField", "time.Time", None, None
    DecimalField = "DecimalField", "float", None, None
    DurationField = "DurationField", None, None, None
    EmailField = "EmailField", "string", "type:varchar(254)", "email"
    FileField = "FileField", "string", "type:varchar(100)", None
    FilePathField = "FilePathField", "string", "type:varchar(100)", None
    FloatField = "FloatField", "float", None, None
    ImageField = "ImageField", "string", None, None
    IntegerField = "IntegerField", "int32", None, "numeric"
    GenericIPAddressField = "GenericIPAddressField", None, None, None
    JsonField = "JsonField", "datatypes.JSON", None, None
    NullBooleanField = "NullBooleanField", "bool", None, None
    PositiveBigIntegerField = "PositiveBigIntegerField", "uint64", "check:%(field_name)s>0", "numeric,gte=0"
    PositiveIntegerField = "PositiveIntegerField", "uint32", "check:%(field_name)s>0", "numeric,gte=0"
    PositiveSmallIntegerField = "PositiveSmallIntegerField", "uint16", "check:%(field_name)s>0", "numeric,gte=0"
    SlugField = "SlugField", "string", "type:varchar(50)", "numeric,gte=0"
    SmallAutoField = "SmallAutoField", "uint16", None, None
    SmallIntegerField = "SmallIntegerField", "int16", None, "numeric,gte=0"
    TextField = "TextField", "string", None, None
    TimeField = "TimeField", "time.Time", None, None
    URLField = "URLField", "string", "type:varchar(100)", None
    UUIDField = "UUIDField", "uuid.UUID", "type:uuid;default:uuid_generate_v4()", None

    ForeignKey = "ForeignKey", "%(foreign_model)s", "foreignKey:%(foreign_model_id)s", None
    ManyToOneRel = "ManyToOneRel", "%(foreign_model)s", "foreignKey:%(foreign_model_id)s", None

    ManyToManyField = "ManyToManyField", "[]*%(foreign_model)s", "many2many:%(m2m_db_table)s", None
    ManyToManyRel = "ManyToManyRel", "[]*%(foreign_model)s", "many2many:%(m2m_db_table)s", None

    OneToOneField = "OneToOneField", "%(foreign_model)s", "foreignKey:%(foreign_model_id)s", None
    OneToOneRel = "OneToOneRel", "%(foreign_model)s", "foreignKey:%(foreign_model_id)s", None


class DjangoField(enum.Enum):
    AutoField = "AutoField"
    BigAutoField = "BigAutoField"
    BigIntegerField = "BigIntegerField"
    BinaryField = "BinaryField"
    BooleanField = "BooleanField"
    CharField = "CharField"
    DateField = "DateField"
    DateTimeField = "DateTimeField"
    DecimalField = "DecimalField"
    DurationField = "DurationField"
    EmailField = "EmailField"
    FileField = "FileField"
    FilePathField = "FilePathField"
    FloatField = "FloatField"
    ImageField = "ImageField"
    IntegerField = "IntegerField"
    GenericIPAddressField = "GenericIPAddressField"
    JSONField = "JSONField"
    NullBooleanField = "NullBooleanField"
    PositiveBigIntegerField = "PositiveBigIntegerField"
    PositiveIntegerField = "PositiveIntegerField"
    PositiveSmallIntegerField = "PositiveSmallIntegerField"
    SlugField = "SlugField"
    SmallAutoField = "SmallAutoField"
    SmallIntegerField = "SmallIntegerField"
    TextField = "TextField"
    TimeField = "TimeField"
    URLField = "URLField"
    UUIDField = "UUIDField"
    CommaSeparatedIntegerField = "CommaSeparatedIntegerField"
    IPAddressField = "IPAddressField"


class KField(enum.Enum):
    # Integer types
    Short = "Short"
    Int = "Int"
    Long = "Long"

    # Floating point
    Float = "Float"
    Double = "Double"

    # Boolean
    Boolean = "Boolean"

    # String
    String = "String"

    # JSON
    Json = "Map<String, Object>"

    LocalDate = "LocalDate"
    LocalDateTime = "LocalDateTime"
    LocalTime = "LocalTime"

    # Byte Array
    ByteArray = "ByteArray"


class KValidation(enum.Enum):
    Noop = None
    EmailValidator = "EmailValidator"
    URLValidator = "URLValidator"
    IPValidator = "IPValidator"
    MinValidator = "MinValidator"
    MaxValidator = "MaxValidator"
    ChoiceValidator = "ChoiceValidator"

    def render(self):
        if self == KValidation.Noop:
            return
        else:
            return {
                KValidation.EmailValidator: "@Email",
                KValidation.URLValidator: "@URL"
            }[self]


class KGenerator(enum.Enum):
    Noop = None
    AutoGenerator = "AutoGenerator"
    UUIDGenerator = "UUIDGenerator"
    CREATE_DATETIME_GENERATOR = "CREATE_DATETIME_GENERATOR"
    MODIFY_DATETIME_GENERATOR = "MODIFY_DATETIME_GENERATOR"

    def render(self):
        if self == KGenerator.Noop:
            return
        else:
            return {
                KGenerator.AutoGenerator: "@GeneratedValue(strategy=GenerationType.IDENTITY)",
                KGenerator.UUIDGenerator: "@GeneratedValue(generator = \"uuid2\") "
                                          "@GenericGenerator(name = \"uuid2\", strategy = \"uuid2\")",
                KGenerator.CREATE_DATETIME_GENERATOR: "@CreationTimestamp",
                KGenerator.MODIFY_DATETIME_GENERATOR: "@UpdateTimestamp",

            }[self]


@dataclass
class BasicField:
    name: str
    nullable: bool
    field_class: str
    type: KField
    validation: [KValidation]
    generator: [KGenerator]


class M2MField(NamedTuple):
    name: str
    model: str
    db_table: str = ""
    column_id: str = ""
    reverse_column_id: str = ""
    reverse: bool = False
    reverse_field: str = None

    def __str__(self):
        return "name=%s - model=%s db_table=%s - column_id=%s - reverse_column_id=%s\
         - reverse=%s - reverse_field=%s" % (
            self.name, self.model, self.db_table, self.column_id,
            self.reverse_column_id, self.reverse, self.reverse_field
        )


class M2OField(NamedTuple):
    # M2O is never in reverse
    name: str
    model: str
    attname: str

    def __str__(self):
        return "name=%s - model=%s - attname=%s" % (
            self.name, self.model, self.attname
        )


class O2MField(NamedTuple):
    # O2M is always reversed
    name: str
    model: str
    reverse_field: str = None

    def __str__(self):
        return "name=%s - model=%s - reverse_field=%s" % (
            self.name, self.model, self.reverse_field
        )


class O2OField(NamedTuple):
    name: str
    model: str
    nullable: bool
    attname: str
    reverse: bool
    reverse_field: str = None

    def __str__(self):
        return "name=%s - model=%s - attname=%s reverse=%s - reverse_field=%s" % (
            self.name, self.model, self.attname, self.reverse, self.reverse_field
        )
