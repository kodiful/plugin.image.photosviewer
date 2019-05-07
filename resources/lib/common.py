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
