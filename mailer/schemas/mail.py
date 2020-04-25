from colander import SchemaNode, MappingSchema, String


class MailSchema(MappingSchema):
    content = SchemaNode(String())
