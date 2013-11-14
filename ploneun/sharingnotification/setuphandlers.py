from collective.grok import gs
from ploneun.sharingnotification import MessageFactory as _

@gs.importstep(
    name=u'ploneun.sharingnotification', 
    title=_('ploneun.sharingnotification import handler'),
    description=_(''))
def setupVarious(context):
    if context.readDataFile('ploneun.sharingnotification.marker.txt') is None:
        return
    portal = context.getSite()

    # do anything here
