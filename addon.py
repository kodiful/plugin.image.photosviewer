# -*- coding: utf-8 -*-

import sys
import time
import os
import glob
import datetime

from urllib.parse import parse_qs
from urllib.parse import urlencode

import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs

from resources.lib.common import *
from resources.lib.db import *
from resources.lib.map import *
from resources.lib.cache import *
from resources.lib.const import *


def build_url(values):
    query = urlencode(values)
    if query:
        url = '%s?%s' % (Const.BASE_URL, query)
    else:
        url = Const.BASE_URL
    return url


def convert_timestamp(year=None, month=None, day=None, hour=None, minute=None, timestamp=None):
    if timestamp:
        t = datetime.datetime.fromtimestamp(int(timestamp) + 978307200)
        (year, month, day, hour, minute) = t.replace(year=t.year).strftime('%Y,%m,%d,%H,%M').split(',')
    if year:
        if month:
            m = Const.STR(30017).split(',')
            mindex = int(month) - 1
            if day:
                d = Const.STR(30018).split(',')
                dindex = datetime.date(int(year), int(month), int(day)).weekday()
                if hour and minute:
                    itemname = Const.STR(30030).format(year=year, month=m[mindex], day=day, day7=d[dindex], hour=hour, minute=minute)
                else:
                    itemname = Const.STR(30031).format(year=year, month=m[mindex], day=day, day7=d[dindex])
                if isholiday('%s-%s-%s' % (year, month, day)) or dindex == 6:
                    itemname = '[COLOR red]' + itemname + '[/COLOR]'
                elif dindex == 5:
                    itemname = '[COLOR blue]' + itemname + '[/COLOR]'
            else:
                itemname = Const.STR(30032).format(year=year, month=m[mindex])
        else:
            itemname = Const.STR(30033).format(year=year)
    else:
        itemname = ''
    return itemname


