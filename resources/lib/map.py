# -*- coding: utf-8 -*-

try:
    from sqlite3 import dbapi2 as sqlite
except Exception:
    from pysqlite2 import dbapi2 as sqlite

import os

from urllib.request import urlretrieve
from urllib.request import urlcleanup
from urllib.parse import unquote
from urllib.parse import urlencode
from urllib.error import HTTPError

import xbmc
import xbmcaddon
import xbmcvfs

from resources.lib.common import *
from resources.lib.const import *


class Map:

    def __init__(self):
        # ディレクトリ
        self.path = os.path.join(Const.PROFILE_PATH, 'cache', 'thumbnail')
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        # DB
        self.db = os.path.join(xbmcvfs.translatePath('special://database'), 'Textures13.db')
        # 言語
        self.lang = Const.STR(30020)
        # 地域
        self.region = Const.STR(30021)

    def create(self, minLatLong, maxLatLong=None):
        # クエリ作成 https://developers.google.com/maps/documentation/static-maps/intro
        coordinates = '%s,%s' % minLatLong
        if maxLatLong:
            coordinates = coordinates + '|%s,%s' % maxLatLong
        req_param = {
            "visible": coordinates,
            "size": "320x320",
            "scale": "2",
            "maptype": "roadmap",
            "style": "feature:road.local|element:geometry|visibility:simplified",
            "style": "feature:administrative|element:labels.text.fill|color:0x000000",
            "style": "feature:administrative.province|element:geometry.stroke|weight:2|color:0x444444",
        }
        # ファイル名
        imagefile = os.path.join(self.path, '%s.png' % coordinates)
        # キャッシュクリア
        if os.path.isfile(imagefile) and os.path.getsize(imagefile) < 12000:
            try:
                # delete imagefile
                os.remove(imagefile)
                # delete from database
                conn = sqlite.connect(self.db)
                c = conn.cursor()
                c.execute("DELETE FROM texture WHERE url = ?", (imagefile,))
                conn.commit()
                conn.close()
            except Exception:
                pass
        # ファイル取得
        if not os.path.isfile(imagefile):
            try:
                try:
                    xbmc.sleep(1000)
                except Exception:
                    pass
                # urlretrieve(unquote('http://maps.googleapis.com/maps/api/staticmap?' + urlencode(req_param)), imagefile)
                urlretrieve(unquote(('http://maps.googleapis.com/maps/api/staticmap?language=%s&region=%s&' % (self.lang, self.region)) + urlencode(req_param)), imagefile)
            except HTTPError as e:
                raise e
            except Exception:
                urlcleanup()
                remove_tries = 3
                while remove_tries and os.path.isfile(imagefile):
                    try:
                        os.remove(imagefile)
                    except Exception:
                        remove_tries -= 1
                    try:
                        xbmc.sleep(1000)
                    except Exception:
                        pass
        return imagefile
