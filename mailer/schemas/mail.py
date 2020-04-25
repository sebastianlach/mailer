from colander import SchemaNode, MappingSchema
from colander import String
from colander import Email, Length, All


class MailSchema(MappingSchema):
    content = SchemaNode(String())


class RecipientSchema(MappingSchema):
    name = SchemaNode(String(), validator=Length(0, 255), missing=None)
    address = SchemaNode(String(), validator=All(Email(), Length(0, 255)))
