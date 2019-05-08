# -*- coding: utf-8 -*-

import os, inspect
import xbmc, xbmcaddon

def notify(*messages, **options):
    log(messages, error=options.get('error', False))
    time = options.get('time', 10000)
    image = options.get('image', None)
    if image is None:
        if options.get('error', False):
            image = 'DefaultIconError.png'
        else:
            image = 'DefaultIconInfo.png'
    m = []
    for message in messages:
        if isinstance(message, str):
            m.append(message)
        elif isinstance(message, unicode):
            m.append(message.encode('utf-8'))
        else:
            m.append(str(message))
    xbmc.executebuiltin('Notification("%s","%s",%d,"%s")' % (xbmcaddon.Addon().getAddonInfo('name'),str(' ').join(m),time,image))

def log(*messages, **options):
    addon = xbmcaddon.Addon()
    if options.get('error', False):
        level = xbmc.LOGERROR
    elif addon.getSetting('debug') == 'true':
        level = xbmc.LOGNOTICE
    else:
        level = None
    if level:
        m = []
        for message in messages:
            if isinstance(message, str):
                m.append(message)
            elif isinstance(message, unicode):
                m.append(message.encode('utf-8'))
            else:
                m.append(str(message))
        frame = inspect.currentframe(1)
        xbmc.log(str('%s: %s(%d): %s: %s') % (addon.getAddonInfo('id'), os.path.basename(frame.f_code.co_filename), frame.f_lineno, frame.f_code.co_name, str(' ').join(m)), level)

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

