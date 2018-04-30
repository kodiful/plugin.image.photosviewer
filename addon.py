# -*- coding: utf-8 -*-

import sys
import time
import os
import glob
import urllib
import urlparse
import datetime

import xbmc
import xbmcgui as gui
import xbmcplugin as plugin
import xbmcaddon
import xbmcvfs

from resources.lib.common import *
from resources.lib.db import *
from resources.lib.map import *
from resources.lib.cache import *
from resources.lib.const import Const

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

def build_url(values):
    query = urllib.urlencode(values)
    if query:
        url = '%s?%s' % (base_url,query)
    else:
        url = base_url
    return url

def convert_timestamp(year=None, month=None, day=None, hour=None, minute=None, timestamp=None):
    if timestamp:
        t = datetime.datetime.fromtimestamp(int(timestamp)+978307200)
        (year,month,day,hour,minute) = t.replace(year=t.year).strftime('%Y,%m,%d,%H,%M').split(',')
    if year:
        if month:
            m = Const.STR(30017).split(',')
            mindex = int(month)-1
            if day:
                d = Const.STR(30018).split(',')
                dindex = datetime.date(int(year), int(month), int(day)).weekday()
                if hour and minute:
                    itemname = Const.STR(30030).format(year=year, month=m[mindex], day=day, day7=d[dindex], hour=hour, minute=minute)
                else:
                    itemname = Const.STR(30031).format(year=year, month=m[mindex], day=day, day7=d[dindex])
                if isholiday('%s-%s-%s' % (year,month,day)) or dindex == 6:
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
        # パラメータ
    	self.params = {}
        qs = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query, keep_blank_values=True)
        for key in qs.keys():
            self.params[key] = qs[key][0]

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
            os.utime(self.photo_app_db_file, (ctime, mtime))
        # ファイルのパス
        self.photo_app_picture_path = os.path.join(self.photo_app_path, 'Masters')
        self.photo_app_thumbnail_path = os.path.join(self.photo_app_path, 'resources', 'proxies', 'derivatives')
        self.photo_app_face_path = os.path.join(self.photo_app_path, 'resources', 'media', 'face')
        # DB
    	self.db = None

    def open_db(self):
    	if self.db is not None: return
    	try:
            self.db = DB(self.photo_app_db_file)
    	except:
            pass

    def close_db(self):
    	try:
    	    self.db.CloseDB()
    	except:
    	    pass

    def list_moments(self, year, month):
    	n = 0
    	moments = self.db.GetMomentList(year, month)
    	for (name,) in moments:
    	    if year is None:
                url = build_url({'action': 'moments', 'year': name})
                item = gui.ListItem(convert_timestamp(year=name), iconImage=Const.CALENDAR, thumbnailImage=Const.CALENDAR)
                contextmenu = []
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=name)), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_year', 'year': name})))
                item.addContextMenuItems(contextmenu, replaceItems=True)
    	    elif month is None:
                url = build_url({'action': 'moments', 'year': year[0], 'month': name})
                item = gui.ListItem(convert_timestamp(year=year[0],month=name), iconImage=Const.CALENDAR, thumbnailImage=Const.CALENDAR)
                contextmenu = []
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=year[0],month=name)), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_month', 'year': year[0], 'month': name})))
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=year[0])), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_year', 'year': year[0]})))
                item.addContextMenuItems(contextmenu, replaceItems=True)
    	    else:
                url = build_url({'action': 'search_by_day', 'year': year[0], 'month': month[0], 'day': name})
                item = gui.ListItem(convert_timestamp(year=year[0],month=month[0],day=name), iconImage=Const.CALENDAR, thumbnailImage=Const.CALENDAR)
                contextmenu = []
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=year[0],month=month[0])), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_month', 'year': year[0], 'month': month[0]})))
                contextmenu.append((Const.STR(30012).format(period=convert_timestamp(year=year[0])), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_year', 'year': year[0]})))
                item.addContextMenuItems(contextmenu, replaceItems=True)
    	    plugin.addDirectoryItem(addon_handle, url, item, True)
    	    n += 1
    	return n

    def list_places(self):
    	n = 0
        map = Map()
    	places = self.db.GetPlaceList()
    	for (name, uuid, minLatitude, maxLatitude, minLongitude, maxLongitude) in places:
            url = build_url({'action': 'places', 'uuid': uuid})
            try:
                thumbnail = map.create((minLatitude, minLongitude), (maxLatitude, maxLongitude))
            except:
                thumbnail = Const.MARKER
            item = gui.ListItem(name, iconImage=thumbnail, thumbnailImage=thumbnail)
    	    plugin.addDirectoryItem(addon_handle, url, item, True)
    	    n += 1
    	return n

    def list_people(self):
    	n = 0
    	people = self.db.GetPersonList()
    	for (name, uuid, modelId) in people:
            url = build_url({'action': 'people', 'uuid': uuid})
            imagePath = glob.glob(os.path.join(self.photo_app_face_path, ('%04x' % modelId)[0:2], '00', 'facetile_%x.jpeg' % modelId))[-1]
            item = gui.ListItem(name, iconImage=imagePath, thumbnailImage=imagePath)
    	    plugin.addDirectoryItem(addon_handle, url, item, True)
    	    n += 1
    	return n

    def list_albums(self, folderUuid):
    	n = 0
    	folders = self.db.GetFolderList(folderUuid)
    	for (name, uuid) in folders:
            url = build_url({'action': 'albums', 'folderUuid': uuid})
            thumbnailPath = Const.PHOTO_GALLERY
            item = gui.ListItem(name, iconImage=thumbnailPath, thumbnailImage=thumbnailPath)
    	    plugin.addDirectoryItem(addon_handle, url, item, True)
    	    n += 1
    	albums = self.db.GetAlbumList(folderUuid)
    	for (name, uuid, modelId) in albums:
            url = build_url({'action': 'albums', 'uuid': uuid})
            thumbnailPath = glob.glob(os.path.join(self.photo_app_thumbnail_path, ('%04x' % modelId)[0:2], '00', '%x' % modelId, '*.jpg'))[-1]
            item = gui.ListItem(name, iconImage=thumbnailPath, thumbnailImage=thumbnailPath)
    	    plugin.addDirectoryItem(addon_handle, url, item, True)
    	    n += 1
    	return n

    def list_photos(self, uuid, action):
    	pictures = self.db.GetPictureList(uuid, action)
        heic = Const.GET('heic')
    	n = 0
    	for (imageDate, imagePath, isMissing, modelId, latitude, longitude) in pictures:
            thumbnailPath = glob.glob(os.path.join(self.photo_app_thumbnail_path, ('%04x' % modelId)[0:2], '00', '%x' % modelId, '*.jpg'))[-1]
            if isMissing == 0:
                imagePath = os.path.join(self.photo_app_picture_path, smart_utf8(imagePath))
            else:
                imagePath = thumbnailPath
            # replace heic images with thumbnails
            if imagePath.endswith('.HEIC') or imagePath.endswith('.heic'):
                if heic == '1':
                    imagePath = Cache().convert(imagePath)
                else:
                    imagePath = thumbnailPath
            item = gui.ListItem(convert_timestamp(timestamp=imageDate), iconImage=thumbnailPath, thumbnailImage=thumbnailPath)
            contextmenu = []
            contextmenu.append((Const.STR(30010), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_timestamp', 'timestamp': imageDate})))
            if latitude and longitude:
                contextmenu.append((Const.STR(30011), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_latlong', 'latitude': latitude, 'longitude': longitude})))
            contextmenu.append((Const.STR(30014), 'XBMC.Container.Update(%s,replace)' % build_url({})))
            item.addContextMenuItems(contextmenu, replaceItems=True)
    	    plugin.addDirectoryItem(addon_handle, imagePath, item, False)
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
            item = gui.ListItem(convert_timestamp(timestamp=imageDate), iconImage=thumbnailPath, thumbnailImage=thumbnailPath)
            contextmenu = []
            contextmenu.append((Const.STR(30010), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_timestamp', 'timestamp': imageDate})))
            if latitude and longitude:
                contextmenu.append((Const.STR(30011), 'XBMC.Container.Update(%s)' % build_url({'action': 'search_by_latlong', 'latitude': latitude, 'longitude': longitude})))
            contextmenu.append((Const.STR(30014), 'XBMC.Container.Update(%s,replace)' % build_url({})))
            item.addContextMenuItems(contextmenu, replaceItems=True)
    	    plugin.addDirectoryItem(addon_handle, imagePath, item, False)
    	    n += 1
    	return n

    def main_menu(self):
        url = build_url({'action': 'moments'})
        item = gui.ListItem(Const.STR(30001), iconImage=Const.PICTURE, thumbnailImage=Const.PICTURE)
    	plugin.addDirectoryItem(addon_handle, url, item, True)

        url = build_url({'action': 'people'})
        item = gui.ListItem(Const.STR(30003), iconImage=Const.PEOPLE, thumbnailImage=Const.PEOPLE)
    	plugin.addDirectoryItem(addon_handle, url, item, True)

        url = build_url({'action': 'places'})
        item = gui.ListItem(Const.STR(30002), iconImage=Const.MARKER, thumbnailImage=Const.MARKER)
    	plugin.addDirectoryItem(addon_handle, url, item, True)

        url = build_url({'action': 'videos'})
        item = gui.ListItem(Const.STR(30005), iconImage=Const.MOVIE, thumbnailImage=Const.MOVIE)
    	plugin.addDirectoryItem(addon_handle, url, item, True)

        url = build_url({'action': 'albums', 'folderUuid': 'TopLevelAlbums'})
        item = gui.ListItem(Const.STR(30004), iconImage=Const.PHOTO_GALLERY, thumbnailImage=Const.PHOTO_GALLERY)
    	plugin.addDirectoryItem(addon_handle, url, item, True)

    	return 4

if __name__ == '__main__':

    action_result = None
    items = 0

    log('argv[0] = %s' % sys.argv[0])
    log('argv[1] = %s' % sys.argv[1])
    log('argv[2] = %s' % sys.argv[2])

    action = args.get('action', None)
    folderUuid = args.get('folderUuid', None)
    uuid = args.get('uuid', None)
    year = args.get('year', None)
    month = args.get('month', None)
    day = args.get('day', None)

    timestamp = args.get('timestamp', None)
    latitude = args.get('latitude', None)
    longitude = args.get('longitude', None)

    app = App()
    app.open_db()

    if action is None:
        Cache().clear()
        items = app.main_menu()
    elif not (uuid is None):
        items = app.list_photos(uuid[0], action[0])
    elif action[0] == 'moments':
        items = app.list_moments(year, month)
    elif action[0] == 'people':
        items = app.list_people()
    elif action[0] == 'places':
        items = app.list_places()
    elif action[0] == 'videos':
        items = app.list_videos()
    elif action[0] == 'albums':
        items = app.list_albums(folderUuid[0])

    elif action[0] == 'search_by_year':
        items = app.list_photos((year[0]), action[0])
        mode = 'thumbnail'
    elif action[0] == 'search_by_month':
        items = app.list_photos((year[0], month[0]), action[0])
        mode = 'thumbnail'
    elif action[0] == 'search_by_day':
        items = app.list_photos((year[0], month[0], day[0]), action[0])
        mode = 'thumbnail'
    elif action[0] == 'search_by_timestamp':
        items = app.list_photos((timestamp[0]), action[0])
        mode = 'thumbnail'
    elif action[0] == 'search_by_latlong':
        items = app.list_photos((latitude[0], longitude[0]), action[0])
        mode = 'thumbnail'

    app.close_db()

    if items == 0:
        action_result = Const.STR(30100)
    else:
        plugin.endOfDirectory(addon_handle, True)

	xbmc.sleep(300)
    if action_result: notify(action_result)