class App:

    def __init__(self):
        # ハンドル
        self.handle = int(sys.argv[1])
        # 写真アプリのパス
        self.photo_app_path = Const.GET('photo_library_path')
        if self.photo_app_path == '':
            self.photo_app_path = os.path.join(os.getenv('HOME'), 'Pictures', Const.STR(30000))
        Const.SET('photo_library_path', self.photo_app_path)
        # photos.dbをチェック
        self.photo_app_db_file = os.path.join(Const.PROFILE_PATH, 'photos.db')
        self.photo_app_db_orig = os.path.join(self.photo_app_path, 'database', 'photos.db')
        ctime = os.stat(self.photo_app_db_orig).st_ctime
        mtime = os.stat(self.photo_app_db_orig).st_mtime
        # photos.dbをコピー
        if xbmcvfs.exists(self.photo_app_db_file) and os.stat(self.photo_app_db_file).st_mtime == mtime:
            pass
        else:
            xbmcvfs.copy(self.photo_app_db_orig, self.photo_app_db_file)
            #os.utime(self.photo_app_db_file, (ctime, mtime))
        # ファイルのパス
        self.photo_app_picture_path = os.path.join(self.photo_app_path, 'Masters')
        self.photo_app_thumbnail_path = os.path.join(self.photo_app_path, 'resources', 'proxies', 'derivatives')
        self.photo_app_face_path = os.path.join(self.photo_app_path, 'resources', 'media', 'face')
        # DB
        self.db = None

    def open_db(self):
        if self.db is not None:
            return
        try:
            self.db = DB(self.photo_app_db_file)
        except Exception:
            pass
        return self

    def close_db(self):
        try:
            self.db.CloseDB()
        except Exception:
            pass
        return self

    def list_moments(self, year, month):
        n = 0
        moments = self.db.GetMomentList(year, month)
        for (name,) in moments:
            if year is None:
                url = build_url({'action': 'moments', 'year': name})
                item = xbmcgui.ListItem(convert_timestamp(year=name))
                item.setArt({'icon': Const.CALENDAR, 'thumbnail': Const.CALENDAR})
                contextmenu = []
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=name)), 'Container.Update(%s)' % build_url({'action': 'search_by_year', 'year': name})))
                item.addContextMenuItems(contextmenu, replaceItems=True)
            elif month is None:
                url = build_url({'action': 'moments', 'year': year, 'month': name})
                item = xbmcgui.ListItem(convert_timestamp(year=year, month=name))
                item.setArt({'icon': Const.CALENDAR, 'thumbnail': Const.CALENDAR})
                contextmenu = []
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=year, month=name)), 'Container.Update(%s)' % build_url({'action': 'search_by_month', 'year': year, 'month': name})))
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=year)), 'Container.Update(%s)' % build_url({'action': 'search_by_year', 'year': year})))
                item.addContextMenuItems(contextmenu, replaceItems=True)
            else:
                url = build_url({'action': 'search_by_day', 'year': year, 'month': month, 'day': name})
                item = xbmcgui.ListItem(convert_timestamp(year=year, month=month, day=name))
                item.setArt({'icon': Const.CALENDAR, 'thumbnail': Const.CALENDAR})
                contextmenu = []
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=year, month=month)), 'Container.Update(%s)' % build_url({'action': 'search_by_month', 'year': year, 'month': month})))
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=year)), 'Container.Update(%s)' % build_url({'action': 'search_by_year', 'year': year})))
                item.addContextMenuItems(contextmenu, replaceItems=True)
            xbmcplugin.addDirectoryItem(self.handle, url, item, True)
            n += 1
        return n

    def list_places(self, parent=None):
        n = 0
        map = Map()
        places = self.db.GetPlaceList(parent)
        for (name, uuid, type, modelId, minLatitude, maxLatitude, minLongitude, maxLongitude) in places:
            try:
                thumbnail = map.create((minLatitude, minLongitude), (maxLatitude, maxLongitude))
            except Exception:
                thumbnail = Const.MARKER
            if int(type) > 16:
                url = build_url({'action': 'places', 'uuid': uuid})
                item = xbmcgui.ListItem(name)
                item.setArt({'icon': thumbnail, 'thumbnail': thumbnail})
            else:
                url = build_url({'action': 'places', 'name': smart_utf8(name), 'uuid': uuid, 'type': type, 'modelId': modelId})
                item = xbmcgui.ListItem(name)
                item.setArt({'icon': thumbnail, 'thumbnail': thumbnail})
                contextmenu = []
                contextmenu.append((Const.STR(30013).format(place=smart_unicode(name)), 'Container.Update(%s)' % build_url({'action': 'places', 'uuid': uuid})))
                item.addContextMenuItems(contextmenu, replaceItems=True)
            xbmcplugin.addDirectoryItem(self.handle, url, item, True)
            n += 1
        return n

    def list_people(self):
        n = 0
        people = self.db.GetPersonList()
        for (name, uuid, modelId) in people:
            url = build_url({'action': 'people', 'uuid': uuid})
            imagePath = glob.glob(os.path.join(self.photo_app_face_path, ('%04x' % modelId)[0:2], '00', 'facetile_%x.jpeg' % modelId))[-1]
            item = xbmcgui.ListItem(name)
            item.setArt({'icon': imagePath, 'thumbnail': imagePath})
            xbmcplugin.addDirectoryItem(self.handle, url, item, True)
            n += 1
        return n

    def list_albums(self, folderUuid):
        n = 0
        folders = self.db.GetFolderList(folderUuid)
        for (name, uuid) in folders:
            url = build_url({'action': 'albums', 'folderUuid': uuid})
            thumbnailPath = Const.PHOTO_GALLERY
            item = xbmcgui.ListItem(name)
            item.setArt({'icon': thumbnailPath, 'thumbnail': thumbnailPath})
            xbmcplugin.addDirectoryItem(self.handle, url, item, True)
            n += 1
        albums = self.db.GetAlbumList(folderUuid)
        for (name, uuid, modelId) in albums:
            url = build_url({'action': 'albums', 'uuid': uuid})
            thumbnailPath = glob.glob(os.path.join(self.photo_app_thumbnail_path, ('%04x' % modelId)[0:2], '00', '%x' % modelId, '*.jpg'))[-1]
            item = xbmcgui.ListItem(name)
            item.setArt({'icon': thumbnailPath, 'thumbnail': thumbnailPath})
            xbmcplugin.addDirectoryItem(self.handle, url, item, True)
            n += 1
        return n

    def list_photos(self, uuid, action):
        pictures = self.db.GetPictureList(uuid, action)
        heic = Const.GET('heic')
        n = 0
        for (imageDate, imagePath, isMissing, modelId, latitude, longitude, orientation) in pictures:
            thumbnailPath = glob.glob(os.path.join(self.photo_app_thumbnail_path, ('%04x' % modelId)[0:2], '00', '%x' % modelId, '*.jpg'))[-1]
            if isMissing == 0:
                imagePath = os.path.join(self.photo_app_picture_path, smart_utf8(imagePath))
            else:
                imagePath = thumbnailPath
            # replace heic images with thumbnails
            if imagePath.endswith('.HEIC') or imagePath.endswith('.heic'):
                if heic == '0':
                    # サムネイルで代替
                    imagePath = thumbnailPath
                elif heic == '1':
                    # JPEGに変換
                    imagePath = Cache().convert(imagePath)
                else:
                    pass
            item = xbmcgui.ListItem(convert_timestamp(timestamp=imageDate))
            item.setArt({'icon': thumbnailPath, 'thumbnail': thumbnailPath})
            contextmenu = []
            contextmenu.append((Const.STR(30010), 'Container.Update(%s)' % build_url({'action': 'search_by_timestamp', 'timestamp': imageDate})))
            if latitude and longitude:
                contextmenu.append((Const.STR(30011), 'Container.Update(%s)' % build_url({'action': 'search_by_latlong', 'latitude': latitude, 'longitude': longitude})))
            contextmenu.append((Const.STR(30014), 'Container.Update(%s,replace)' % build_url({})))
            item.addContextMenuItems(contextmenu, replaceItems=True)
            xbmcplugin.addDirectoryItem(self.handle, imagePath, item, False)
            n += 1
        return n

    def list_videos(self):
        n = 0
        videos = self.db.GetVideoList()
        for (imageDate, imagePath, isMissing, modelId, latitude, longitude) in videos:
            thumbnailPath = glob.glob(os.path.join(self.photo_app_thumbnail_path, ('%04x' % modelId)[0:2], '00', '%x' % modelId, '*.jpg'))[-1]
            if isMissing == 0:
                imagePath = os.path.join(self.photo_app_picture_path, smart_utf8(imagePath))
            else:
                imagePath = thumbnailPath
            item = xbmcgui.ListItem(convert_timestamp(timestamp=imageDate))
            item.setArt({'icon': thumbnailPath, 'thumbnail': thumbnailPath})
            contextmenu = []
            contextmenu.append((Const.STR(30010), 'Container.Update(%s)' % build_url({'action': 'search_by_timestamp', 'timestamp': imageDate})))
            if latitude and longitude:
                contextmenu.append((Const.STR(30011), 'Container.Update(%s)' % build_url({'action': 'search_by_latlong', 'latitude': latitude, 'longitude': longitude})))
            contextmenu.append((Const.STR(30014), 'Container.Update(%s,replace)' % build_url({})))
            item.addContextMenuItems(contextmenu, replaceItems=True)
            xbmcplugin.addDirectoryItem(self.handle, imagePath, item, False)
            n += 1
        return n

    def main_menu(self):
        url = build_url({'action': 'moments'})
        item = xbmcgui.ListItem(Const.STR(30001))
        item.setArt({'icon': Const.PICTURE, 'thumbnail': Const.PICTURE})
        xbmcplugin.addDirectoryItem(self.handle, url, item, True)

        url = build_url({'action': 'people'})
        item = xbmcgui.ListItem(Const.STR(30003))
        item.setArt({'icon': Const.PEOPLE, 'thumbnail': Const.PEOPLE})
        xbmcplugin.addDirectoryItem(self.handle, url, item, True)

        url = build_url({'action': 'places'})
        item = xbmcgui.ListItem(Const.STR(30002))
        item.setArt({'icon': Const.MARKER, 'thumbnail': Const.MARKER})
        xbmcplugin.addDirectoryItem(self.handle, url, item, True)

        url = build_url({'action': 'videos'})
        item = xbmcgui.ListItem(Const.STR(30005))
        item.setArt({'icon': Const.MOVIE, 'thumbnail': Const.MOVIE})
        xbmcplugin.addDirectoryItem(self.handle, url, item, True)

        url = build_url({'action': 'albums', 'folderUuid': 'TopLevelAlbums'})
        item = xbmcgui.ListItem(Const.STR(30004))
        item.setArt({'icon': Const.PHOTO_GALLERY, 'thumbnail': Const.PHOTO_GALLERY})
        xbmcplugin.addDirectoryItem(self.handle, url, item, True)

        return 4


