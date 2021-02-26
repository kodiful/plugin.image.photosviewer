# -*- coding: utf-8 -*-

import os
import subprocess
import hashlib

from resources.lib.const import Const


class Cache:

    def __init__(self):
        # ディレクトリ
        self.path = os.path.join(Const.PROFILE_PATH, 'cache', 'heic2jpeg')
        # ディレクトリが無ければ作成
        if not os.path.isdir(self.path):
            os.makedirs(self.path)

    def clear(self):
        files = os.listdir(self.path)
        for filename in files:
            os.remove(os.path.join(self.path, filename))

    def convert(self, infile):
        # 出力ファイル
        outfile = os.path.join(self.path, '%s.jpeg' % (hashlib.md5(infile).hexdigest()))
        # 画像変換実行
        if not os.path.isfile(outfile):
            command = 'sips --setProperty format jpeg "{infile}" --out "{outfile}"'.format(infile=infile, outfile=outfile)
            subprocess.call(command, shell=True)
        return outfile
