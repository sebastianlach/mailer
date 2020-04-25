from colander import SchemaNode, MappingSchema
from colander import String
from colander import Email, Length, All
from colander import drop


class MailSchema(MappingSchema):
    content = SchemaNode(String())
    name = SchemaNode(String(), validator=Length(0, 255), missing=drop)
    address = SchemaNode(
        String(),
        validator=All(Email(), Length(0, 255)),
        missing=drop,
    )


class RecipientSchema(MappingSchema):
    name = SchemaNode(String(), validator=Length(0, 255), missing=drop)
    address = SchemaNode(String(), validator=All(Email(), Length(0, 255)))
