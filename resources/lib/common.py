# -*- coding: utf-8 -*-

import datetime, time
import xbmc

def log_notice(msg=''):
    xbmc.log(smart_utf8(msg), xbmc.LOGNOTICE)

def log_error(msg=''):
    xbmc.log(smart_utf8(msg), xbmc.LOGERROR)

def notify(msg=''):
    xbmc.executebuiltin('XBMC.Notification(%s,%s,3000)' % ('Photos Viewer', smart_utf8(msg)))

def smart_unicode(s):
    """credit : sfaxman"""
    if not s:
    	return ''
    try:
    	if not isinstance(s, basestring):
    	    if hasattr(s, '__unicode__'):
    		s = unicode(s)
    	    else:
    		s = unicode(str(s), 'UTF-8')
    	elif not isinstance(s, unicode):
    	    s = unicode(s, 'UTF-8')
    except:
    	if not isinstance(s, basestring):
    	    if hasattr(s, '__unicode__'):
    		s = unicode(s)
    	    else:
    		s = unicode(str(s), 'ISO-8859-1')
    	elif not isinstance(s, unicode):
    	    s = unicode(s, 'ISO-8859-1')
    return s

def smart_utf8(s):
    return smart_unicode(s).encode('utf-8')

def set_view(mode=None):
    skin_used = xbmc.getSkinDir()
    if skin_used == 'skin.mimic':
        if mode == 'thumbnail':
            mode = 52
        elif mode == 'picture':
            mode = 510
        elif mode == 'list':
            mode = 50
    if mode:
        xbmc.executebuiltin("Container.SetViewMode(%d)" % (mode))

def convert_timestamp(timestamp, date_format='%Y-%m-%d %H:%M'):
    t = datetime.datetime.fromtimestamp(int(timestamp))
    t = t.replace(year=t.year+31)
    return t.strftime(date_format)
