# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Dropbox\workspace-python\pyEindwerk\src\gui\config.ui'
#
# Created: Tue Aug 21 17:23:12 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(395, 238)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(30, 190, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.formLayoutWidget = QtGui.QWidget(Dialog)
        self.formLayoutWidget.setGeometry(QtCore.QRect(20, 20, 351, 161))
        self.formLayoutWidget.setObjectName(_fromUtf8("formLayoutWidget"))
        self.formLayout = QtGui.QFormLayout(self.formLayoutWidget)
        self.formLayout.setMargin(0)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.labelSqldatabase = QtGui.QLabel(self.formLayoutWidget)
        self.labelSqldatabase.setObjectName(_fromUtf8("labelSqldatabase"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.labelSqldatabase)
        self.sqldatabase = QtGui.QLineEdit(self.formLayoutWidget)
        self.sqldatabase.setObjectName(_fromUtf8("sqldatabase"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.sqldatabase)
        self.labelLogin = QtGui.QLabel(self.formLayoutWidget)
        self.labelLogin.setObjectName(_fromUtf8("labelLogin"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.labelLogin)
        self.login = QtGui.QLineEdit(self.formLayoutWidget)
        self.login.setObjectName(_fromUtf8("login"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.login)
        self.labelPassword = QtGui.QLabel(self.formLayoutWidget)
        self.labelPassword.setObjectName(_fromUtf8("labelPassword"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.labelPassword)
        self.labelHost = QtGui.QLabel(self.formLayoutWidget)
        self.labelHost.setObjectName(_fromUtf8("labelHost"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.labelHost)
        self.labelPort = QtGui.QLabel(self.formLayoutWidget)
        self.labelPort.setObjectName(_fromUtf8("labelPort"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.LabelRole, self.labelPort)
        self.host = QtGui.QLineEdit(self.formLayoutWidget)
        self.host.setObjectName(_fromUtf8("host"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.host)
        self.port = QtGui.QLineEdit(self.formLayoutWidget)
        self.port.setObjectName(_fromUtf8("port"))
        self.formLayout.setWidget(4, QtGui.QFormLayout.FieldRole, self.port)
        self.password = QtGui.QLineEdit(self.formLayoutWidget)
        self.password.setObjectName(_fromUtf8("password"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.password)
        self.labelDatabase = QtGui.QLabel(self.formLayoutWidget)
        self.labelDatabase.setObjectName(_fromUtf8("labelDatabase"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.LabelRole, self.labelDatabase)
        self.database = QtGui.QLineEdit(self.formLayoutWidget)
        self.database.setObjectName(_fromUtf8("database"))
        self.formLayout.setWidget(5, QtGui.QFormLayout.FieldRole, self.database)
        self.labelSqldatabase.setBuddy(self.sqldatabase)
        self.labelLogin.setBuddy(self.login)
        self.labelPassword.setBuddy(self.password)
        self.labelHost.setBuddy(self.host)
        self.labelPort.setBuddy(self.port)
        self.labelDatabase.setBuddy(self.database)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Dialog", None, QtGui.QApplication.UnicodeUTF8))
        self.labelSqldatabase.setText(QtGui.QApplication.translate("Dialog", "SQL database:", None, QtGui.QApplication.UnicodeUTF8))
        self.sqldatabase.setText(QtGui.QApplication.translate("Dialog", "mysql", None, QtGui.QApplication.UnicodeUTF8))
        self.labelLogin.setText(QtGui.QApplication.translate("Dialog", "Login:", None, QtGui.QApplication.UnicodeUTF8))
        self.login.setText(QtGui.QApplication.translate("Dialog", "imdb", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPassword.setText(QtGui.QApplication.translate("Dialog", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelHost.setText(QtGui.QApplication.translate("Dialog", "Host:", None, QtGui.QApplication.UnicodeUTF8))
        self.labelPort.setText(QtGui.QApplication.translate("Dialog", "Port:", None, QtGui.QApplication.UnicodeUTF8))
        self.host.setText(QtGui.QApplication.translate("Dialog", "localhost", None, QtGui.QApplication.UnicodeUTF8))
        self.port.setText(QtGui.QApplication.translate("Dialog", "3306", None, QtGui.QApplication.UnicodeUTF8))
        self.password.setText(QtGui.QApplication.translate("Dialog", "imdbpwd", None, QtGui.QApplication.UnicodeUTF8))
        self.labelDatabase.setText(QtGui.QApplication.translate("Dialog", "Database:", None, QtGui.QApplication.UnicodeUTF8))
        self.database.setText(QtGui.QApplication.translate("Dialog", "imdb", None, QtGui.QApplication.UnicodeUTF8))

