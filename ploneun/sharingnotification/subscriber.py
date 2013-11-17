from five import grok
from ploneun.sharingnotification.interfaces import IObjectSharingModifiedEvent
from ploneun.sharingnotification.interfaces import IProductSpecific
from Products.CMFCore.interfaces import IContentish
from zope.globalrequest import getRequest
from zope.component.hooks import getSite
from email import message_from_string


ROLE_TITLE={
    'Contributor': 'Can Add',
    'Editor': 'Can Edit',
    'Reviewer': 'Can Review',
    'Reader': 'Can View'
}

@grok.subscribe(IContentish, IObjectSharingModifiedEvent)
def mail_notification(obj, event):
    request = getRequest()
    if not IProductSpecific.providedBy(request):
        return
    mtool = obj.portal_membership
    sharer = mtool.getAuthenticatedMember()
    sharerdata = {
        'fullname': sharer.getProperty('fullname') or sharer.getId(),
        'email': sharer.getProperty('email'),
    }
    site = getSite()

    encoding = site.getProperty('email_charset', 'utf-8')

    for userid in event.user_roles:
        new_roles = event.user_roles[userid]['to_assign']
        if 'Owner' in new_roles:
            new_roles.remove('Owner')
        if not new_roles:
            continue
        user = mtool.getMemberById(userid)
        userdata = {
            'fullname': user.getProperty('fullname') or userid,
            'email': user.getProperty('email'),
        }

        type_title = site.portal_types[obj.portal_type].Title()

        permissions = [ROLE_TITLE[r] for r in new_roles]

        mail_text = obj.ploneun_sharingnotification_email(
            user=userdata,
            portal=site,
            sharer=sharerdata,
            charset=encoding,
            item_type=type_title,
            permissions=permissions
        )

        message_obj = message_from_string(mail_text)
        mTo = message_obj['To']
        mFrom = message_obj['From']
        subject = message_obj['Subject']

        site.MailHost.send(mail_text, mTo, mFrom, subject=subject,
                        charset=encoding)
