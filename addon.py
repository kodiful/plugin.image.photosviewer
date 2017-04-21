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

addon = xbmcaddon.Addon()

plugin_path = addon.getAddonInfo("path")
resource_path = os.path.join(plugin_path, "resources")
lib_path = os.path.join(resource_path, "lib")
sys.path.append(lib_path)

base_url = sys.argv[0]
addon_handle = int(sys.argv[1])
args = urlparse.parse_qs(sys.argv[2][1:])

def build_url(query):
    return base_url + '?' + urllib.urlencode(query)

class App:

    def __init__(self):
        # パラメータ
    	self.params = {}
        qs = urlparse.parse_qs(urlparse.urlparse(sys.argv[2]).query, keep_blank_values=True)
        for key in qs.keys():
            self.params[key] = qs[key][0]
            log_notice('init:params %s=%s' % (key,self.params[key]))

        # 写真アプリのパス
        self.photo_app_path = addon.getSetting('photo_library_path')
        if self.photo_app_path == '':
            self.photo_app_path = os.path.join(os.getenv('HOME'), 'Pictures', addon.getLocalizedString(30000))
        addon.setSetting('photo_library_path', self.photo_app_path)
        # photos.dbをチェック
        self.photo_app_db_file = os.path.join(xbmc.translatePath(addon.getAddonInfo('Profile')), 'photos.db')
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
    	for (name, uuid) in moments:
    	    print "app: moment: %s" % (name)
    	    if year is None:
               url = build_url({'action': 'moments', 'year': name})
               item = gui.ListItem('%s' % (int(name)), iconImage='DefaultYear.png', thumbnailImage='DefaultYear.png')
    	    elif month is None:
               url = build_url({'action': 'moments', 'year': year[0], 'month': name})
               item = gui.ListItem('%s-%s' % (int(year[0]), name), iconImage='DefaultYear.png', thumbnailImage='DefaultYear.png')
            else:
               url = build_url({'action': 'moments', 'year': year[0], 'month': month[0], 'day': name, 'uuid': uuid})
               item = gui.ListItem('%s-%s-%s' % (int(year[0]), month[0], name), iconImage='DefaultYear.png', thumbnailImage='DefaultYear.png')
    	    plugin.addDirectoryItem(addon_handle, url, item, True)
    	    n += 1
    	return n

    def list_places(self):
    	n = 0
    	places = self.db.GetPlaceList()
    	for (name, uuid) in places:
            url = build_url({'action': 'places', 'uuid': uuid})
            item = gui.ListItem(name, iconImage='DefaultCountry.png', thumbnailImage='DefaultCountry.png')
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
            thumbnailPath = 'DefaultFolder.png'
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
    	n = 0
    	for (imageDate, imagePath, isMissing, modelId) in pictures:
            thumbnailPath = glob.glob(os.path.join(self.photo_app_thumbnail_path, ('%04x' % modelId)[0:2], '00', '%x' % modelId, '*.jpg'))[-1]
            if isMissing == 0:
                imagePath = os.path.join(self.photo_app_picture_path, smart_utf8(imagePath))
            else:
                imagePath = thumbnailPath
            item = gui.ListItem(convert_timestamp(imageDate), iconImage=thumbnailPath, thumbnailImage=thumbnailPath)
    	    plugin.addDirectoryItem(addon_handle, imagePath, item, False)
    	    n += 1
    	return n

    def list_videos(self):
    	n = 0
    	videos = self.db.GetVideoList()
    	for (imageDate, imagePath, isMissing, modelId) in videos:
            thumbnailPath = glob.glob(os.path.join(self.photo_app_thumbnail_path, ('%04x' % modelId)[0:2], '00', '%x' % modelId, '*.jpg'))[-1]
            if isMissing == 0:
                imagePath = os.path.join(self.photo_app_picture_path, smart_utf8(imagePath))
            else:
                imagePath = thumbnailPath
            item = gui.ListItem(convert_timestamp(imageDate), iconImage=thumbnailPath, thumbnailImage=thumbnailPath)
    	    plugin.addDirectoryItem(addon_handle, imagePath, item, False)
    	    n += 1
    	return n

    def main_menu(self):
        url = build_url({'action': 'moments'})
        item = gui.ListItem(addon.getLocalizedString(30001), iconImage='DefaultPicture.png', thumbnailImage='DefaultPicture.png')
    	plugin.addDirectoryItem(addon_handle, url, item, True)

        url = build_url({'action': 'people'})
        item = gui.ListItem(addon.getLocalizedString(30003), iconImage='DefaultUser.png', thumbnailImage='DefaultUser.png')
    	plugin.addDirectoryItem(addon_handle, url, item, True)

        url = build_url({'action': 'places'})
        item = gui.ListItem(addon.getLocalizedString(30002), iconImage='DefaultCountry.png', thumbnailImage='DefaultCountry.png')
    	plugin.addDirectoryItem(addon_handle, url, item, True)

        url = build_url({'action': 'videos'})
        item = gui.ListItem(addon.getLocalizedString(30005), iconImage='DefaultVideo.png', thumbnailImage='DefaultVideo.png')
    	plugin.addDirectoryItem(addon_handle, url, item, True)

        url = build_url({'action': 'albums', 'folderUuid': 'TopLevelAlbums'})
        item = gui.ListItem(addon.getLocalizedString(30004), iconImage='DefaultFolder.png', thumbnailImage='DefaultFolder.png')
    	plugin.addDirectoryItem(addon_handle, url, item, True)

    	return 4

if __name__ == '__main__':

    action_result = None
    items = 0

    action = args.get('action', None)
    folderUuid = args.get('folderUuid', None)
    uuid = args.get('uuid', None)
    year = args.get('year', None)
    month = args.get('month', None)

    app = App()
    app.open_db()

    if action is None:
        items = app.main_menu()
        set_view('thumbnail')
    elif not (uuid is None):
        items = app.list_photos(uuid[0], action[0])
        set_view('thumbnail')
    elif action[0] == 'moments':
        items = app.list_moments(year, month)
        set_view('list')
    elif action[0] == 'people':
        items = app.list_people()
        set_view('thumbnail')
    elif action[0] == 'places':
        items = app.list_places()
        set_view('list')
    elif action[0] == 'videos':
        items = app.list_videos()
        set_view('thumbnail')
    elif action[0] == 'albums':
        items = app.list_albums(folderUuid[0])
        set_view('thumbnail')

    app.close_db()

    if items == 0:
        action_result = addon.getLocalizedString(30100)
    else:
        plugin.endOfDirectory(addon_handle, True)

	xbmc.sleep(300)
    if action_result: notify(action_result)
