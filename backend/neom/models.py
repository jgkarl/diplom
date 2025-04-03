from neomodel import (
    StructuredNode,
    StringProperty,
    RelationshipTo,
    UniqueIdProperty,
)

class PersonNode(StructuredNode):
    uuid =  UniqueIdProperty()
    first_name = StringProperty(max_length=255, null=False)
    last_name = StringProperty(max_length=255, null=False)
    birth = StringProperty(max_length=10, null=True)

class BookNode(StructuredNode):
    uuid = UniqueIdProperty()
    title = StringProperty(max_length=500, null=False)
    token = StringProperty(max_length=64, null=True, blank=True)
    published = StringProperty(max_length=10, null=True, blank=True)
    
    # Relations : book has many authors and many supervisors - one supervisor can have many books
    authors = RelationshipTo('PersonNode', 'AUTHORED_BY')
    supervisors = RelationshipTo('PersonNode', 'SUPERVISED_BY')
    
