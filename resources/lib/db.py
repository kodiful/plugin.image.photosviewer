# -*- coding: utf-8 -*-

try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite

import sys
import os
import time
import locale

import xbmc
from common import *

class DB:

    def __init__(self, dbfile):
    	self.OpenDB(dbfile)

    def __del__(self):
        self.CloseDB()

    def OpenDB(self, dbfile):
        try:
    	    self.dbconn = sqlite.connect(dbfile)
    	except Exception, e:
    	    pass

    def CloseDB(self):
        try:
        	self.dbconn.close()
    	except Exception, e:
    	    pass

    def GetMomentList(self, year, month):
    	moment_list = []
    	cur = self.dbconn.cursor()
    	try:
    	    #SELECT strftime('%Y', startDate, 'unixepoch', 'localtime'), startDate FROM `RKMoment` WHERE  strftime('%Y', startDate, 'unixepoch', 'localtime') = '1974'
    	    if year is None:
    	        cur.execute("""SELECT strftime('%Y', startDate, 'unixepoch', 'localtime')+31, 0
    	                       FROM RKMoment
    	                       GROUP BY strftime('%Y', startDate, 'unixepoch', 'localtime')""")
    	    elif month is None:
    	        cur.execute("""SELECT strftime('%m', startDate, 'unixepoch', 'localtime'), 0
    	                       FROM RKMoment
    	                       WHERE strftime('%Y', startDate, 'unixepoch', 'localtime') = ?
    	                       GROUP BY strftime('%Y-%m', startDate, 'unixepoch', 'localtime')""", ('%s' % (int(year[0])-31),))
    	    else:
    	        cur.execute("""SELECT strftime('%d', startDate, 'unixepoch', 'localtime'), uuid
    	                       FROM RKMoment
    	                       WHERE strftime('%Y-%m', startDate, 'unixepoch', 'localtime') = ?
    	                       ORDER BY startDate""", ('%s-%s' % (int(year[0])-31, month[0]),))
    	    for row in cur:
                moment_list.append(row)
    	except Exception, e:
    	    print "photoapp.db: GetMomentList: " + smart_utf8(e)
    	    pass
    	cur.close()
    	return moment_list

    def GetPlaceList(self):
    	place_list = []
    	cur = self.dbconn.cursor()
    	try:
    	    cur.execute("""SELECT defaultName, uuid FROM RKPlace
                           WHERE type <= 16
    	                   ORDER BY type, defaultName ASC""")
    	    for row in cur:
                place_list.append(row)
    	except Exception, e:
    	    xbmc.log("photoapp.db: GetPlaceList: " + smart_utf8(e), level=xbmc.LOGERROR)
    	    pass
    	cur.close()
    	return place_list

    def GetPersonList(self):
    	person_list = []
    	cur = self.dbconn.cursor()
    	try:
    	    cur.execute("""SELECT p.name, p.uuid, m.modelId
                           FROM RKModelResource m, RKPerson p
                           WHERE m.attachedModelId = p.representativeFaceId
                           AND p.name != ""
    	                   ORDER BY p.name ASC""")
    	    for row in cur:
                person_list.append(row)
    	except Exception, e:
    	    xbmc.log("photoapp.db: GetPersonList: " + smart_utf8(e), level=xbmc.LOGERROR)
    	    pass
    	cur.close()
    	return person_list

    def GetVideoList(self):
    	video_list = []
    	cur = self.dbconn.cursor()
    	try:
            cur.execute("""SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId
                           FROM RKMaster m, RKVersion v
                           WHERE m.uuid = v.masterUuid
                           AND m.isMissing = 0 AND v.naturalDuration > 0
                           ORDER BY m.imageDate ASC""")
    	    for row in cur:
                video_list.append(row)
    	except Exception, e:
    	    print "photoapp.db: GetVideoList: " + smart_utf8(e)
    	    pass
    	cur.close()
    	return video_list

    def GetFolderList(self, folderUuid):
    	folder_list = []
    	cur = self.dbconn.cursor()
    	try:
    	    cur.execute("""SELECT f.name, f.uuid
                           FROM RKFolder f
                           WHERE f.isHidden = 0 AND f.isInTrash = 0 AND f.parentFolderUuid = ?
    	                   ORDER BY f.name ASC""", (folderUuid,))
    	    for row in cur:
                folder_list.append(row)
    	except Exception, e:
    	    print "photoapp.db: GetFolderList: " + smart_utf8(e)
    	    pass
    	cur.close()
    	return folder_list

    def GetAlbumList(self, folderUuid):
    	album_list = []
    	cur = self.dbconn.cursor()
    	try:
    	    cur.execute("""SELECT a.name, a.uuid, v.modelId
                           FROM RKVersion v, RKAlbum a
                           WHERE v.uuid = a.posterVersionUuid
                           AND a.isHidden = 0 AND a.isInTrash = 0 AND a.customSortAvailable = 1 AND a.folderUuid = ?
    	                   ORDER BY a.name ASC""", (folderUuid,))
    	    for row in cur:
                album_list.append(row)
    	except Exception, e:
    	    print "photoapp.db: GetAlbumList: " + smart_utf8(e)
    	    pass
    	cur.close()
    	return album_list

    def GetPictureList(self, uuid, action):
    	picture_list = []
    	cur = self.dbconn.cursor()
    	try:
    	    if action == 'moments':
    	        cur.execute("""SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId
    	                       FROM RKMaster m, RKVersion v
    	                       WHERE m.uuid = v.masterUuid
    	                       AND v.momentUuid = ?
                               ORDER BY m.imageDate ASC""", (uuid,))
    	    elif action == 'people':
    	        cur.execute("""SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId
    	                       FROM RKMaster m, RKVersion v, RKFace f, RKPerson p
    	                       WHERE m.uuid = v.masterUuid
    	                       AND v.modelId = f.imageModelId
                               AND f.personId = p.modelId
                               AND p.uuid = ?
                               ORDER BY m.imageDate ASC""", (uuid,))
    	    elif action == 'places':
    	        cur.execute("""SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId
    	                       FROM RKMaster m, RKVersion v, RKPlace p
    	                       WHERE m.uuid = v.masterUuid
                               AND v.latitude > p.minLatitude
                               AND v.latitude < p.maxLatitude
                               AND v.longitude > p.minLongitude
                               AND v.longitude < p.maxLongitude
                               AND p.uuid = ?
                               ORDER BY m.imageDate ASC""", (uuid,))
    	    else:
    	        cur.execute("""SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId
    	                       FROM RKMaster m, RKVersion v, RKCustomSortOrder o
    	                       WHERE m.uuid = v.masterUuid
                               AND v.Uuid = o.objectUuid
                               AND o.containerUuid = ?
                               ORDER BY m.imageDate ASC""", (uuid,))
    	    for row in cur:
                picture_list.append(row)
    	except Exception, e:
    	    print "photoapp.db: GetPictureList: " + smart_utf8(e)
    	    pass
    	cur.close()
    	return picture_list
