# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Dropbox\workspace-python\pyEindwerk\src\gui\main_window.ui'
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(898, 518)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/cinema.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setSizeConstraint(QtGui.QLayout.SetNoConstraint)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.graphicsView = QtGui.QGraphicsView(self.centralwidget)
        self.graphicsView.setProperty(_fromUtf8("cursor"), QtCore.Qt.ArrowCursor)
        self.graphicsView.setMouseTracking(False)
        self.graphicsView.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
        self.graphicsView.setOptimizationFlags(QtGui.QGraphicsView.DontSavePainterState)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.verticalLayout_2.addWidget(self.graphicsView)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 898, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_Help = QtGui.QMenu(self.menubar)
        self.menu_Help.setObjectName(_fromUtf8("menu_Help"))
        self.menuGenerate = QtGui.QMenu(self.menubar)
        self.menuGenerate.setObjectName(_fromUtf8("menuGenerate"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBarFile = QtGui.QToolBar(MainWindow)
        self.toolBarFile.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBarFile.setObjectName(_fromUtf8("toolBarFile"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarFile)
        self.entityDock = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.entityDock.sizePolicy().hasHeightForWidth())
        self.entityDock.setSizePolicy(sizePolicy)
        self.entityDock.setMinimumSize(QtCore.QSize(72, 93))
        self.entityDock.setBaseSize(QtCore.QSize(50, 0))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/add-document.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.entityDock.setWindowIcon(icon1)
        self.entityDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.entityDock.setObjectName(_fromUtf8("entityDock"))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.entityLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.entityLayout.setMargin(0)
        self.entityLayout.setObjectName(_fromUtf8("entityLayout"))
        self.entityTreeView = QtGui.QTreeView(self.dockWidgetContents)
        self.entityTreeView.setEnabled(True)
        self.entityTreeView.setMinimumSize(QtCore.QSize(50, 0))
        self.entityTreeView.setBaseSize(QtCore.QSize(70, 0))
        self.entityTreeView.setFrameShadow(QtGui.QFrame.Sunken)
        self.entityTreeView.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
        self.entityTreeView.setTabKeyNavigation(True)
        self.entityTreeView.setDragEnabled(True)
        self.entityTreeView.setDragDropMode(QtGui.QAbstractItemView.DragOnly)
        self.entityTreeView.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.entityTreeView.setAnimated(True)
        self.entityTreeView.setObjectName(_fromUtf8("entityTreeView"))
        self.entityTreeView.header().setVisible(False)
        self.entityLayout.addWidget(self.entityTreeView)
        self.entityDock.setWidget(self.dockWidgetContents)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.entityDock)
        self.constraintsDock = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.constraintsDock.sizePolicy().hasHeightForWidth())
        self.constraintsDock.setSizePolicy(sizePolicy)
        self.constraintsDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.constraintsDock.setObjectName(_fromUtf8("constraintsDock"))
        self.dockWidgetConstraints = QtGui.QWidget()
        self.dockWidgetConstraints.setMinimumSize(QtCore.QSize(216, 289))
        self.dockWidgetConstraints.setObjectName(_fromUtf8("dockWidgetConstraints"))
        self._2 = QtGui.QVBoxLayout(self.dockWidgetConstraints)
        self._2.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self._2.setContentsMargins(2, 0, 4, 0)
        self._2.setObjectName(_fromUtf8("_2"))
        self.horizontalLayoutAttribute = QtGui.QHBoxLayout()
        self.horizontalLayoutAttribute.setObjectName(_fromUtf8("horizontalLayoutAttribute"))
        self.attributeLabel = QtGui.QLabel(self.dockWidgetConstraints)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.attributeLabel.sizePolicy().hasHeightForWidth())
        self.attributeLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.attributeLabel.setFont(font)
        self.attributeLabel.setObjectName(_fromUtf8("attributeLabel"))
        self.horizontalLayoutAttribute.addWidget(self.attributeLabel)
        self._2.addLayout(self.horizontalLayoutAttribute)
        self.attributeBox = QtGui.QCheckBox(self.dockWidgetConstraints)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.attributeBox.setFont(font)
        self.attributeBox.setObjectName(_fromUtf8("attributeBox"))
        self._2.addWidget(self.attributeBox)
        self.availabilityComboBox = QtGui.QComboBox(self.dockWidgetConstraints)
        self.availabilityComboBox.setObjectName(_fromUtf8("availabilityComboBox"))
        self.availabilityComboBox.addItem(_fromUtf8(""))
        self.availabilityComboBox.addItem(_fromUtf8(""))
        self._2.addWidget(self.availabilityComboBox)
        self.rangeBox = QtGui.QCheckBox(self.dockWidgetConstraints)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.rangeBox.setFont(font)
        self.rangeBox.setObjectName(_fromUtf8("rangeBox"))
        self._2.addWidget(self.rangeBox)
        self.dials = QtGui.QWidget(self.dockWidgetConstraints)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.dials.sizePolicy().hasHeightForWidth())
        self.dials.setSizePolicy(sizePolicy)
        self.dials.setObjectName(_fromUtf8("dials"))
        self.horizontalLayoutDials = QtGui.QHBoxLayout(self.dials)
        self.horizontalLayoutDials.setSizeConstraint(QtGui.QLayout.SetMinimumSize)
        self.horizontalLayoutDials.setMargin(0)
        self.horizontalLayoutDials.setObjectName(_fromUtf8("horizontalLayoutDials"))
        self.minimumLabel = QtGui.QLabel(self.dials)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minimumLabel.sizePolicy().hasHeightForWidth())
        self.minimumLabel.setSizePolicy(sizePolicy)
        self.minimumLabel.setObjectName(_fromUtf8("minimumLabel"))
        self.horizontalLayoutDials.addWidget(self.minimumLabel)
        self.minimumDail = QtGui.QDial(self.dials)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.minimumDail.sizePolicy().hasHeightForWidth())
        self.minimumDail.setSizePolicy(sizePolicy)
        self.minimumDail.setObjectName(_fromUtf8("minimumDail"))
        self.horizontalLayoutDials.addWidget(self.minimumDail)
        self.maximumLabel = QtGui.QLabel(self.dials)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maximumLabel.sizePolicy().hasHeightForWidth())
        self.maximumLabel.setSizePolicy(sizePolicy)
        self.maximumLabel.setObjectName(_fromUtf8("maximumLabel"))
        self.horizontalLayoutDials.addWidget(self.maximumLabel)
        self.maximumDial = QtGui.QDial(self.dials)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maximumDial.sizePolicy().hasHeightForWidth())
        self.maximumDial.setSizePolicy(sizePolicy)
        self.maximumDial.setObjectName(_fromUtf8("maximumDial"))
        self.horizontalLayoutDials.addWidget(self.maximumDial)
        self._2.addWidget(self.dials)
        self.spinners = QtGui.QWidget(self.dockWidgetConstraints)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.spinners.sizePolicy().hasHeightForWidth())
        self.spinners.setSizePolicy(sizePolicy)
        self.spinners.setObjectName(_fromUtf8("spinners"))
        self.horizontalLayoutSpinBox = QtGui.QHBoxLayout(self.spinners)
        self.horizontalLayoutSpinBox.setMargin(0)
        self.horizontalLayoutSpinBox.setObjectName(_fromUtf8("horizontalLayoutSpinBox"))
        self.startSpinBox = QtGui.QSpinBox(self.spinners)
        self.startSpinBox.setObjectName(_fromUtf8("startSpinBox"))
        self.horizontalLayoutSpinBox.addWidget(self.startSpinBox)
        self.stopSpinBox = QtGui.QSpinBox(self.spinners)
        self.stopSpinBox.setObjectName(_fromUtf8("stopSpinBox"))
        self.horizontalLayoutSpinBox.addWidget(self.stopSpinBox)
        self._2.addWidget(self.spinners)
        self.valueBox = QtGui.QCheckBox(self.dockWidgetConstraints)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        self.valueBox.setFont(font)
        self.valueBox.setObjectName(_fromUtf8("valueBox"))
        self._2.addWidget(self.valueBox)
        self.listWidgetValues = QtGui.QListWidget(self.dockWidgetConstraints)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listWidgetValues.sizePolicy().hasHeightForWidth())
        self.listWidgetValues.setSizePolicy(sizePolicy)
        self.listWidgetValues.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.listWidgetValues.setObjectName(_fromUtf8("listWidgetValues"))
        self._2.addWidget(self.listWidgetValues)
        self.checkAllButton = QtGui.QPushButton(self.dockWidgetConstraints)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/media-shuffle.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.checkAllButton.setIcon(icon2)
        self.checkAllButton.setObjectName(_fromUtf8("checkAllButton"))
        self._2.addWidget(self.checkAllButton)
        self.constraintsDock.setWidget(self.dockWidgetConstraints)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.constraintsDock)
        self.toolBarProgram = QtGui.QToolBar(MainWindow)
        self.toolBarProgram.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)
        self.toolBarProgram.setObjectName(_fromUtf8("toolBarProgram"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBarProgram)
        self.propertiesDock = QtGui.QDockWidget(MainWindow)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.propertiesDock.sizePolicy().hasHeightForWidth())
        self.propertiesDock.setSizePolicy(sizePolicy)
        self.propertiesDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.propertiesDock.setObjectName(_fromUtf8("propertiesDock"))
        self.dockWidgetProperties = QtGui.QWidget()
        self.dockWidgetProperties.setObjectName(_fromUtf8("dockWidgetProperties"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetProperties)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.labelEntities = QtGui.QLabel(self.dockWidgetProperties)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.labelEntities.sizePolicy().hasHeightForWidth())
        self.labelEntities.setSizePolicy(sizePolicy)
        self.labelEntities.setObjectName(_fromUtf8("labelEntities"))
        self.verticalLayout.addWidget(self.labelEntities)
        self.rootEntityAmount = QtGui.QSpinBox(self.dockWidgetProperties)
        self.rootEntityAmount.setAccelerated(True)
        self.rootEntityAmount.setPrefix(_fromUtf8(""))
        self.rootEntityAmount.setMinimum(1)
        self.rootEntityAmount.setMaximum(5000000)
        self.rootEntityAmount.setProperty(_fromUtf8("value"), 10)
        self.rootEntityAmount.setObjectName(_fromUtf8("rootEntityAmount"))
        self.verticalLayout.addWidget(self.rootEntityAmount)
        self.horizontalLayoutRandom = QtGui.QHBoxLayout()
        self.horizontalLayoutRandom.setObjectName(_fromUtf8("horizontalLayoutRandom"))
        self.randomBox = QtGui.QCheckBox(self.dockWidgetProperties)
        self.randomBox.setObjectName(_fromUtf8("randomBox"))
        self.horizontalLayoutRandom.addWidget(self.randomBox)
        self.sortBox = QtGui.QCheckBox(self.dockWidgetProperties)
        self.sortBox.setChecked(True)
        self.sortBox.setObjectName(_fromUtf8("sortBox"))
        self.horizontalLayoutRandom.addWidget(self.sortBox)
        self.verticalLayout.addLayout(self.horizontalLayoutRandom)
        self.horizontalLayoutOutput = QtGui.QHBoxLayout()
        self.horizontalLayoutOutput.setObjectName(_fromUtf8("horizontalLayoutOutput"))
        self.labelOutputFile = QtGui.QLabel(self.dockWidgetProperties)
        self.labelOutputFile.setObjectName(_fromUtf8("labelOutputFile"))
        self.horizontalLayoutOutput.addWidget(self.labelOutputFile)
        self.outputFilePath = QtGui.QLineEdit(self.dockWidgetProperties)
        self.outputFilePath.setObjectName(_fromUtf8("outputFilePath"))
        self.horizontalLayoutOutput.addWidget(self.outputFilePath)
        self.outputFileChooserButton = QtGui.QPushButton(self.dockWidgetProperties)
        self.outputFileChooserButton.setMaximumSize(QtCore.QSize(30, 16777215))
        self.outputFileChooserButton.setObjectName(_fromUtf8("outputFileChooserButton"))
        self.horizontalLayoutOutput.addWidget(self.outputFileChooserButton)
        self.verticalLayout.addLayout(self.horizontalLayoutOutput)
        self.progressBar = QtGui.QProgressBar(self.dockWidgetProperties)
        self.progressBar.setEnabled(False)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMaximum(100)
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.verticalLayout.addWidget(self.progressBar)
        self.cancelButton = QtGui.QPushButton(self.dockWidgetProperties)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/stop.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.cancelButton.setIcon(icon3)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.verticalLayout.addWidget(self.cancelButton)
        spacerItem = QtGui.QSpacerItem(20, 0, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.propertiesDock.setWidget(self.dockWidgetProperties)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(1), self.propertiesDock)
        self.infoDock = QtGui.QDockWidget(MainWindow)
        self.infoDock.setFeatures(QtGui.QDockWidget.DockWidgetFloatable|QtGui.QDockWidget.DockWidgetMovable)
        self.infoDock.setObjectName(_fromUtf8("infoDock"))
        self.dockWidgetInformation = QtGui.QWidget()
        self.dockWidgetInformation.setObjectName(_fromUtf8("dockWidgetInformation"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.dockWidgetInformation)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.docViewer = QtGui.QPlainTextEdit(self.dockWidgetInformation)
        self.docViewer.setUndoRedoEnabled(False)
        self.docViewer.setReadOnly(True)
        self.docViewer.setObjectName(_fromUtf8("docViewer"))
        self.verticalLayout_3.addWidget(self.docViewer)
        self.infoDock.setWidget(self.dockWidgetInformation)
        MainWindow.addDockWidget(QtCore.Qt.DockWidgetArea(2), self.infoDock)
        self.actionAbout = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/about.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionAbout.setIcon(icon4)
        self.actionAbout.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionAbout.setMenuRole(QtGui.QAction.AboutRole)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionLoad_query = QtGui.QAction(MainWindow)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/media-eject.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionLoad_query.setIcon(icon5)
        self.actionLoad_query.setObjectName(_fromUtf8("actionLoad_query"))
        self.actionSave_query = QtGui.QAction(MainWindow)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionSave_query.setIcon(icon6)
        self.actionSave_query.setObjectName(_fromUtf8("actionSave_query"))
        self.actionSave_query_as = QtGui.QAction(MainWindow)
        self.actionSave_query_as.setObjectName(_fromUtf8("actionSave_query_as"))
        self.actionConfigure = QtGui.QAction(MainWindow)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/tools.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionConfigure.setIcon(icon7)
        self.actionConfigure.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionConfigure.setMenuRole(QtGui.QAction.PreferencesRole)
        self.actionConfigure.setObjectName(_fromUtf8("actionConfigure"))
        self.actionExit = QtGui.QAction(MainWindow)
        self.actionExit.setIcon(icon3)
        self.actionExit.setShortcutContext(QtCore.Qt.ApplicationShortcut)
        self.actionExit.setMenuRole(QtGui.QAction.QuitRole)
        self.actionExit.setObjectName(_fromUtf8("actionExit"))
        self.actionGenerate = QtGui.QAction(MainWindow)
        icon8 = QtGui.QIcon()
        icon8.addPixmap(QtGui.QPixmap(_fromUtf8(":/science.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionGenerate.setIcon(icon8)
        self.actionGenerate.setObjectName(_fromUtf8("actionGenerate"))
        self.actionAdd = QtGui.QAction(MainWindow)
        icon9 = QtGui.QIcon()
        icon9.addPixmap(QtGui.QPixmap(_fromUtf8(":/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionAdd.setIcon(icon9)
        self.actionAdd.setVisible(True)
        self.actionAdd.setObjectName(_fromUtf8("actionAdd"))
        self.actionRemove = QtGui.QAction(MainWindow)
        icon10 = QtGui.QIcon()
        icon10.addPixmap(QtGui.QPixmap(_fromUtf8(":/remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.On)
        self.actionRemove.setIcon(icon10)
        self.actionRemove.setObjectName(_fromUtf8("actionRemove"))
        self.actionAbout_Qt = QtGui.QAction(MainWindow)
        self.actionAbout_Qt.setObjectName(_fromUtf8("actionAbout_Qt"))
        self.actionClear = QtGui.QAction(MainWindow)
        icon11 = QtGui.QIcon()
        icon11.addPixmap(QtGui.QPixmap(_fromUtf8(":/button-up.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.actionClear.setIcon(icon11)
        self.actionClear.setObjectName(_fromUtf8("actionClear"))
        self.menu_File.addAction(self.actionLoad_query)
        self.menu_File.addAction(self.actionSave_query)
        self.menu_File.addAction(self.actionSave_query_as)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionConfigure)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.actionExit)
        self.menu_Help.addAction(self.actionAbout)
        self.menu_Help.addAction(self.actionAbout_Qt)
        self.menuGenerate.addAction(self.actionGenerate)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menuGenerate.menuAction())
        self.menubar.addAction(self.menu_Help.menuAction())
        self.toolBarFile.addAction(self.actionLoad_query)
        self.toolBarFile.addAction(self.actionSave_query)
        self.toolBarFile.addAction(self.actionConfigure)
        self.toolBarProgram.addAction(self.actionAdd)
        self.toolBarProgram.addAction(self.actionRemove)
        self.toolBarProgram.addAction(self.actionClear)
        self.toolBarProgram.addAction(self.actionGenerate)
        self.toolBarProgram.addAction(self.actionExit)
        self.labelEntities.setBuddy(self.rootEntityAmount)
        self.labelOutputFile.setBuddy(self.outputFilePath)

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.actionExit, QtCore.SIGNAL(_fromUtf8("triggered()")), MainWindow.close)
        QtCore.QObject.connect(self.minimumDail, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.startSpinBox.setValue)
        QtCore.QObject.connect(self.maximumDial, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.stopSpinBox.setValue)
        QtCore.QObject.connect(self.startSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.minimumDail.setValue)
        QtCore.QObject.connect(self.stopSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.maximumDial.setValue)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        MainWindow.setTabOrder(self.entityTreeView, self.rootEntityAmount)
        MainWindow.setTabOrder(self.rootEntityAmount, self.outputFilePath)
        MainWindow.setTabOrder(self.outputFilePath, self.outputFileChooserButton)
        MainWindow.setTabOrder(self.outputFileChooserButton, self.cancelButton)
        MainWindow.setTabOrder(self.cancelButton, self.docViewer)
        MainWindow.setTabOrder(self.docViewer, self.listWidgetValues)
        MainWindow.setTabOrder(self.listWidgetValues, self.minimumDail)
        MainWindow.setTabOrder(self.minimumDail, self.maximumDial)
        MainWindow.setTabOrder(self.maximumDial, self.stopSpinBox)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "IMDb dataset generator", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_File.setTitle(QtGui.QApplication.translate("MainWindow", "&File", None, QtGui.QApplication.UnicodeUTF8))
        self.menu_Help.setTitle(QtGui.QApplication.translate("MainWindow", "&Help", None, QtGui.QApplication.UnicodeUTF8))
        self.menuGenerate.setTitle(QtGui.QApplication.translate("MainWindow", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarFile.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.entityDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "  Entity list", None, QtGui.QApplication.UnicodeUTF8))
        self.constraintsDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Constraints", None, QtGui.QApplication.UnicodeUTF8))
        self.attributeLabel.setText(QtGui.QApplication.translate("MainWindow", "Attribute", None, QtGui.QApplication.UnicodeUTF8))
        self.attributeBox.setText(QtGui.QApplication.translate("MainWindow", "Availability constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.availabilityComboBox.setItemText(0, QtGui.QApplication.translate("MainWindow", "Attribute available", None, QtGui.QApplication.UnicodeUTF8))
        self.availabilityComboBox.setItemText(1, QtGui.QApplication.translate("MainWindow", "Attribute available and unique", None, QtGui.QApplication.UnicodeUTF8))
        self.rangeBox.setText(QtGui.QApplication.translate("MainWindow", "Range constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.minimumLabel.setText(QtGui.QApplication.translate("MainWindow", "Minimum:", None, QtGui.QApplication.UnicodeUTF8))
        self.maximumLabel.setText(QtGui.QApplication.translate("MainWindow", "Maximum:", None, QtGui.QApplication.UnicodeUTF8))
        self.valueBox.setText(QtGui.QApplication.translate("MainWindow", "Value constraint:", None, QtGui.QApplication.UnicodeUTF8))
        self.checkAllButton.setText(QtGui.QApplication.translate("MainWindow", "Invert selected", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBarProgram.setWindowTitle(QtGui.QApplication.translate("MainWindow", "toolBar_2", None, QtGui.QApplication.UnicodeUTF8))
        self.propertiesDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Generation options", None, QtGui.QApplication.UnicodeUTF8))
        self.labelEntities.setText(QtGui.QApplication.translate("MainWindow", "Amount of root entities to generate data from:", None, QtGui.QApplication.UnicodeUTF8))
        self.rootEntityAmount.setSuffix(QtGui.QApplication.translate("MainWindow", " entities", None, QtGui.QApplication.UnicodeUTF8))
        self.randomBox.setText(QtGui.QApplication.translate("MainWindow", "Generate at random", None, QtGui.QApplication.UnicodeUTF8))
        self.sortBox.setText(QtGui.QApplication.translate("MainWindow", "uniq + sort output", None, QtGui.QApplication.UnicodeUTF8))
        self.labelOutputFile.setText(QtGui.QApplication.translate("MainWindow", "Output file: ", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFilePath.setStatusTip(QtGui.QApplication.translate("MainWindow", "Output file for the generated Prolog facts. Everything in the file will be overwritten.", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFilePath.setText(QtGui.QApplication.translate("MainWindow", "../outputs/output.pl", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFileChooserButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Choose a file", None, QtGui.QApplication.UnicodeUTF8))
        self.outputFileChooserButton.setText(QtGui.QApplication.translate("MainWindow", "...", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setStatusTip(QtGui.QApplication.translate("MainWindow", "Cancel the generation process", None, QtGui.QApplication.UnicodeUTF8))
        self.cancelButton.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.infoDock.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Information", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout.setText(QtGui.QApplication.translate("MainWindow", "&About...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_query.setText(QtGui.QApplication.translate("MainWindow", "Load query", None, QtGui.QApplication.UnicodeUTF8))
        self.actionLoad_query.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+L", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_query.setText(QtGui.QApplication.translate("MainWindow", "Save query", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_query.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_query_as.setText(QtGui.QApplication.translate("MainWindow", "Save query as...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionSave_query_as.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Shift+S", None, QtGui.QApplication.UnicodeUTF8))
        self.actionConfigure.setText(QtGui.QApplication.translate("MainWindow", "Configure...", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setText(QtGui.QApplication.translate("MainWindow", "&Exit", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setStatusTip(QtGui.QApplication.translate("MainWindow", "Exit the program", None, QtGui.QApplication.UnicodeUTF8))
        self.actionExit.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+Q", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate.setText(QtGui.QApplication.translate("MainWindow", "Generate", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate.setToolTip(QtGui.QApplication.translate("MainWindow", "Generate the dataset", None, QtGui.QApplication.UnicodeUTF8))
        self.actionGenerate.setShortcut(QtGui.QApplication.translate("MainWindow", "Ctrl+G", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAdd.setToolTip(QtGui.QApplication.translate("MainWindow", "Add the entity", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.actionRemove.setToolTip(QtGui.QApplication.translate("MainWindow", "Remove the selected entity", None, QtGui.QApplication.UnicodeUTF8))
        self.actionAbout_Qt.setText(QtGui.QApplication.translate("MainWindow", "About Qt", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setText(QtGui.QApplication.translate("MainWindow", "Clear", None, QtGui.QApplication.UnicodeUTF8))
        self.actionClear.setToolTip(QtGui.QApplication.translate("MainWindow", "Clears the schema", None, QtGui.QApplication.UnicodeUTF8))

import icons_rc
