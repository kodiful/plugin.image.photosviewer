# -*- coding: utf-8 -*-

import os
import xbmc, xbmcaddon

class Const:

    # ガラポンTVクライアント
    ADDON = xbmcaddon.Addon()
    ADDON_ID = ADDON.getAddonInfo('id')
    BASE_URL = 'plugin://%s' % ADDON_ID

    STR = ADDON.getLocalizedString
    GET = ADDON.getSetting
    SET = ADDON.setSetting

    # ディレクトリパス
    PROFILE_PATH = xbmc.translatePath(ADDON.getAddonInfo('profile').decode('utf-8'))
    PLUGIN_PATH = xbmc.translatePath(ADDON.getAddonInfo('path').decode('utf-8'))
    RESOURCES_PATH = os.path.join(PLUGIN_PATH, 'resources')
    DATA_PATH = os.path.join(RESOURCES_PATH, 'data')
    IMAGE_PATH = os.path.join(DATA_PATH, 'image')

    # サムネイル
    PICTURE       = os.path.join(IMAGE_PATH, 'icons8-picture-filled-500.png')
    PEOPLE        = os.path.join(IMAGE_PATH, 'icons8-people-filled-500.png')
    MARKER        = os.path.join(IMAGE_PATH, 'icons8-marker-filled-500.png')
    MOVIE         = os.path.join(IMAGE_PATH, 'icons8-movie-filled-500.png')
    PHOTO_GALLERY = os.path.join(IMAGE_PATH, 'icons8-photo-gallery-filled-500.png')
    CALENDAR      = os.path.join(IMAGE_PATH, 'icons8-calendar-filled-500.png')