def isholiday(day):
    holidays = {
        "1950-01-01":True,
        "1950-01-15":True,
        "1950-03-21":True,
        "1950-04-29":True,
        "1950-05-03":True,
        "1950-05-05":True,
        "1950-09-23":True,
        "1950-11-03":True,
        "1950-11-23":True,
        "1951-01-01":True,
        "1951-01-15":True,
        "1951-03-21":True,
        "1951-04-29":True,
        "1951-05-03":True,
        "1951-05-05":True,
        "1951-09-24":True,
        "1951-11-03":True,
        "1951-11-23":True,
        "1952-01-01":True,
        "1952-01-15":True,
        "1952-03-21":True,
        "1952-04-29":True,
        "1952-05-03":True,
        "1952-05-05":True,
        "1952-09-23":True,
        "1952-11-03":True,
        "1952-11-23":True,
        "1953-01-01":True,
        "1953-01-15":True,
        "1953-03-21":True,
        "1953-04-29":True,
        "1953-05-03":True,
        "1953-05-05":True,
        "1953-09-23":True,
        "1953-11-03":True,
        "1953-11-23":True,
        "1954-01-01":True,
        "1954-01-15":True,
        "1954-03-21":True,
        "1954-04-29":True,
        "1954-05-03":True,
        "1954-05-05":True,
        "1954-09-23":True,
        "1954-11-03":True,
        "1954-11-23":True,
        "1955-01-01":True,
        "1955-01-15":True,
        "1955-03-21":True,
        "1955-04-29":True,
        "1955-05-03":True,
        "1955-05-05":True,
        "1955-09-24":True,
        "1955-11-03":True,
        "1955-11-23":True,
        "1956-01-01":True,
        "1956-01-15":True,
        "1956-03-21":True,
        "1956-04-29":True,
        "1956-05-03":True,
        "1956-05-05":True,
        "1956-09-23":True,
        "1956-11-03":True,
        "1956-11-23":True,
        "1957-01-01":True,
        "1957-01-15":True,
        "1957-03-21":True,
        "1957-04-29":True,
        "1957-05-03":True,
        "1957-05-05":True,
        "1957-09-23":True,
        "1957-11-03":True,
        "1957-11-23":True,
        "1958-01-01":True,
        "1958-01-15":True,
        "1958-03-21":True,
        "1958-04-29":True,
        "1958-05-03":True,
        "1958-05-05":True,
        "1958-09-23":True,
        "1958-11-03":True,
        "1958-11-23":True,
        "1959-01-01":True,
        "1959-01-15":True,
        "1959-03-21":True,
        "1959-04-10":True,
        "1959-04-29":True,
        "1959-05-03":True,
        "1959-05-05":True,
        "1959-09-24":True,
        "1959-11-03":True,
        "1959-11-23":True,
        "1960-01-01":True,
        "1960-01-15":True,
        "1960-03-20":True,
        "1960-04-29":True,
        "1960-05-03":True,
        "1960-05-05":True,
        "1960-09-23":True,
        "1960-11-03":True,
        "1960-11-23":True,
        "1961-01-01":True,
        "1961-01-15":True,
        "1961-03-21":True,
        "1961-04-29":True,
        "1961-05-03":True,
        "1961-05-05":True,
        "1961-09-23":True,
        "1961-11-03":True,
        "1961-11-23":True,
        "1962-01-01":True,
        "1962-01-15":True,
        "1962-03-21":True,
        "1962-04-29":True,
        "1962-05-03":True,
        "1962-05-05":True,
        "1962-09-23":True,
        "1962-11-03":True,
        "1962-11-23":True,
        "1963-01-01":True,
        "1963-01-15":True,
        "1963-03-21":True,
        "1963-04-29":True,
        "1963-05-03":True,
        "1963-05-05":True,
        "1963-09-24":True,
        "1963-11-03":True,
        "1963-11-23":True,
        "1964-01-01":True,
        "1964-01-15":True,
        "1964-03-20":True,
        "1964-04-29":True,
        "1964-05-03":True,
        "1964-05-05":True,
        "1964-09-23":True,
        "1964-11-03":True,
        "1964-11-23":True,
        "1965-01-01":True,
        "1965-01-15":True,
        "1965-03-21":True,
        "1965-04-29":True,
        "1965-05-03":True,
        "1965-05-05":True,
        "1965-09-23":True,
        "1965-11-03":True,
        "1965-11-23":True,
        "1966-01-01":True,
        "1966-01-15":True,
        "1966-03-21":True,
        "1966-04-29":True,
        "1966-05-03":True,
        "1966-05-05":True,
        "1966-09-15":True,
        "1966-09-23":True,
        "1966-10-10":True,
        "1966-11-03":True,
        "1966-11-23":True,
        "1967-01-01":True,
        "1967-01-15":True,
        "1967-02-11":True,
        "1967-03-21":True,
        "1967-04-29":True,
        "1967-05-03":True,
        "1967-05-05":True,
        "1967-09-15":True,
        "1967-09-24":True,
        "1967-10-10":True,
        "1967-11-03":True,
        "1967-11-23":True,
        "1968-01-01":True,
        "1968-01-15":True,
        "1968-02-11":True,
        "1968-03-20":True,
        "1968-04-29":True,
        "1968-05-03":True,
        "1968-05-05":True,
        "1968-09-15":True,
        "1968-09-23":True,
        "1968-10-10":True,
        "1968-11-03":True,
        "1968-11-23":True,
        "1969-01-01":True,
        "1969-01-15":True,
        "1969-02-11":True,
        "1969-03-21":True,
        "1969-04-29":True,
        "1969-05-03":True,
        "1969-05-05":True,
        "1969-09-15":True,
        "1969-09-23":True,
        "1969-10-10":True,
        "1969-11-03":True,
        "1969-11-23":True,
        "1970-01-01":True,
        "1970-01-15":True,
        "1970-02-11":True,
        "1970-03-21":True,
        "1970-04-29":True,
        "1970-05-03":True,
        "1970-05-05":True,
        "1970-09-15":True,
        "1970-09-23":True,
        "1970-10-10":True,
        "1970-11-03":True,
        "1970-11-23":True,
        "1971-01-01":True,
        "1971-01-15":True,
        "1971-02-11":True,
        "1971-03-21":True,
        "1971-04-29":True,
        "1971-05-03":True,
        "1971-05-05":True,
        "1971-09-15":True,
        "1971-09-24":True,
        "1971-10-10":True,
        "1971-11-03":True,
        "1971-11-23":True,
        "1972-01-01":True,
        "1972-01-15":True,
        "1972-02-11":True,
        "1972-03-20":True,
        "1972-04-29":True,
        "1972-05-03":True,
        "1972-05-05":True,
        "1972-09-15":True,
        "1972-09-23":True,
        "1972-10-10":True,
        "1972-11-03":True,
        "1972-11-23":True,
        "1973-01-01":True,
        "1973-01-15":True,
        "1973-02-11":True,
        "1973-03-21":True,
        "1973-04-29":True,
        "1973-04-30":True,
        "1973-05-03":True,
        "1973-05-05":True,
        "1973-09-15":True,
        "1973-09-23":True,
        "1973-09-24":True,
        "1973-10-10":True,
        "1973-11-03":True,
        "1973-11-23":True,
        "1974-01-01":True,
        "1974-01-15":True,
        "1974-02-11":True,
        "1974-03-21":True,
        "1974-04-29":True,
        "1974-05-03":True,
        "1974-05-05":True,
        "1974-05-06":True,
        "1974-09-15":True,
        "1974-09-16":True,
        "1974-09-23":True,
        "1974-10-10":True,
        "1974-11-03":True,
        "1974-11-04":True,
        "1974-11-23":True,
        "1975-01-01":True,
        "1975-01-15":True,
        "1975-02-11":True,
        "1975-03-21":True,
        "1975-04-29":True,
        "1975-05-03":True,
        "1975-05-05":True,
        "1975-09-15":True,
        "1975-09-24":True,
        "1975-10-10":True,
        "1975-11-03":True,
        "1975-11-23":True,
        "1975-11-24":True,
        "1976-01-01":True,
        "1976-01-15":True,
        "1976-02-11":True,
        "1976-03-20":True,
        "1976-04-29":True,
        "1976-05-03":True,
        "1976-05-05":True,
        "1976-09-15":True,
        "1976-09-23":True,
        "1976-10-10":True,
        "1976-10-11":True,
        "1976-11-03":True,
        "1976-11-23":True,
        "1977-01-01":True,
        "1977-01-15":True,
        "1977-02-11":True,
        "1977-03-21":True,
        "1977-04-29":True,
        "1977-05-03":True,
        "1977-05-05":True,
        "1977-09-15":True,
        "1977-09-23":True,
        "1977-10-10":True,
        "1977-11-03":True,
        "1977-11-23":True,
        "1978-01-01":True,
        "1978-01-02":True,
        "1978-01-15":True,
        "1978-01-16":True,
        "1978-02-11":True,
        "1978-03-21":True,
        "1978-04-29":True,
        "1978-05-03":True,
        "1978-05-05":True,
        "1978-09-15":True,
        "1978-09-23":True,
        "1978-10-10":True,
        "1978-11-03":True,
        "1978-11-23":True,
        "1979-01-01":True,
        "1979-01-15":True,
        "1979-02-11":True,
        "1979-02-12":True,
        "1979-03-21":True,
        "1979-04-29":True,
        "1979-04-30":True,
        "1979-05-03":True,
        "1979-05-05":True,
        "1979-09-15":True,
        "1979-09-24":True,
        "1979-10-10":True,
        "1979-11-03":True,
        "1979-11-23":True,
        "1980-01-01":True,
        "1980-01-15":True,
        "1980-02-11":True,
        "1980-03-20":True,
        "1980-04-29":True,
        "1980-05-03":True,
        "1980-05-05":True,
        "1980-09-15":True,
        "1980-09-23":True,
        "1980-10-10":True,
        "1980-11-03":True,
        "1980-11-23":True,
        "1980-11-24":True,
        "1981-01-01":True,
        "1981-01-15":True,
        "1981-02-11":True,
        "1981-03-21":True,
        "1981-04-29":True,
        "1981-05-03":True,
        "1981-05-04":True,
        "1981-05-05":True,
        "1981-09-15":True,
        "1981-09-23":True,
        "1981-10-10":True,
        "1981-11-03":True,
        "1981-11-23":True,
        "1982-01-01":True,
        "1982-01-15":True,
        "1982-02-11":True,
        "1982-03-21":True,
        "1982-03-22":True,
        "1982-04-29":True,
        "1982-05-03":True,
        "1982-05-05":True,
        "1982-09-15":True,
        "1982-09-23":True,
        "1982-10-10":True,
        "1982-10-11":True,
        "1982-11-03":True,
        "1982-11-23":True,
        "1983-01-01":True,
        "1983-01-15":True,
        "1983-02-11":True,
        "1983-03-21":True,
        "1983-04-29":True,
        "1983-05-03":True,
        "1983-05-05":True,
        "1983-09-15":True,
        "1983-09-23":True,
        "1983-10-10":True,
        "1983-11-03":True,
        "1983-11-23":True,
        "1984-01-01":True,
        "1984-01-02":True,
        "1984-01-15":True,
        "1984-01-16":True,
        "1984-02-11":True,
        "1984-03-20":True,
        "1984-04-29":True,
        "1984-04-30":True,
        "1984-05-03":True,
        "1984-05-05":True,
        "1984-09-15":True,
        "1984-09-23":True,
        "1984-09-24":True,
        "1984-10-10":True,
        "1984-11-03":True,
        "1984-11-23":True,
        "1985-01-01":True,
        "1985-01-15":True,
        "1985-02-11":True,
        "1985-03-21":True,
        "1985-04-29":True,
        "1985-05-03":True,
        "1985-05-05":True,
        "1985-05-06":True,
        "1985-09-15":True,
        "1985-09-16":True,
        "1985-09-23":True,
        "1985-10-10":True,
        "1985-11-03":True,
        "1985-11-04":True,
        "1985-11-23":True,
        "1986-01-01":True,
        "1986-01-15":True,
        "1986-02-11":True,
        "1986-03-21":True,
        "1986-04-29":True,
        "1986-05-03":True,
        "1986-05-05":True,
        "1986-09-15":True,
        "1986-09-23":True,
        "1986-10-10":True,
        "1986-11-03":True,
        "1986-11-23":True,
        "1986-11-24":True,
        "1987-01-01":True,
        "1987-01-15":True,
        "1987-02-11":True,
        "1987-03-21":True,
        "1987-04-29":True,
        "1987-05-03":True,
        "1987-05-04":True,
        "1987-05-05":True,
        "1987-09-15":True,
        "1987-09-23":True,
        "1987-10-10":True,
        "1987-11-03":True,
        "1987-11-23":True,
        "1988-01-01":True,
        "1988-01-15":True,
        "1988-02-11":True,
        "1988-03-20":True,
        "1988-03-21":True,
        "1988-04-29":True,
        "1988-05-03":True,
        "1988-05-04":True,
        "1988-05-05":True,
        "1988-09-15":True,
        "1988-09-23":True,
        "1988-10-10":True,
        "1988-11-03":True,
        "1988-11-23":True,
        "1989-01-01":True,
        "1989-01-02":True,
        "1989-01-15":True,
        "1989-01-16":True,
        "1989-02-11":True,
        "1989-02-24":True,
        "1989-03-21":True,
        "1989-04-29":True,
        "1989-05-03":True,
        "1989-05-04":True,
        "1989-05-05":True,
        "1989-09-15":True,
        "1989-09-23":True,
        "1989-10-10":True,
        "1989-11-03":True,
        "1989-11-23":True,
        "1989-12-23":True,
        "1990-01-01":True,
        "1990-01-15":True,
        "1990-02-11":True,
        "1990-02-12":True,
        "1990-03-21":True,
        "1990-04-29":True,
        "1990-04-30":True,
        "1990-05-03":True,
        "1990-05-04":True,
        "1990-05-05":True,
        "1990-09-15":True,
        "1990-09-23":True,
        "1990-09-24":True,
        "1990-10-10":True,
        "1990-11-03":True,
        "1990-11-12":True,
        "1990-11-23":True,
        "1990-12-23":True,
        "1990-12-24":True,
        "1991-01-01":True,
        "1991-01-15":True,
        "1991-02-11":True,
        "1991-03-21":True,
        "1991-04-29":True,
        "1991-05-03":True,
        "1991-05-04":True,
        "1991-05-05":True,
        "1991-05-06":True,
        "1991-09-15":True,
        "1991-09-16":True,
        "1991-09-23":True,
        "1991-10-10":True,
        "1991-11-03":True,
        "1991-11-04":True,
        "1991-11-23":True,
        "1991-12-23":True,
        "1992-01-01":True,
        "1992-01-15":True,
        "1992-02-11":True,
        "1992-03-20":True,
        "1992-04-29":True,
        "1992-05-03":True,
        "1992-05-04":True,
        "1992-05-05":True,
        "1992-09-15":True,
        "1992-09-23":True,
        "1992-10-10":True,
        "1992-11-03":True,
        "1992-11-23":True,
        "1992-12-23":True,
        "1993-01-01":True,
        "1993-01-15":True,
        "1993-02-11":True,
        "1993-03-20":True,
        "1993-04-29":True,
        "1993-05-03":True,
        "1993-05-04":True,
        "1993-05-05":True,
        "1993-06-09":True,
        "1993-09-15":True,
        "1993-09-23":True,
        "1993-10-10":True,
        "1993-10-11":True,
        "1993-11-03":True,
        "1993-11-23":True,
        "1993-12-23":True,
        "1994-01-01":True,
        "1994-01-15":True,
        "1994-02-11":True,
        "1994-03-21":True,
        "1994-04-29":True,
        "1994-05-03":True,
        "1994-05-04":True,
        "1994-05-05":True,
        "1994-09-15":True,
        "1994-09-23":True,
        "1994-10-10":True,
        "1994-11-03":True,
        "1994-11-23":True,
        "1994-12-23":True,
        "1995-01-01":True,
        "1995-01-02":True,
        "1995-01-15":True,
        "1995-01-16":True,
        "1995-02-11":True,
        "1995-03-21":True,
        "1995-04-29":True,
        "1995-05-03":True,
        "1995-05-04":True,
        "1995-05-05":True,
        "1995-09-15":True,
        "1995-09-23":True,
        "1995-10-10":True,
        "1995-11-03":True,
        "1995-11-23":True,
        "1995-12-23":True,
        "1996-01-01":True,
        "1996-01-15":True,
        "1996-02-11":True,
        "1996-02-12":True,
        "1996-03-20":True,
        "1996-04-29":True,
        "1996-05-03":True,
        "1996-05-04":True,
        "1996-05-05":True,
        "1996-05-06":True,
        "1996-07-20":True,
        "1996-09-15":True,
        "1996-09-16":True,
        "1996-09-23":True,
        "1996-10-10":True,
        "1996-11-03":True,
        "1996-11-04":True,
        "1996-11-23":True,
        "1996-12-23":True,
        "1997-01-01":True,
        "1997-01-15":True,
        "1997-02-11":True,
        "1997-03-20":True,
        "1997-04-29":True,
        "1997-05-03":True,
        "1997-05-05":True,
        "1997-07-20":True,
        "1997-07-21":True,
        "1997-09-15":True,
        "1997-09-23":True,
        "1997-10-10":True,
        "1997-11-03":True,
        "1997-11-23":True,
        "1997-11-24":True,
        "1997-12-23":True,
        "1998-01-01":True,
        "1998-01-15":True,
        "1998-02-11":True,
        "1998-03-21":True,
        "1998-04-29":True,
        "1998-05-03":True,
        "1998-05-04":True,
        "1998-05-05":True,
        "1998-07-20":True,
        "1998-09-15":True,
        "1998-09-23":True,
        "1998-10-10":True,
        "1998-11-03":True,
        "1998-11-23":True,
        "1998-12-23":True,
        "1999-01-01":True,
        "1999-01-15":True,
        "1999-02-11":True,
        "1999-03-21":True,
        "1999-03-22":True,
        "1999-04-29":True,
        "1999-05-03":True,
        "1999-05-04":True,
        "1999-05-05":True,
        "1999-07-20":True,
        "1999-09-15":True,
        "1999-09-23":True,
        "1999-10-10":True,
        "1999-10-11":True,
        "1999-11-03":True,
        "1999-11-23":True,
        "1999-12-23":True,
        "2000-01-01":True,
        "2000-01-10":True,
        "2000-02-11":True,
        "2000-03-20":True,
        "2000-04-29":True,
        "2000-05-03":True,
        "2000-05-04":True,
        "2000-05-05":True,
        "2000-07-20":True,
        "2000-09-15":True,
        "2000-09-23":True,
        "2000-10-09":True,
        "2000-11-03":True,
        "2000-11-23":True,
        "2000-12-23":True,
        "2001-01-01":True,
        "2001-01-08":True,
        "2001-02-11":True,
        "2001-02-12":True,
        "2001-03-20":True,
        "2001-04-29":True,
        "2001-04-30":True,
        "2001-05-03":True,
        "2001-05-04":True,
        "2001-05-05":True,
        "2001-07-20":True,
        "2001-09-15":True,
        "2001-09-23":True,
        "2001-09-24":True,
        "2001-10-08":True,
        "2001-11-03":True,
        "2001-11-23":True,
        "2001-12-23":True,
        "2001-12-24":True,
        "2002-01-01":True,
        "2002-01-14":True,
        "2002-02-11":True,
        "2002-03-21":True,
        "2002-04-29":True,
        "2002-05-03":True,
        "2002-05-04":True,
        "2002-05-05":True,
        "2002-05-06":True,
        "2002-07-20":True,
        "2002-09-15":True,
        "2002-09-16":True,
        "2002-09-23":True,
        "2002-10-14":True,
        "2002-11-03":True,
        "2002-11-04":True,
        "2002-11-23":True,
        "2002-12-23":True,
        "2003-01-01":True,
        "2003-01-13":True,
        "2003-02-11":True,
        "2003-03-21":True,
        "2003-04-29":True,
        "2003-05-03":True,
        "2003-05-05":True,
        "2003-07-21":True,
        "2003-09-15":True,
        "2003-09-23":True,
        "2003-10-13":True,
        "2003-11-03":True,
        "2003-11-23":True,
        "2003-11-24":True,
        "2003-12-23":True,
        "2004-01-01":True,
        "2004-01-12":True,
        "2004-02-11":True,
        "2004-03-20":True,
        "2004-04-29":True,
        "2004-05-03":True,
        "2004-05-04":True,
        "2004-05-05":True,
        "2004-07-19":True,
        "2004-09-20":True,
        "2004-09-23":True,
        "2004-10-11":True,
        "2004-11-03":True,
        "2004-11-23":True,
        "2004-12-23":True,
        "2005-01-01":True,
        "2005-01-10":True,
        "2005-02-11":True,
        "2005-03-20":True,
        "2005-03-21":True,
        "2005-04-29":True,
        "2005-05-03":True,
        "2005-05-04":True,
        "2005-05-05":True,
        "2005-07-18":True,
        "2005-09-19":True,
        "2005-09-23":True,
        "2005-10-10":True,
        "2005-11-03":True,
        "2005-11-23":True,
        "2005-12-23":True,
        "2006-01-01":True,
        "2006-01-02":True,
        "2006-01-09":True,
        "2006-02-11":True,
        "2006-03-21":True,
        "2006-04-29":True,
        "2006-05-03":True,
        "2006-05-04":True,
        "2006-05-05":True,
        "2006-07-17":True,
        "2006-09-18":True,
        "2006-09-23":True,
        "2006-10-09":True,
        "2006-11-03":True,
        "2006-11-23":True,
        "2006-12-23":True,
        "2007-01-01":True,
        "2007-01-08":True,
        "2007-02-11":True,
        "2007-02-12":True,
        "2007-03-21":True,
        "2007-04-29":True,
        "2007-04-30":True,
        "2007-05-03":True,
        "2007-05-04":True,
        "2007-05-05":True,
        "2007-07-16":True,
        "2007-09-17":True,
        "2007-09-23":True,
        "2007-09-24":True,
        "2007-10-08":True,
        "2007-11-03":True,
        "2007-11-23":True,
        "2007-12-23":True,
        "2007-12-24":True,
        "2008-01-01":True,
        "2008-01-14":True,
        "2008-02-11":True,
        "2008-03-20":True,
        "2008-04-29":True,
        "2008-05-03":True,
        "2008-05-04":True,
        "2008-05-05":True,
        "2008-05-06":True,
        "2008-07-21":True,
        "2008-09-15":True,
        "2008-09-23":True,
        "2008-10-13":True,
        "2008-11-03":True,
        "2008-11-23":True,
        "2008-11-24":True,
        "2008-12-23":True,
        "2009-01-01":True,
        "2009-01-12":True,
        "2009-02-11":True,
        "2009-03-20":True,
        "2009-04-29":True,
        "2009-05-03":True,
        "2009-05-04":True,
        "2009-05-05":True,
        "2009-05-06":True,
        "2009-07-20":True,
        "2009-09-21":True,
        "2009-09-22":True,
        "2009-09-23":True,
        "2009-10-12":True,
        "2009-11-03":True,
        "2009-11-23":True,
        "2009-12-23":True,
        "2010-01-01":True,
        "2010-01-11":True,
        "2010-02-11":True,
        "2010-03-21":True,
        "2010-03-22":True,
        "2010-04-29":True,
        "2010-05-03":True,
        "2010-05-04":True,
        "2010-05-05":True,
        "2010-07-19":True,
        "2010-09-20":True,
        "2010-09-23":True,
        "2010-10-11":True,
        "2010-11-03":True,
        "2010-11-23":True,
        "2010-12-23":True,
        "2011-01-01":True,
        "2011-01-10":True,
        "2011-02-11":True,
        "2011-03-21":True,
        "2011-04-29":True,
        "2011-05-03":True,
        "2011-05-04":True,
        "2011-05-05":True,
        "2011-07-18":True,
        "2011-09-19":True,
        "2011-09-23":True,
        "2011-10-10":True,
        "2011-11-03":True,
        "2011-11-23":True,
        "2011-12-23":True,
        "2012-01-01":True,
        "2012-01-02":True,
        "2012-01-09":True,
        "2012-02-11":True,
        "2012-03-20":True,
        "2012-04-29":True,
        "2012-04-30":True,
        "2012-05-03":True,
        "2012-05-04":True,
        "2012-05-05":True,
        "2012-07-16":True,
        "2012-09-17":True,
        "2012-09-22":True,
        "2012-10-08":True,
        "2012-11-03":True,
        "2012-11-23":True,
        "2012-12-23":True,
        "2012-12-24":True,
        "2013-01-01":True,
        "2013-01-14":True,
        "2013-02-11":True,
        "2013-03-20":True,
        "2013-04-29":True,
        "2013-05-03":True,
        "2013-05-04":True,
        "2013-05-05":True,
        "2013-05-06":True,
        "2013-07-15":True,
        "2013-09-16":True,
        "2013-09-23":True,
        "2013-10-14":True,
        "2013-11-03":True,
        "2013-11-04":True,
        "2013-11-23":True,
        "2013-12-23":True,
        "2014-01-01":True,
        "2014-01-13":True,
        "2014-02-11":True,
        "2014-03-21":True,
        "2014-04-29":True,
        "2014-05-03":True,
        "2014-05-04":True,
        "2014-05-05":True,
        "2014-05-06":True,
        "2014-07-21":True,
        "2014-09-15":True,
        "2014-09-23":True,
        "2014-10-13":True,
        "2014-11-03":True,
        "2014-11-23":True,
        "2014-11-24":True,
        "2014-12-23":True,
        "2015-01-01":True,
        "2015-01-12":True,
        "2015-02-11":True,
        "2015-03-21":True,
        "2015-04-29":True,
        "2015-05-03":True,
        "2015-05-04":True,
        "2015-05-05":True,
        "2015-05-06":True,
        "2015-07-20":True,
        "2015-09-21":True,
        "2015-09-22":True,
        "2015-09-23":True,
        "2015-10-12":True,
        "2015-11-03":True,
        "2015-11-23":True,
        "2015-12-23":True,
        "2016-01-01":True,
        "2016-01-11":True,
        "2016-02-11":True,
        "2016-03-20":True,
        "2016-03-21":True,
        "2016-04-29":True,
        "2016-05-03":True,
        "2016-05-04":True,
        "2016-05-05":True,
        "2016-07-18":True,
        "2016-08-11":True,
        "2016-09-19":True,
        "2016-09-22":True,
        "2016-10-10":True,
        "2016-11-03":True,
        "2016-11-23":True,
        "2016-12-23":True,
        "2017-01-01":True, # 元日
        "2017-01-02":True, # 振替休日
        "2017-01-09":True, # 成人の日
        "2017-02-11":True, # 建国記念の日
        "2017-03-20":True, # 春分の日
        "2017-04-29":True, # 昭和の日
        "2017-05-03":True, # 憲法記念日
        "2017-05-04":True, # みどりの日
        "2017-05-05":True, # こどもの日
        "2017-07-17":True, # 海の日
        "2017-08-11":True, # 山の日
        "2017-09-18":True, # 敬老の日
        "2017-09-23":True, # 秋分の日
        "2017-10-09":True, # 体育の日
        "2017-11-03":True, # 文化の日
        "2017-11-23":True, # 勤労感謝の日
        "2017-12-23":True, # 天皇誕生日
        "2018-01-01":True, # 元日
        "2018-01-08":True, # 成人の日
        "2018-02-11":True, # 建国記念の日
        "2018-02-12":True, # 振替休日
        "2018-03-21":True, # 春分の日
        "2018-04-29":True, # 昭和の日
        "2018-04-30":True, # 振替休日
        "2018-05-03":True, # 憲法記念日
        "2018-05-04":True, # みどりの日
        "2018-05-05":True, # こどもの日
        "2018-07-16":True, # 海の日
        "2018-08-11":True, # 山の日
        "2018-09-17":True, # 敬老の日
        "2018-09-23":True, # 秋分の日
        "2018-09-24":True, # 振替休日
        "2018-10-08":True, # 体育の日
        "2018-11-03":True, # 文化の日
        "2018-11-23":True, # 勤労感謝の日
        "2018-12-23":True, # 天皇誕生日
        "2018-12-24":True, # 振替休日
        "2019-01-01":True, # 元日
        "2019-01-14":True, # 成人の日
        "2019-02-11":True, # 建国記念の日
        "2019-03-21":True, # 春分の日
        "2019-04-29":True, # 昭和の日
        "2019-04-30":True, # 祝日
        "2019-05-01":True, # 天皇の即位の日
        "2019-05-02":True, # 祝日
        "2019-05-03":True, # 憲法記念日
        "2019-05-04":True, # みどりの日
        "2019-05-05":True, # こどもの日
        "2019-05-06":True, # 振替休日
        "2019-07-15":True, # 海の日
        "2019-08-11":True, # 山の日
        "2019-08-12":True, # 振替休日
        "2019-09-16":True, # 敬老の日
        "2019-09-23":True, # 秋分の日
        "2019-10-14":True, # 体育の日
        "2019-11-03":True, # 文化の日
        "2019-11-04":True, # 振替休日
        "2019-11-23":True, # 勤労感謝の日
        "2020-01-01":True, # 元日
        "2020-01-13":True, # 成人の日
        "2020-02-11":True, # 建国記念の日
        "2020-02-23":True, # 天皇誕生日
        "2020-02-24":True, # 振替休日
        "2020-03-20":True, # 春分の日
        "2020-04-29":True, # 昭和の日
        "2020-05-03":True, # 憲法記念日
        "2020-05-04":True, # みどりの日
        "2020-05-05":True, # こどもの日
        "2020-05-06":True, # 振替休日
        "2020-07-20":True, # 海の日
        "2020-08-11":True, # 山の日
        "2020-09-21":True, # 敬老の日
        "2020-09-22":True, # 秋分の日
        "2020-10-12":True, # 体育の日
        "2020-11-03":True, # 文化の日
        "2020-11-23":True, # 勤労感謝の日
        "2021-01-01":True, # 元日
        "2021-01-11":True, # 成人の日
        "2021-02-11":True, # 建国記念の日
        "2021-02-23":True, # 天皇誕生日
        "2021-03-20":True, # 春分の日
        "2021-04-29":True, # 昭和の日
        "2021-05-03":True, # 憲法記念日
        "2021-05-04":True, # みどりの日
        "2021-05-05":True, # こどもの日
        "2021-07-19":True, # 海の日
        "2021-08-11":True, # 山の日
        "2021-09-20":True, # 敬老の日
        "2021-09-23":True, # 秋分の日
        "2021-10-11":True, # 体育の日
        "2021-11-03":True, # 文化の日
        "2021-11-23":True, # 勤労感謝の日
        "2022-01-01":True, # 元日
        "2022-01-10":True, # 成人の日
        "2022-02-11":True, # 建国記念の日
        "2022-02-23":True, # 天皇誕生日
        "2022-03-21":True, # 春分の日
        "2022-04-29":True, # 昭和の日
        "2022-05-03":True, # 憲法記念日
        "2022-05-04":True, # みどりの日
        "2022-05-05":True, # こどもの日
        "2022-07-18":True, # 海の日
        "2022-08-11":True, # 山の日
        "2022-09-19":True, # 敬老の日
        "2022-09-23":True, # 秋分の日
        "2022-10-10":True, # 体育の日
        "2022-11-03":True, # 文化の日
        "2022-11-23":True, # 勤労感謝の日
        "2023-01-01":True, # 元日
        "2023-01-02":True, # 振替休日
        "2023-01-09":True, # 成人の日
        "2023-02-11":True, # 建国記念の日
        "2023-02-23":True, # 天皇誕生日
        "2023-03-21":True, # 春分の日
        "2023-04-29":True, # 昭和の日
        "2023-05-03":True, # 憲法記念日
        "2023-05-04":True, # みどりの日
        "2023-05-05":True, # こどもの日
        "2023-07-17":True, # 海の日
        "2023-08-11":True, # 山の日
        "2023-09-18":True, # 敬老の日
        "2023-09-23":True, # 秋分の日
        "2023-10-09":True, # 体育の日
        "2023-11-03":True, # 文化の日
        "2023-11-23":True, # 勤労感謝の日
        "2024-01-01":True, # 元日
        "2024-01-08":True, # 成人の日
        "2024-02-11":True, # 建国記念の日
        "2024-02-12":True, # 振替休日
        "2024-02-23":True, # 天皇誕生日
        "2024-03-20":True, # 春分の日
        "2024-04-29":True, # 昭和の日
        "2024-05-03":True, # 憲法記念日
        "2024-05-04":True, # みどりの日
        "2024-05-05":True, # こどもの日
        "2024-05-06":True, # 振替休日
        "2024-07-15":True, # 海の日
        "2024-08-11":True, # 山の日
        "2024-08-12":True, # 振替休日
        "2024-09-16":True, # 敬老の日
        "2024-09-22":True, # 秋分の日
        "2024-09-23":True, # 振替休日
        "2024-10-14":True, # 体育の日
        "2024-11-03":True, # 文化の日
        "2024-11-04":True, # 振替休日
        "2024-11-23":True, # 勤労感謝の日
        "2025-01-01":True, # 元日
        "2025-01-13":True, # 成人の日
        "2025-02-11":True, # 建国記念の日
        "2025-02-23":True, # 天皇誕生日
        "2025-02-24":True, # 振替休日
        "2025-03-20":True, # 春分の日
        "2025-04-29":True, # 昭和の日
        "2025-05-03":True, # 憲法記念日
        "2025-05-04":True, # みどりの日
        "2025-05-05":True, # こどもの日
        "2025-05-06":True, # 振替休日
        "2025-07-21":True, # 海の日
        "2025-08-11":True, # 山の日
        "2025-09-15":True, # 敬老の日
        "2025-09-23":True, # 秋分の日
        "2025-10-13":True, # 体育の日
        "2025-11-03":True, # 文化の日
        "2025-11-23":True, # 勤労感謝の日
        "2025-11-24":True, # 振替休日
        "2026-01-01":True, # 元日
        "2026-01-12":True, # 成人の日
        "2026-02-11":True, # 建国記念の日
        "2026-02-23":True, # 天皇誕生日
        "2026-03-20":True, # 春分の日
        "2026-04-29":True, # 昭和の日
        "2026-05-03":True, # 憲法記念日
        "2026-05-04":True, # みどりの日
        "2026-05-05":True, # こどもの日
        "2026-05-06":True, # 振替休日
        "2026-07-20":True, # 海の日
        "2026-08-11":True, # 山の日
        "2026-09-21":True, # 敬老の日
        "2026-09-22":True, # 国民の休日
        "2026-09-23":True, # 秋分の日
        "2026-10-12":True, # 体育の日
        "2026-11-03":True, # 文化の日
        "2026-11-23":True, # 勤労感謝の日
        "2027-01-01":True, # 元日
        "2027-01-11":True, # 成人の日
        "2027-02-11":True, # 建国記念の日
        "2027-02-23":True, # 天皇誕生日
        "2027-03-21":True, # 春分の日
        "2027-03-22":True, # 振替休日
        "2027-04-29":True, # 昭和の日
        "2027-05-03":True, # 憲法記念日
        "2027-05-04":True, # みどりの日
        "2027-05-05":True, # こどもの日
        "2027-07-19":True, # 海の日
        "2027-08-11":True, # 山の日
        "2027-09-20":True, # 敬老の日
        "2027-09-23":True, # 秋分の日
        "2027-10-11":True, # 体育の日
        "2027-11-03":True, # 文化の日
        "2027-11-23":True, # 勤労感謝の日
        "2028-01-01":True, # 元日
        "2028-01-10":True, # 成人の日
        "2028-02-11":True, # 建国記念の日
        "2028-02-23":True, # 天皇誕生日
        "2028-03-20":True, # 春分の日
        "2028-04-29":True, # 昭和の日
        "2028-05-03":True, # 憲法記念日
        "2028-05-04":True, # みどりの日
        "2028-05-05":True, # こどもの日
        "2028-07-17":True, # 海の日
        "2028-08-11":True, # 山の日
        "2028-09-18":True, # 敬老の日
        "2028-09-22":True, # 秋分の日
        "2028-10-09":True, # 体育の日
        "2028-11-03":True, # 文化の日
        "2028-11-23":True, # 勤労感謝の日
        "2029-01-01":True, # 元日
        "2029-01-08":True, # 成人の日
        "2029-02-11":True, # 建国記念の日
        "2029-02-12":True, # 振替休日
        "2029-02-23":True, # 天皇誕生日
        "2029-03-20":True, # 春分の日
        "2029-04-29":True, # 昭和の日
        "2029-04-30":True, # 振替休日
        "2029-05-03":True, # 憲法記念日
        "2029-05-04":True, # みどりの日
        "2029-05-05":True, # こどもの日
        "2029-07-16":True, # 海の日
        "2029-08-11":True, # 山の日
        "2029-09-17":True, # 敬老の日
        "2029-09-23":True, # 秋分の日
        "2029-09-24":True, # 振替休日
        "2029-10-08":True, # 体育の日
        "2029-11-03":True, # 文化の日
        "2029-11-23":True, # 勤労感謝の日
        "2030-01-01":True, # 元日
        "2030-01-14":True, # 成人の日
        "2030-02-11":True, # 建国記念の日
        "2030-02-23":True, # 天皇誕生日
        "2030-03-20":True, # 春分の日
        "2030-04-29":True, # 昭和の日
        "2030-05-03":True, # 憲法記念日
        "2030-05-04":True, # みどりの日
        "2030-05-05":True, # こどもの日
        "2030-05-06":True, # 振替休日
        "2030-07-15":True, # 海の日
        "2030-08-11":True, # 山の日
        "2030-08-12":True, # 振替休日
        "2030-09-16":True, # 敬老の日
        "2030-09-23":True, # 秋分の日
        "2030-10-14":True, # 体育の日
        "2030-11-03":True, # 文化の日
        "2030-11-04":True, # 振替休日
        "2030-11-23":True, # 勤労感謝の日
        "2031-01-01":True, # 元日
        "2031-01-13":True, # 成人の日
        "2031-02-11":True, # 建国記念の日
        "2031-02-23":True, # 天皇誕生日
        "2031-02-24":True, # 振替休日
        "2031-03-21":True, # 春分の日
        "2031-04-29":True, # 昭和の日
        "2031-05-03":True, # 憲法記念日
        "2031-05-04":True, # みどりの日
        "2031-05-05":True, # こどもの日
        "2031-05-06":True, # 振替休日
        "2031-07-21":True, # 海の日
        "2031-08-11":True, # 山の日
        "2031-09-15":True, # 敬老の日
        "2031-09-23":True, # 秋分の日
        "2031-10-13":True, # 体育の日
        "2031-11-03":True, # 文化の日
        "2031-11-23":True, # 勤労感謝の日
        "2031-11-24":True, # 振替休日
        "2032-01-01":True, # 元日
        "2032-01-12":True, # 成人の日
        "2032-02-11":True, # 建国記念の日
        "2032-02-23":True, # 天皇誕生日
        "2032-03-20":True, # 春分の日
        "2032-04-29":True, # 昭和の日
        "2032-05-03":True, # 憲法記念日
        "2032-05-04":True, # みどりの日
        "2032-05-05":True, # こどもの日
        "2032-07-19":True, # 海の日
        "2032-08-11":True, # 山の日
        "2032-09-20":True, # 敬老の日
        "2032-09-21":True, # 国民の休日
        "2032-09-22":True, # 秋分の日
        "2032-10-11":True, # 体育の日
        "2032-11-03":True, # 文化の日
        "2032-11-23":True, # 勤労感謝の日
        "2033-01-01":True, # 元日
        "2033-01-10":True, # 成人の日
        "2033-02-11":True, # 建国記念の日
        "2033-02-23":True, # 天皇誕生日
        "2033-03-20":True, # 春分の日
        "2033-03-21":True, # 振替休日
        "2033-04-29":True, # 昭和の日
        "2033-05-03":True, # 憲法記念日
        "2033-05-04":True, # みどりの日
        "2033-05-05":True, # こどもの日
        "2033-07-18":True, # 海の日
        "2033-08-11":True, # 山の日
        "2033-09-19":True, # 敬老の日
        "2033-09-23":True, # 秋分の日
        "2033-10-10":True, # 体育の日
        "2033-11-03":True, # 文化の日
        "2033-11-23":True, # 勤労感謝の日
        "2034-01-01":True, # 元日
        "2034-01-02":True, # 振替休日
        "2034-01-09":True, # 成人の日
        "2034-02-11":True, # 建国記念の日
        "2034-02-23":True, # 天皇誕生日
        "2034-03-20":True, # 春分の日
        "2034-04-29":True, # 昭和の日
        "2034-05-03":True, # 憲法記念日
        "2034-05-04":True, # みどりの日
        "2034-05-05":True, # こどもの日
        "2034-07-17":True, # 海の日
        "2034-08-11":True, # 山の日
        "2034-09-18":True, # 敬老の日
        "2034-09-23":True, # 秋分の日
        "2034-10-09":True, # 体育の日
        "2034-11-03":True, # 文化の日
        "2034-11-23":True, # 勤労感謝の日
        "2035-01-01":True, # 元日
        "2035-01-08":True, # 成人の日
        "2035-02-11":True, # 建国記念の日
        "2035-02-12":True, # 振替休日
        "2035-02-23":True, # 天皇誕生日
        "2035-03-21":True, # 春分の日
        "2035-04-29":True, # 昭和の日
        "2035-04-30":True, # 振替休日
        "2035-05-03":True, # 憲法記念日
        "2035-05-04":True, # みどりの日
        "2035-05-05":True, # こどもの日
        "2035-07-16":True, # 海の日
        "2035-08-11":True, # 山の日
        "2035-09-17":True, # 敬老の日
        "2035-09-23":True, # 秋分の日
        "2035-09-24":True, # 振替休日
        "2035-10-08":True, # 体育の日
        "2035-11-03":True, # 文化の日
        "2035-11-23":True, # 勤労感謝の日
        "2036-01-01":True, # 元日
        "2036-01-14":True, # 成人の日
        "2036-02-11":True, # 建国記念の日
        "2036-02-23":True, # 天皇誕生日
        "2036-03-20":True, # 春分の日
        "2036-04-29":True, # 昭和の日
        "2036-05-03":True, # 憲法記念日
        "2036-05-04":True, # みどりの日
        "2036-05-05":True, # こどもの日
        "2036-05-06":True, # 振替休日
        "2036-07-21":True, # 海の日
        "2036-08-11":True, # 山の日
        "2036-09-15":True, # 敬老の日
        "2036-09-22":True, # 秋分の日
        "2036-10-13":True, # 体育の日
        "2036-11-03":True, # 文化の日
        "2036-11-23":True, # 勤労感謝の日
        "2036-11-24":True, # 振替休日
    }
    return holidays.get(day,False)
