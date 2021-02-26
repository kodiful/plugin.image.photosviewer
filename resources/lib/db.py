# -*- coding: utf-8 -*-

from sqlite3 import dbapi2 as sqlite

from resources.lib.common import log


class DB:

    def __init__(self, dbfile):
        self.OpenDB(dbfile)

    def __del__(self):
        self.CloseDB()

    def OpenDB(self, dbfile):
        try:
            self.dbconn = sqlite.connect(dbfile)
        except Exception as e:
            log('db error: %s' % e, error=True)

    def CloseDB(self):
        try:
            self.dbconn.close()
        except Exception as e:
            log('db error: %s' % e, error=True)

    def GetMomentList(self, year, month):
        moment_list = []
        cur = self.dbconn.cursor()
        try:
            if year is None:
                cur.execute('''SELECT strftime('%Y', imageDate+978307200, 'unixepoch', 'localtime') as year
                               FROM RKMaster m
                               WHERE m.isInTrash = 0
                               GROUP BY year
                               ORDER BY imageDate
                               ''')
            elif month is None:
                cur.execute('''SELECT strftime('%m', imageDate+978307200, 'unixepoch', 'localtime') as month
                               FROM RKMaster m
                               WHERE m.isInTrash = 0
                               AND strftime('%Y', imageDate+978307200, 'unixepoch', 'localtime') = ?
                               GROUP BY month
                               ORDER BY imageDate
                               ''', ('%s' % (year),))
            else:
                cur.execute('''SELECT strftime('%d', imageDate+978307200, 'unixepoch', 'localtime') as day
                               FROM RKMaster m
                               WHERE m.isInTrash = 0
                               AND strftime('%Y-%m', imageDate+978307200, 'unixepoch', 'localtime') = ?
                               GROUP BY day
                               ORDER BY imageDate
                               ''', ('%s-%s' % (year, month),))
            for row in cur:
                moment_list.append(row)
        except Exception as e:
            log('db error: %s' % e, error=True)
        cur.close()
        return moment_list

    def GetPlaceList(self, parent=None):
        place_list = []
        cur = self.dbconn.cursor()
        try:
            if parent is None:
                cur.execute('''SELECT defaultName, uuid, type, modelId, minLatitude, maxLatitude, minLongitude, maxLongitude FROM RKPlace
                               WHERE type = 1
                               ORDER BY defaultName ASC''')
            else:
                (name, uuid, type, modelId) = parent
                if type == 1:
                    to = 2
                elif type == 2:
                    type = 4
                    to = 16
                else:
                    to = 100
                cur.execute('''SELECT DISTINCT p.defaultName, p.uuid, p.type, p.modelId, p.minLatitude, p.maxLatitude, p.minLongitude, p.maxLongitude FROM RKPlaceForVersion pv, RKPlace p
                               WHERE pv.versionId IN (SELECT versionId FROM RKPlaceForVersion WHERE placeId=?)
                               AND p.modelId = pv.placeId
                               AND p.type > ? AND p.type <= ?
                               ORDER BY p.minLatitude+p.maxLatitude+p.minLatitude+p.maxLongitude DESC''', (modelId, type, to,))
            for row in cur:
                place_list.append(row)
        except Exception as e:
            log('db error: %s' % e, error=True)
        cur.close()
        return place_list

    def GetPersonList(self):
        person_list = []
        cur = self.dbconn.cursor()
        try:
            cur.execute('''SELECT p.name, p.uuid, m.modelId
                           FROM RKModelResource m, RKPerson p
                           WHERE m.attachedModelId = p.representativeFaceId
                           AND p.name != ""
                           ORDER BY p.name ASC''')
            for row in cur:
                person_list.append(row)
        except Exception as e:
            log('db error: %s' % e, error=True)
        cur.close()
        return person_list

    def GetFolderList(self, folderUuid):
        folder_list = []
        cur = self.dbconn.cursor()
        try:
            cur.execute('''SELECT f.name, f.uuid
                           FROM RKFolder f
                           WHERE f.isHidden = 0 AND f.isInTrash = 0 AND f.parentFolderUuid = ?
                           ORDER BY f.name ASC''', (folderUuid,))
            for row in cur:
                folder_list.append(row)
        except Exception as e:
            log('db error: %s' % e, error=True)
        cur.close()
        return folder_list

    def GetAlbumList(self, folderUuid):
        album_list = []
        cur = self.dbconn.cursor()
        try:
            cur.execute('''SELECT a.name, a.uuid, v.modelId
                           FROM RKVersion v, RKAlbum a
                           WHERE v.uuid = a.posterVersionUuid
                           AND a.isHidden = 0 AND a.isInTrash = 0 AND a.customSortAvailable = 1 AND a.folderUuid = ?
                           ORDER BY a.name ASC''', (folderUuid,))
            for row in cur:
                album_list.append(row)
        except Exception as e:
            log('db error: %s' % e, error=True)
        cur.close()
        return album_list

    def GetVideoList(self):
        video_list = []
        cur = self.dbconn.cursor()
        try:
            cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude
                           FROM RKMaster m, RKVersion v
                           WHERE m.uuid = v.masterUuid
                           AND m.isInTrash = 0 AND m.isMissing = 0 AND v.naturalDuration > 0
                           ORDER BY m.imageDate ASC''')
            for row in cur:
                video_list.append(row)
        except Exception as e:
            log('db error: %s' % e, error=True)
        cur.close()
        return video_list

    def GetPictureList(self, uuid, action):
        picture_list = []
        cur = self.dbconn.cursor()
        try:
            if action == 'moments':
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND m.uuid = ?
                               GROUP BY m.uuid
                               ORDER BY m.imageDate ASC''', (uuid,))
            elif action == 'people':
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v, RKFace f, RKPerson p
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND v.modelId = f.imageModelId
                               AND f.personId = p.modelId
                               AND p.uuid = ?
                               GROUP BY m.uuid
                               ORDER BY m.imageDate ASC''', (uuid,))
            elif action == 'places':
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v, RKPlace p, RKPLaceForVersion pv
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND v.modelId = pv.versionId
                               AND pv.placeId = p.modelId
                               AND p.uuid = ?
                               GROUP BY m.uuid
                               ORDER BY m.imageDate ASC''', (uuid,))
            elif action == 'search_by_year':
                (year) = uuid
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND strftime('%Y', m.imageDate+978307200, 'unixepoch', 'localtime') = ?
                               GROUP BY m.uuid
                               ORDER BY m.imageDate ASC''', ('%s' % (year),))
            elif action == 'search_by_month':
                (year, month) = uuid
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND strftime('%Y-%m', m.imageDate+978307200, 'unixepoch', 'localtime') = ?
                               GROUP BY m.uuid
                               ORDER BY m.imageDate ASC''', ('%s-%s' % (year, month),))
            elif action == 'search_by_day':
                (year, month, day) = uuid
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND strftime('%Y-%m-%d', m.imageDate+978307200, 'unixepoch', 'localtime') = ?
                               GROUP BY m.uuid
                               ORDER BY m.imageDate ASC''', ('%s-%s-%s' % (year, month, day),))
            elif action == 'search_by_timestamp':
                (timestamp) = uuid
                cur1 = self.dbconn.cursor()
                cur1.execute('''SELECT strftime('%Y-%m-%d', ? + 978307200, 'unixepoch', 'localtime')''', ('%d' % (int(float(timestamp))),))
                (date) = cur1.fetchone()
                cur1.close()
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND strftime('%Y-%m-%d', m.imageDate+978307200, 'unixepoch', 'localtime') = ?
                               GROUP BY m.uuid
                               ORDER BY m.imageDate ASC''', (date[0],))
            elif action == 'search_by_latlong':
                (latitude, longitude) = uuid
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND v.latitude != ""
                               AND v.longitude != ""
                               GROUP BY m.uuid
                               ORDER BY abs(v.latitude - ?) + abs(v.longitude - ?) ASC LIMIT 100''', (latitude, longitude,))
            else:
                cur.execute('''SELECT m.imageDate, m.imagePath, m.isMissing, v.modelId, v.latitude, v.longitude, v.orientation
                               FROM RKMaster m, RKVersion v, RKCustomSortOrder o
                               WHERE m.uuid = v.masterUuid
                               AND m.isInTrash = 0
                               AND v.Uuid = o.objectUuid
                               AND o.containerUuid = ?
                               GROUP BY m.uuid
                               ORDER BY m.imageDate ASC''', (uuid,))
            for row in cur:
                picture_list.append(row)
        except Exception as e:
            log('db error: %s' % e, error=True)
        cur.close()
        return picture_list
