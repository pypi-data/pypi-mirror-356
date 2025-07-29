from plone.app.z3cform.interfaces import IPloneFormLayer
from z3c.form.interfaces import IMultiWidget
from zope.schema.interfaces import IObject
from zope.schema.interfaces import ValidationError


class IDataGridFieldLayer(IPloneFormLayer):
    """Marker interface that defines a browser layer."""


class IDataGridFieldWidget(IMultiWidget):
    """Grid widget."""


class AttributeNotFoundError(ValidationError):
    """An attribute is missing from the class"""

    def __init__(self, fieldname, schema):
        self.fieldname = fieldname
        self.schema = schema
        self.__doc__ = "Missing Field {} required by schema {}".format(
            fieldname, schema
        )


class IRow(IObject):
    """A row. The schema defines dict keys."""
