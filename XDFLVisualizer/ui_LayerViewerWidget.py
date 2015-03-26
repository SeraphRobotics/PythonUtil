# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_LayerViewerWidget.ui'
#
# Created: Fri Jun 25 01:08:48 2010
#      by: PyQt4 UI code generator 4.5.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_LayerViewWidget(object):
    def setupUi(self, LayerViewWidget):
        LayerViewWidget.setObjectName("LayerViewWidget")
        LayerViewWidget.resize(396, 300)
        self.horizontalLayout = QtGui.QHBoxLayout(LayerViewWidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.layerView = QtGui.QGraphicsView(LayerViewWidget)
        self.layerView.setObjectName("layerView")
        self.horizontalLayout.addWidget(self.layerView)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtGui.QLabel(LayerViewWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.layerSpin = QtGui.QSpinBox(LayerViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layerSpin.sizePolicy().hasHeightForWidth())
        self.layerSpin.setSizePolicy(sizePolicy)
        self.layerSpin.setMinimumSize(QtCore.QSize(0, 30))
        self.layerSpin.setObjectName("layerSpin")
        self.verticalLayout_2.addWidget(self.layerSpin)
        self.layerSlider = QtGui.QSlider(LayerViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layerSlider.sizePolicy().hasHeightForWidth())
        self.layerSlider.setSizePolicy(sizePolicy)
        self.layerSlider.setMinimumSize(QtCore.QSize(40, 0))
        self.layerSlider.setProperty("value", QtCore.QVariant(0))
        self.layerSlider.setOrientation(QtCore.Qt.Vertical)
        self.layerSlider.setObjectName("layerSlider")
        self.verticalLayout_2.addWidget(self.layerSlider)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(LayerViewWidget)
        QtCore.QObject.connect(self.layerSpin, QtCore.SIGNAL("valueChanged(int)"), self.layerSlider.setValue)
        QtCore.QObject.connect(self.layerSlider, QtCore.SIGNAL("valueChanged(int)"), self.layerSpin.setValue)
        QtCore.QMetaObject.connectSlotsByName(LayerViewWidget)

    def retranslateUi(self, LayerViewWidget):
        LayerViewWidget.setWindowTitle(QtGui.QApplication.translate("LayerViewWidget", "Layer Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("LayerViewWidget", "Layer", None, QtGui.QApplication.UnicodeUTF8))

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_LayerViewerWidget.ui'
#
# Created: Mon Mar 31 12:55:17 2014
#      by: PyQt4 UI code generator 4.9.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_LayerViewWidget(object):
    def setupUi(self, LayerViewWidget):
        LayerViewWidget.setObjectName(_fromUtf8("LayerViewWidget"))
        LayerViewWidget.resize(391, 358)
        self.verticalLayout = QtGui.QVBoxLayout(LayerViewWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.fileButton = QtGui.QPushButton(LayerViewWidget)
        self.fileButton.setObjectName(_fromUtf8("fileButton"))
        self.horizontalLayout.addWidget(self.fileButton)
        self.fileLineEdit = QtGui.QLineEdit(LayerViewWidget)
        self.fileLineEdit.setObjectName(_fromUtf8("fileLineEdit"))
        self.horizontalLayout.addWidget(self.fileLineEdit)
        spacerItem = QtGui.QSpacerItem(48, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.layerView = QtGui.QGraphicsView(LayerViewWidget)
        self.layerView.setObjectName(_fromUtf8("layerView"))
        self.horizontalLayout_2.addWidget(self.layerView)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label = QtGui.QLabel(LayerViewWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.label)
        self.layerSpin = QtGui.QSpinBox(LayerViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layerSpin.sizePolicy().hasHeightForWidth())
        self.layerSpin.setSizePolicy(sizePolicy)
        self.layerSpin.setMinimumSize(QtCore.QSize(0, 30))
        self.layerSpin.setObjectName(_fromUtf8("layerSpin"))
        self.verticalLayout_2.addWidget(self.layerSpin)
        self.layerSlider = QtGui.QSlider(LayerViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.layerSlider.sizePolicy().hasHeightForWidth())
        self.layerSlider.setSizePolicy(sizePolicy)
        self.layerSlider.setMinimumSize(QtCore.QSize(40, 0))
        self.layerSlider.setProperty("value", 0)
        self.layerSlider.setOrientation(QtCore.Qt.Vertical)
        self.layerSlider.setObjectName(_fromUtf8("layerSlider"))
        self.verticalLayout_2.addWidget(self.layerSlider)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(LayerViewWidget)
        QtCore.QObject.connect(self.layerSpin, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.layerSlider.setValue)
        QtCore.QObject.connect(self.layerSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.layerSpin.setValue)
        QtCore.QMetaObject.connectSlotsByName(LayerViewWidget)

    def retranslateUi(self, LayerViewWidget):
        LayerViewWidget.setWindowTitle(_translate("LayerViewWidget", "Layer Viewer", None))
        self.fileButton.setText(_translate("LayerViewWidget", "Load File", None))
        self.label.setText(_translate("LayerViewWidget", "Layer", None))

