# -*- encoding: utf-8 -*-
'''
@File    :   scan.py
@Time    :   2020/12/16 00:48:23
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
from PyQt5.QtCore import QThread, pyqtSignal
import os

class SCAN(QThread):
    trg = pyqtSignal(list)
    def __init__(self):
        super(SCAN,self).__init__()
        self.signal = True
        
    def run(self):
        while self.signal:
            dirlist = os.listdir("/usr/share/applications")
            self.trg.emit(dirlist)
            self.signal = False
        