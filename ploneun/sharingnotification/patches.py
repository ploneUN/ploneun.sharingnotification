import logging

logger = logging.getLogger('ploneun.sharingnotification')

def _patch_role_settings_updated_event():
    try:
        from plone.app.workflow.browser.sharing import SharingView
    except ImportError:
        return

    if getattr(SharingView, '__ploneun_role_settings_updated', False):
        return 

    logger.info('Patching SharingView with role update event')

    from ploneun.sharingnotification.events import ObjectSharingModifiedEvent
    from zope.event import notify

    _orig_update_role_settings = SharingView.update_role_settings

    def update_role_settings(self, new_settings, reindex=True):

        managed_roles = frozenset([r['id'] for r in self.roles()])
        context = self.context
        user_roles = {}

        for s in new_settings:
            user_id = s['id']

            existing_roles = frozenset(context.get_local_roles_for_userid(userid=user_id))
            selected_roles = frozenset(s['roles'])

            relevant_existing_roles = managed_roles & existing_roles

            if relevant_existing_roles == selected_roles:
                continue

            # We will remove those roles that we are managing and which set
            # on the context, but which were not selected
            to_remove = relevant_existing_roles - selected_roles

            # Leaving us with the selected roles, less any roles that we
            # want to remove
            wanted_roles = (selected_roles | existing_roles) - to_remove

            to_assign = [r for r in wanted_roles if (
                r not in relevant_existing_roles)]
            user_roles[user_id] = {
                'to_remove': to_remove,
                'to_assign': to_assign,
                'old_roles': relevant_existing_roles,
                'new_roles': selected_roles
            }

        event = ObjectSharingModifiedEvent(self.context, user_roles)
        result = _orig_update_role_settings(self, new_settings, reindex)
        notify(event)
        return result

    SharingView.update_role_settings = update_role_settings

_patch_role_settings_updated_event()