if __name__ == '__main__':

    args = parse_qs(sys.argv[2][1:])
    for key in args.keys():
        args[key] = args[key][0]

    action = args.get('action', None)
    folderUuid = args.get('folderUuid', None)
    uuid = args.get('uuid', None)
    year = args.get('year', None)
    month = args.get('month', None)
    day = args.get('day', None)

    timestamp = args.get('timestamp', None)
    latitude = args.get('latitude', None)
    longitude = args.get('longitude', None)

    name = args.get('name', None)
    type = args.get('type', None)
    modelId = args.get('modelId', None)

    app = App().open_db()

    if action is None:
        Cache().clear()
        items = app.main_menu()
    elif uuid:
        if type:
            items = app.list_places((name, uuid, int(type), int(modelId)))
            if items == 0:
                items = app.list_photos(uuid, action)
        else:
            items = app.list_photos(uuid, action)
    elif action == 'moments':
        items = app.list_moments(year, month)
    elif action == 'people':
        items = app.list_people()
    elif action == 'places':
        items = app.list_places()
    elif action == 'videos':
        items = app.list_videos()
    elif action == 'albums':
        items = app.list_albums(folderUuid)

    elif action == 'search_by_year':
        items = app.list_photos((year), action)
    elif action == 'search_by_month':
        items = app.list_photos((year, month), action)
    elif action == 'search_by_day':
        items = app.list_photos((year, month, day), action)
    elif action == 'search_by_timestamp':
        items = app.list_photos((timestamp), action)
    elif action == 'search_by_latlong':
        items = app.list_photos((latitude, longitude), action)
    else:
        items = 0

    app.close_db()

    if items == 0:
        notify(Const.STR(30100))
    else:
        xbmcplugin.endOfDirectory(int(sys.argv[1]), True)
