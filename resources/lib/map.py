# -*- coding: utf-8 -*-

import os

from sqlite3 import dbapi2 as sqlite
from urllib.request import urlretrieve
from urllib.request import urlcleanup
from urllib.error import HTTPError

import xbmc
import xbmcvfs

from resources.lib.const import Const


class Map:

    def __init__(self):
        # ディレクトリ
        self.path = os.path.join(Const.PROFILE_PATH, 'cache', 'thumbnail')
        if not os.path.isdir(self.path):
            os.makedirs(self.path)
        # DB
        self.db = os.path.join(xbmcvfs.translatePath('special://database'), 'Textures13.db')
        # APIキー
        self.key = Const.GET('apikey')
        # 言語
        self.lang = Const.STR(30020)
        # 地域
        self.region = Const.STR(30021)

    def create(self, minLatLong, maxLatLong=None):
        # クエリ作成 https://developers.google.com/maps/documentation/static-maps/intro
        coordinates = '%s,%s' % minLatLong
        if maxLatLong:
            coordinates = coordinates + '|%s,%s' % maxLatLong
        # ファイルパス
        filepath = os.path.join(self.path, '%s.png' % coordinates)
        # 不完全なファイルは削除
        if os.path.isfile(filepath) and os.path.getsize(filepath) < 12000:
            try:
                # delete imagefile
                os.remove(filepath)
                # delete from database
                conn = sqlite.connect(self.db)
                c = conn.cursor()
                c.execute("DELETE FROM texture WHERE url = ?", (filepath,))
                conn.commit()
                conn.close()
            except Exception:
                pass
        # ファイルを取得
        if not os.path.isfile(filepath):
            if self.key:
                # APIキーが設定されていたら画像ファイルを取得
                try:
                    try:
                        xbmc.sleep(1000)
                    except Exception:
                        pass
                    # リクエストパラメータ
                    params = (
                        ('key', self.key),
                        ('language', self.lang),
                        ('region', self.region),
                        ('visible', coordinates),
                        ('size', '320x320'),
                        ('scale', '2'),
                        ('maptype', 'roadmap'),
                        ('style', 'feature:road.local|element:geometry|visibility:simplified'),
                        ('style', 'feature:administrative|element:labels.text.fill|color:0x000000'),
                        ('style', 'feature:administrative.province|element:geometry.stroke|weight:2|color:0x444444'),
                    )
                    # リクエスト実行
                    urlretrieve(
                        'http://maps.googleapis.com/maps/api/staticmap?%s' % '&'.join(map(lambda x: '%s=%s' % x, params)),
                        filepath)
                except HTTPError as e:
                    raise e
                except Exception:
                    urlcleanup()
                    remove_tries = 3
                    while remove_tries and os.path.isfile(filepath):
                        try:
                            os.remove(filepath)
                        except Exception:
                            remove_tries -= 1
                        try:
                            xbmc.sleep(1000)
                        except Exception:
                            pass
        # 完全なファイルが取得できなかったらデフォルトの画像ファイルを設定
        if not os.path.isfile(filepath) or os.path.getsize(filepath) < 12000:
            filepath = Const.MARKER
        return filepath
