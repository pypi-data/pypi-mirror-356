# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CNMapViewer.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import resources_rc as resources_rc


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(400, 400)
        MainWindow.setMinimumSize(QSize(400, 400))
        self.action_New = QAction(MainWindow)
        self.action_New.setObjectName("action_New")
        self.actionaboutQt = QAction(MainWindow)
        self.actionaboutQt.setObjectName("actionaboutQt")
        self.actionTEST = QAction(MainWindow)
        self.actionTEST.setObjectName("actionTEST")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.label.setGeometry(QRect(50, 80, 128, 128))
        self.label.setPixmap(QPixmap(":/assets/icons/add.ico"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 400, 22))
        self.menu_File = QMenu(self.menubar)
        self.menu_File.setObjectName("menu_File")
        self.menu_Edit = QMenu(self.menubar)
        self.menu_Edit.setObjectName("menu_Edit")
        self.menu_About = QMenu(self.menubar)
        self.menu_About.setObjectName("menu_About")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_About.menuAction())
        self.menu_File.addAction(self.action_New)
        self.menu_Edit.addAction(self.actionTEST)
        self.menu_About.addAction(self.actionaboutQt)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        self.action_New.setText(QCoreApplication.translate("MainWindow", "&New", None))
        self.actionaboutQt.setText(
            QCoreApplication.translate("MainWindow", "aboutQt", None)
        )
        self.actionTEST.setText(QCoreApplication.translate("MainWindow", "TEST", None))
        self.menu_File.setTitle(QCoreApplication.translate("MainWindow", "&File", None))
        self.menu_Edit.setTitle(QCoreApplication.translate("MainWindow", "&Edit", None))
        self.menu_About.setTitle(
            QCoreApplication.translate("MainWindow", "&About", None)
        )

    # retranslateUi
