from zope.component.interfaces import ObjectEvent


class ObjectSharingModifiedEvent(ObjectEvent):
    
    def __init__(self, object, user_roles):
        super(ObjectSharingModifiedEvent, self).__init__(object)
        self.user_roles = user_roles
