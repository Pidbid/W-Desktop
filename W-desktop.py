# -*- encoding: utf-8 -*-
'''
@File    :   W-desktop.py
@Time    :   2020/12/15 21:48:03
@Author  :   Wicos 
@Version :   1.0
@Contact :   wicos@wicos.cn
@Blog    :   https://www.wicos.me
'''

# here put the import lib
import os
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from module import scan


class GUI(QMainWindow):
    def __init__(self):
        super(GUI, self).__init__()
        self.initGui()
        self.thread()

    def initGui(self):
        self.resize(380, 400)
        self.setMaximumSize(380, 400)
        self.setMinimumSize(380, 400)
        self.setWindowTitle("W-Desktop桌面添加")
        self.setWindowIcon(QIcon(os.getcwd() + "/static/icon/icon.png"))
        self.statusbar = self.statusBar()
        self.center()
        self.input()
        self.btn()
        self.label()
        self.radiobtn()
        self.textbox()
        
    def thread(self):
        self.files = []
        self.scan = scan.SCAN()
        self.scan.start()
        self.scan.trg.connect(self.fun_files)

    def center(self):
        screen = QDesktopWidget().screenGeometry()
        form = self.geometry()
        x_move_step = (screen.width() - form.width()) / 2
        y_move_step = (screen.height() - form.height()) / 2
        self.move(int(x_move_step), int(y_move_step))

    def radiobtn(self):
        self.rbtn_application = QRadioButton("Application", self)
        self.rbtn_application.resize(110, 25)
        self.rbtn_application.move(10, 100)
        self.rbtn_directory = QRadioButton("Directory", self)
        self.rbtn_directory.resize(110, 25)
        self.rbtn_directory.move(130, 100)
        self.rbtn_link = QRadioButton("Link", self)
        self.rbtn_link.resize(110, 25)
        self.rbtn_link.move(230, 100)

    def label(self):
        self.label_type = QLabel("选择文件类型：", self)
        self.label_type.resize(100, 25)
        self.label_type.move(10, 75)

    def textbox(self):
        self.txt_scan = QTextEdit(self)
        self.txt_scan.resize(360, 220)
        self.txt_scan.move(10, 160)

    def btn(self):
        self.btn_selectfile = QPushButton("选择", self)
        self.btn_selectfile.clicked.connect(self.fun_select_runfile)
        self.btn_selectfile.resize(50, 25)
        self.btn_selectfile.move(320, 10)
        self.btn_selectico = QPushButton("选择", self)
        self.btn_selectico.clicked.connect(self.fun_select_ico)
        self.btn_selectico.resize(50, 25)
        self.btn_selectico.move(240, 45)
        self.btn_icoonline = QPushButton("图标扫描", self)
        self.btn_icoonline.clicked.connect(self.fun_scanico)
        self.btn_icoonline.resize(70, 25)
        self.btn_icoonline.move(300, 45)
        self.btn_preview = QPushButton("预览", self)
        self.btn_preview.clicked.connect(self.fun_preview)
        self.btn_preview.resize(100, 30)
        self.btn_preview.move(80, 125)
        self.btn_add = QPushButton("添加", self)
        self.btn_add.clicked.connect(self.fun_add)
        self.btn_add.resize(100, 30)
        self.btn_add.move(190, 125)

    def input(self):
        self.input_runfile = QLineEdit(self)
        self.input_runfile.setPlaceholderText("可运行文件路径")
        self.input_runfile.resize(300, 25)
        self.input_runfile.move(10, 10)
        self.input_icofile = QLineEdit(self)
        self.input_icofile.setPlaceholderText("运行图标路径")
        self.input_icofile.resize(220, 25)
        self.input_icofile.move(10, 45)
        
    def fun_files(self,filelist):
        self.files = filelist

    def fun_select_runfile(self):
        self.select_file = QFileDialog.getOpenFileName(
            self, "getOpenFileName", "./", "Files (*)")
        self.input_runfile.setText(str(self.select_file[0]))

    def fun_select_ico(self):
        self.select_file = QFileDialog.getOpenFileName(
            self, "getOpenFileName", "./", "ICO Files (*.ico)")
        self.input_icofile.setText(str(self.select_file[0]))

    def fun_preview(self):
        if self.input_runfile.text() == "" or self.input_icofile.text() == "":
            QMessageBox.information(
                self, '提示', '请检查是否选择运行文件或图标文件', QMessageBox.Yes)
        elif self.rbtn_directory.isChecked() + self.rbtn_application.isChecked() + self.rbtn_link.isChecked() == 0:
            QMessageBox.information(
                self, '提示', '请选择一个文件类型', QMessageBox.Yes)
        else:
            link_select = False
            self.link_url = ""
            self.dsk_name = os.path.splitext(self.input_runfile.text())[
                0].split("/")[-1]
            types = "Application"
            if self.rbtn_link.isChecked():
                types = "Link"
                self.link_url,link_select = QInputDialog.getText(self, '输入提示', '输入URL：')
            elif self.rbtn_directory.isChecked():
                types = "Directory"
            desktops = "[Desktop Entry]\nName=" + self.dsk_name + "\nType=" + types + "\nExec=" + self.input_runfile.text() + "\nIcon=" + self.input_icofile.text()
            if link_select:
                desktops = desktops + "\nUrl=" + self.link_url
            self.txt_scan.setPlainText(desktops)
            
    def fun_add(self):
        if self.txt_scan.toPlainText() != "":
            filepath = "/usr/share/applications/" + self.dsk_name + ".desktop"
            this_file = self.dsk_name + ".desktop"
            if this_file in self.files:
                QMessageBox.information(
                self, '提示', '已存在同名应用，请修改应用名称。', QMessageBox.Yes)
            else:
                self.statusbar.showMessage("正在添加应用……")
                with open(filepath,"w") as dsk:
                    dsk.write(self.txt_scan.toPlainText())
                self.statusbar.showMessage("添加完毕")
                
    def fun_scanico(self):
        QMessageBox.information(
                self, '提示', '功能待开发', QMessageBox.Yes)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    gui = GUI()
    gui.show()
    sys.exit(app.exec_())
