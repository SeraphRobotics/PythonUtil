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

