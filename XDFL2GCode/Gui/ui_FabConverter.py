# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_FabConverter.ui'
#
# Created: Sat Jun 05 00:08:13 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_FabConverter(object):
    def setupUi(self, FabConverter):
        FabConverter.setObjectName("FabConverter")
        FabConverter.resize(675, 506)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/favicon.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        FabConverter.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(FabConverter)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_4 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtGui.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.fabFileEdit = QtGui.QTextEdit(self.centralwidget)
        self.fabFileEdit.setReadOnly(True)
        self.fabFileEdit.setObjectName("fabFileEdit")
        self.verticalLayout_2.addWidget(self.fabFileEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtGui.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.makerbotButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.makerbotButton.sizePolicy().hasHeightForWidth())
        self.makerbotButton.setSizePolicy(sizePolicy)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/makerbot.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.makerbotButton.setIcon(icon1)
        self.makerbotButton.setIconSize(QtCore.QSize(70, 70))
        self.makerbotButton.setObjectName("makerbotButton")
        self.verticalLayout.addWidget(self.makerbotButton)
        spacerItem = QtGui.QSpacerItem(78, 28, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.repRapButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.repRapButton.sizePolicy().hasHeightForWidth())
        self.repRapButton.setSizePolicy(sizePolicy)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/reprap.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.repRapButton.setIcon(icon2)
        self.repRapButton.setIconSize(QtCore.QSize(70, 70))
        self.repRapButton.setObjectName("repRapButton")
        self.verticalLayout.addWidget(self.repRapButton)
        spacerItem1 = QtGui.QSpacerItem(78, 18, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.rapManButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rapManButton.sizePolicy().hasHeightForWidth())
        self.rapManButton.setSizePolicy(sizePolicy)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/BFB3k.jpg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rapManButton.setIcon(icon3)
        self.rapManButton.setIconSize(QtCore.QSize(70, 70))
        self.rapManButton.setObjectName("rapManButton")
        self.verticalLayout.addWidget(self.rapManButton)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_2 = QtGui.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_3.addWidget(self.label_2)
        self.gcodeTextEdit = QtGui.QTextEdit(self.centralwidget)
        self.gcodeTextEdit.setObjectName("gcodeTextEdit")
        self.verticalLayout_3.addWidget(self.gcodeTextEdit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_3)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.loadFabFileButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.loadFabFileButton.sizePolicy().hasHeightForWidth())
        self.loadFabFileButton.setSizePolicy(sizePolicy)
        self.loadFabFileButton.setObjectName("loadFabFileButton")
        self.horizontalLayout.addWidget(self.loadFabFileButton)
        spacerItem2 = QtGui.QSpacerItem(90, 20, QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.saveAsButton = QtGui.QPushButton(self.centralwidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.saveAsButton.sizePolicy().hasHeightForWidth())
        self.saveAsButton.setSizePolicy(sizePolicy)
        self.saveAsButton.setObjectName("saveAsButton")
        self.horizontalLayout.addWidget(self.saveAsButton)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        FabConverter.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(FabConverter)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 675, 21))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtGui.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        FabConverter.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(FabConverter)
        self.statusbar.setObjectName("statusbar")
        FabConverter.setStatusBar(self.statusbar)
        self.aboutAction = QtGui.QAction(FabConverter)
        self.aboutAction.setObjectName("aboutAction")
        self.menuAbout.addAction(self.aboutAction)
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(FabConverter)
        QtCore.QMetaObject.connectSlotsByName(FabConverter)

    def retranslateUi(self, FabConverter):
        FabConverter.setWindowTitle(QtGui.QApplication.translate("FabConverter", "XDFL File to G-Code Converter", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("FabConverter", "XDFL File", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("FabConverter", "Printer", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("FabConverter", "G-Code", None, QtGui.QApplication.UnicodeUTF8))
        self.loadFabFileButton.setText(QtGui.QApplication.translate("FabConverter", "Load XDFL File", None, QtGui.QApplication.UnicodeUTF8))
        self.saveAsButton.setText(QtGui.QApplication.translate("FabConverter", "Save As", None, QtGui.QApplication.UnicodeUTF8))
        self.menuAbout.setTitle(QtGui.QApplication.translate("FabConverter", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.aboutAction.setText(QtGui.QApplication.translate("FabConverter", "About", None, QtGui.QApplication.UnicodeUTF8))

import FabConverter_rc