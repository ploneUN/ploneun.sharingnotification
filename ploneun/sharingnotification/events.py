from zope.component.interfaces import ObjectEvent
from zope.interface import implements
from ploneun.sharingnotification.interfaces import IObjectSharingModifiedEvent

class ObjectSharingModifiedEvent(ObjectEvent):
    implements(IObjectSharingModifiedEvent)

    def __init__(self, object, user_roles):
        super(ObjectSharingModifiedEvent, self).__init__(object)
        self.user_roles = user_roles
