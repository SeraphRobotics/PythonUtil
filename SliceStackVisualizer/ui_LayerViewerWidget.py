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
# Created: Wed Dec 12 17:04:41 2012
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_LayerViewWidget(object):
    def setupUi(self, LayerViewWidget):
        LayerViewWidget.setObjectName(_fromUtf8("LayerViewWidget"))
        LayerViewWidget.resize(613, 557)
        LayerViewWidget.setWindowTitle(QtGui.QApplication.translate("LayerViewWidget", "Layer Viewer", None, QtGui.QApplication.UnicodeUTF8))
        self.horizontalLayout = QtGui.QHBoxLayout(LayerViewWidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.layerView = QtGui.QGraphicsView(LayerViewWidget)
        self.layerView.setObjectName(_fromUtf8("layerView"))
        self.horizontalLayout.addWidget(self.layerView)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.label_2 = QtGui.QLabel(LayerViewWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Cambria"))
        font.setPointSize(14)
        self.label_2.setFont(font)
        self.label_2.setText(QtGui.QApplication.translate("LayerViewWidget", "Z", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_2.addWidget(self.label_2)
        self.zSpin = QtGui.QDoubleSpinBox(LayerViewWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.zSpin.sizePolicy().hasHeightForWidth())
        self.zSpin.setSizePolicy(sizePolicy)
        self.zSpin.setMinimumSize(QtCore.QSize(0, 30))
        self.zSpin.setAlignment(QtCore.Qt.AlignCenter)
        self.zSpin.setReadOnly(True)
        self.zSpin.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.zSpin.setSuffix(QtGui.QApplication.translate("LayerViewWidget", " mm", None, QtGui.QApplication.UnicodeUTF8))
        self.zSpin.setMinimum(-99990000.0)
        self.zSpin.setMaximum(99990000.0)
        self.zSpin.setObjectName(_fromUtf8("zSpin"))
        self.verticalLayout_2.addWidget(self.zSpin)
        self.label = QtGui.QLabel(LayerViewWidget)
        self.label.setMinimumSize(QtCore.QSize(0, 30))
        self.label.setText(QtGui.QApplication.translate("LayerViewWidget", "Layer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setAlignment(QtCore.Qt.AlignBottom|QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft)
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
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(LayerViewWidget)
        QtCore.QObject.connect(self.layerSpin, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.layerSlider.setValue)
        QtCore.QObject.connect(self.layerSlider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.layerSpin.setValue)
        QtCore.QMetaObject.connectSlotsByName(LayerViewWidget)

    def retranslateUi(self, LayerViewWidget):
        pass

