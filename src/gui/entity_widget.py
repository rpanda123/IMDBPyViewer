# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Dropbox\workspace-python\pyEindwerk\src\gui\entity_widget.ui'
#
# Created: Tue Aug 21 17:23:13 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_EntityWidget(object):
    def setupUi(self, EntityWidget):
        EntityWidget.setObjectName(_fromUtf8("EntityWidget"))
        EntityWidget.resize(203, 310)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(EntityWidget.sizePolicy().hasHeightForWidth())
        EntityWidget.setSizePolicy(sizePolicy)
        EntityWidget.setCursor(QtCore.Qt.ArrowCursor)
        EntityWidget.setMouseTracking(True)
        EntityWidget.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 127);"))
        self.verticalLayout = QtGui.QVBoxLayout(EntityWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.entityLabel = QtGui.QLabel(EntityWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entityLabel.sizePolicy().hasHeightForWidth())
        self.entityLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial Black"))
        font.setPointSize(10)
        font.setWeight(75)
        font.setBold(True)
        self.entityLabel.setFont(font)
        self.entityLabel.setCursor(QtCore.Qt.SizeAllCursor)
        self.entityLabel.setTextFormat(QtCore.Qt.RichText)
        self.entityLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.entityLabel.setObjectName(_fromUtf8("entityLabel"))
        self.verticalLayout.addWidget(self.entityLabel)
        self.splitter = QtGui.QSplitter(EntityWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.splitter.sizePolicy().hasHeightForWidth())
        self.splitter.setSizePolicy(sizePolicy)
        self.splitter.setMinimumSize(QtCore.QSize(0, 20))
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName(_fromUtf8("splitter"))
        self.classList = QtGui.QListView(self.splitter)
        self.classList.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 255);"))
        self.classList.setFrameShape(QtGui.QFrame.StyledPanel)
        self.classList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.classList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.classList.setAlternatingRowColors(True)
        self.classList.setObjectName(_fromUtf8("classList"))
        self.linkList = QtGui.QListView(self.splitter)
        self.linkList.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"color: rgb(0, 170, 127);"))
        self.linkList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.linkList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.linkList.setAlternatingRowColors(True)
        self.linkList.setObjectName(_fromUtf8("linkList"))
        self.attributeList = QtGui.QListView(self.splitter)
        self.attributeList.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 255);\n"
"color: rgb(86, 86, 86);\n"
""))
        self.attributeList.setFrameShape(QtGui.QFrame.StyledPanel)
        self.attributeList.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.attributeList.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.attributeList.setAlternatingRowColors(True)
        self.attributeList.setObjectName(_fromUtf8("attributeList"))
        self.verticalLayout.addWidget(self.splitter)

        self.retranslateUi(EntityWidget)
        QtCore.QMetaObject.connectSlotsByName(EntityWidget)

    def retranslateUi(self, EntityWidget):
        EntityWidget.setWindowTitle(QtGui.QApplication.translate("EntityWidget", "Entity", None, QtGui.QApplication.UnicodeUTF8))
        self.entityLabel.setText(QtGui.QApplication.translate("EntityWidget", "Entity Name", None, QtGui.QApplication.UnicodeUTF8))

