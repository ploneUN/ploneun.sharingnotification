from zope.interface import Interface
from zope.component.interfaces import IObjectEvent
class IProductSpecific(Interface):
    pass

class IObjectSharingModifiedEvent(IObjectEvent):
    pass
