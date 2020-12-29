#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMDb Relational Dataset Generator
# Copyright (C) 2012  Jef Van den Brandt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
http://www.korokithakis.net/tutorials/python/
http://www.ics.com/learning/icsnetwork/


MyGrid would be the class representing the concept of "grid" I've talked about 
in post #1. It has as children some rectangles managed in turn by a layout 
(default: QGraphicsGridLayout) for the reasons I've also mentioned in post #1.
http://www.qtcentre.org/threads/40320-QGraphicsScene-and-QGraphicsWidget-(
reusable-and-embeddable)?s=ba870d122ade91f89e4069c23cf44a5f

http://doc.qt.nokia.com/latest/qgraphicsgridlayout.html
ambiguity in ownership
QGraphicsLayoutItem::setOwnedByLayout()


addItem ( QGraphicsItem * item )
If the item is visible (i.e., QGraphicsItem::isVisible() returns true),
 QGraphicsScene will emit changed() once control goes back to the event loop.
 
setSelectionArea 

void QGraphicsScene::update ( const QRectF & rect = QRectF() ) [slot]
Schedules a redraw of the area rect on the scene.
See also sceneRect() and changed().

The boundingRect() function is called by QGraphicsView to determine whether the item needs to be drawn.
The shape() function is called by QGraphicsView for fine-grained collision detection.

resize:
http://labs.qt.nokia.com/2006/12/15/interact-with-volatile-graphics-items/

TODO:
 - root entity removed: select new root entity if applicable
   or don't remove root
 - only remove entity when there is only one link
 - help messages in bar at bottom
 
http://packages.python.org/distribute/setuptools.html#automatic-script-creation
"""

from PyQt4 import QtCore, QtGui
import gui
import sys
import modeltest
import imdbmodel as dataset

scene = None # where we draw everything on; the model
debug = False # whether we check the UI models or not

class CannotAddEntityException(Exception):
	"""The selected entity cannot be added to the scene."""
	pass

class EntityTreeModel(QtGui.QStandardItemModel):
	"""The model of the entity tree on the left side of this tool.
	Based on the list of major entities from the dataset."""
	def __init__(self, parent=None):
		super(EntityTreeModel, self).__init__(parent)
		
		root = self.invisibleRootItem()
		for entity in dataset.entities:
			self._addEntity(entity, root)
			
	def _addEntity(self, entityClass, root):
		"""Private helper function which recursively adds elements."""
		item = EntityTreeElement(entityClass)

		for subentity in entityClass.listSubentities():
			self._addEntity(subentity, item)
		root.appendRow(item)
		
	def data(self, index, role=QtCore.Qt.DisplayRole):
		"""Returns the data stored under the given role 
		for the item referred to by the index."""
		if index.isValid() and role == QtCore.Qt.UserRole:
			# when drag/drop: returns class of the model
			return self.itemFromIndex(index).classEntityModel
		else:
			# for the label/name of the tree element,...
			return QtGui.QStandardItemModel.data(self, index, role)
		
class EntityTreeElement(QtGui.QStandardItem):
	"""Item of the Entity tree on the left side of this tool.
	entity: an AbstractEntity class (like Movie)"""
	def __init__(self, clsEntity):
		self.classEntityModel = clsEntity
#		QtGui.QStandardItem.__init__(self, clsEntity.name)
		super(EntityTreeElement, self).__init__(clsEntity.name)

class MainWindow(QtGui.QMainWindow):
	"""Class that represents the main window of this application."""
	def __init__(self):
		super(MainWindow, self).__init__()
		
		# the controller contains the ui and doesn't inherit it directly
		# load user interface elements
		self.ui = gui.Ui_MainWindow()
		self.ui.setupUi(self)
		self.setWindowTitle("%s Relational Dataset Generator" % dataset.name)
		# http://stackoverflow.com/questions/1660474/pyqt-and-mvc-pattern
		# the controller contains the ui and doesn't inherit it directly. The controller will be responsible for managing signal slots connections for your gui and providing an interface to you data model.
		
		# scene: where we draw everything on; the model
		global scene
		scene = DiagramScene(self.ui.graphicsView)
		scene.selectionChanged.connect(self.selectionChanged)
		#self.scene.drop.connect(self.newEntity)
		self.ui.graphicsView.setScene(scene)
	
		# where we drag the entities from
		emodel = EntityTreeModel(self.ui.entityTreeView)
		if debug:
			modeltest.ModelTest(emodel, self)
		self.ui.entityTreeView.setModel(emodel)
		self.ui.entityTreeView.expandAll()
		
		def mousePressEventTree(event):
			selfTree = self.ui.entityTreeView
			#print selfTree.selectedIndexes()
			selfTree.defaultMousePressEvent(event)
		defaultmpe = self.ui.entityTreeView.mousePressEvent
		self.ui.entityTreeView.mousePressEvent = mousePressEventTree
		self.ui.entityTreeView.defaultMousePressEvent = defaultmpe
		
		# connect the actions from the menus
		self.ui.actionAbout_Qt.triggered.connect(QtGui.qApp.aboutQt)
		self.ui.actionAbout.triggered.connect(self.about)
		self.ui.actionAdd.triggered.connect(self.addAction)
		self.ui.actionRemove.triggered.connect(removeSelectedEntities)
		self.ui.actionGenerate.triggered.connect(generate)
		self.ui.actionClear.triggered.connect(self.clear)
		
#		self.ui.actionLoad_query.triggered.connect(self.notYetImplemented)
#		self.ui.actionSave_query.triggered.connect(self.notYetImplemented)
		self.ui.actionLoad_query.triggered.connect(self.loadQuery)
		self.ui.actionSave_query.triggered.connect(self.saveQuery)
		self.ui.actionSave_query_as.triggered.connect(self.notYetImplemented)
		
		self.ui.outputFileChooserButton.clicked.connect(self.askOutputFile)
		
#		QtCore.QObject.connect(self.ui.pushButton, QtCore.SIGNAL("clicked()"), self.do_stuff)
#	
		self.thread = dataset.GeneratorThread()
		self.thread.finished.connect(self.generationFinished)
		self.thread.terminated.connect(self.generationFinished)
		self.thread.progress.connect(self.generationProgress)

		# to stop generation gracefully
		self.ui.cancelButton.clicked.connect(self.thread.halt)
		self.showCancelButton(False)
		
				
		self.hideAllConstraints()
		# connect enabling checkboxes constraints
		self.ui.attributeBox.stateChanged.connect(
											self.constraintAttributeChanged)
		self.ui.rangeBox.stateChanged.connect(self.constraintRangeChanged)
		self.ui.valueBox.stateChanged.connect(self.constraintValueChanged)
		
		# connect other widgets constraints
		self.ui.availabilityComboBox.currentIndexChanged.connect(
										self.attributeConstraintIndexChanged)
		self.ui.startSpinBox.valueChanged.connect(self.rangeValueChanged)
		self.ui.stopSpinBox.valueChanged.connect(self.rangeValueChanged)
		self.ui.listWidgetValues.itemChanged.connect(self.valueChanged)
		self.ui.checkAllButton.clicked.connect(self.invertAllValues)
		
	def showCancelButton(self, status):
		if status:
			self.ui.cancelButton.show()
		else:
			self.ui.cancelButton.hide()
		
	def notYetImplemented(self):
		QtGui.QMessageBox.about(self, "Not implemented", 
							"This feature isn't implemented.")
		
	def about(self):
		"""Message box about window gets shown."""
		QtGui.QMessageBox.about(self, "About Menu",
				"<p>Created by <b>Jef Van den Brandt</b>.</p>"
				"Icons by <a href='http://www.interactivemania.com/'>"
				"interactivemania</a>.")
			
	def selectionChanged(self):
		"""When an entity is selected or deselected."""
		#print("selectionChanged main !!!")
	
	def addAction(self):
		srcw = self.ui.entityTreeView
		entity = srcw.model().data(srcw.currentIndex(), QtCore.Qt.UserRole)
		drawEntity(entity, QtCore.QPointF())

	def generationProgress(self, current, total):
		self.ui.progressBar.setMaximum(total)
		self.ui.progressBar.setValue(current)
	
	def generationFinished(self):
		# TODO: other behaviour when cancelled
		print("The generation finished.")
		if self.ui.sortBox.checkState() == QtCore.Qt.Checked:
			print("Sorting...")
			sortOutputFile(myapp.output)
		QtGui.QMessageBox.about(self, "Finished", "The generation finished.")
		
		# enable generate action
		self.ui.actionGenerate.setEnabled(True)
		self.showCancelButton(False)
		
	def askOutputFile(self):
		self.ui.outputFilePath.setText(QtGui.QFileDialog.getOpenFileName())
		
	def hideAllConstraints(self):
		self.ui.attributeLabel.setText("")
		
		self.ui.attributeBox.hide()
		self.ui.availabilityComboBox.hide()
		
		self.ui.rangeBox.hide()
		self.ui.dials.hide()
		self.ui.spinners.hide()
		
		self.ui.valueBox.hide()
		self.ui.listWidgetValues.hide()
		self.ui.checkAllButton.hide()
		
	def constraintAttributeChanged(self, state):
		self.ui.attributeBox.model.enabled = (state == QtCore.Qt.Checked)
	def attributeConstraintIndexChanged(self, index):
		self.ui.attributeBox.model.unique = index
		
	def constraintRangeChanged(self, state):
		self.ui.rangeBox.model.enabled = (state == QtCore.Qt.Checked)
	def rangeValueChanged(self, value):
		self.ui.rangeBox.model.curMin = self.ui.startSpinBox.value()
		self.ui.rangeBox.model.curMax = self.ui.stopSpinBox.value()

	def constraintValueChanged(self, state):
		self.ui.valueBox.model.enabled = (state == QtCore.Qt.Checked)
	def valueChanged(self, qlistwidgetitem):
		myapp.ui.valueBox.model.values[str(qlistwidgetitem.text())] = (
							qlistwidgetitem.checkState() == QtCore.Qt.Checked)
		# so we don't forget to check the enable button
		myapp.ui.valueBox.setChecked(True)
	def invertAllValues(self):
		"""Invert the selection."""
		w = myapp.ui.listWidgetValues
		for i in range(w.count()):
			if w.item(i).isSelected():
				if w.item(i).checkState() == QtCore.Qt.Checked:
					w.item(i).setCheckState(QtCore.Qt.Unchecked)
				else:
					w.item(i).setCheckState(QtCore.Qt.Checked)
					
	def saveQuery(self):
		import pickle

		with open("diagram.imdb", "w") as diagram:
			pickle.dump(scene.getAllModelsAsPythonList(), diagram)
		
	def loadQuery(self):
		import pickle
		
		with open("diagram.imdb", "r") as diagram:
			modelList = pickle.load(diagram)
		self.clear()
		for model in modelList:
			drawEntity(model)
			
	def clear(self):
		"""Clears the diagram of all entities and links."""
		scene.clear()
		
class EntityWidget(QtGui.QSizeGrip):
	"""A (graphical) entity widget representation. 
	A proper way to do a resize instead of inheriting of QSizeGrip:
	http://www.qtforum.org/article/31833/
	need-help-to-resize-qwidget-manually-inside-a-main-window.html"""
	def __init__(self, model, proxy, parent=None):
		QtGui.QSizeGrip.__init__(self, parent)
		self.ui = gui.Ui_EntityWidget()
		self.ui.setupUi(self)
		self.setCursor(QtCore.Qt.ArrowCursor)
		
#		self.proxy = proxy # TODO: never used? Parent?
		
		# the proxy of the (last) other widget we link with
		self.newLinkedProxy = None
		
		self.model = model # instantiated AbstractEntity class
		self._rootChange()
		
		# 1) ATTRIBUTES -------------------------------------------------------
		# models behind the lists
		ecm = None
		elm = None	  
		eam = EntityAttributeModel(self.model.attributes)
		eam.itemChanged.connect(eam.checkStateChange)

		# 2) LINKS ------------------------------------------------------------
		# try to link from the 'root' Entity first, then others at random 
		si = scene.selectedItems()
		if not len(si):
			si = scene.items()
		proxies = [item for item in si if hasattr(item, 'widget')]
		
		can_be_drawn = False
		
		# decide if widget can be drawn based on model data
		for item in sorted(proxies): # selected items
			try: # try to get item and model from proxy
				m = item.widget().model

				# possible to connect an exiting entity to this new one?
				linkclass = m.links[self.model.rootLevelEntityType] # no: KeyError
				linkInst = linkclass(m, self.model) # yes!
				self.model.link = linkInst # LNK
				assert isinstance(linkInst, dataset.AbstractLink)
				assert not isinstance(linkclass, dataset.AbstractLink)
				can_be_drawn = True
				
				self.newLinkedProxy = item
				
				if not self.generationRoot: # isn't this always true here?
					elm = EntityLinkModel(linkInst)
					elm.itemChanged.connect(elm.checkStateChange)
					
				break
			except KeyError:
				# Entity is root or nothing found to link to the Entity
				print("FAILED to connect: %s <-> %s" % 
					(self.model.name, m.name))
				continue # no link possible between found and this entity
		
		if not can_be_drawn and not self.isRoot():
			# we can't connect or add a new entity
			raise CannotAddEntityException()
			
			
		# 3) CLASS ------------------------------------------------------------
		classes = self.model.listSubentities()
		if not len(classes):
			# Not a root entity type: show current class
			classes = [model.__class__]
			
		self.model.guiClassObjects = []
		for cls in classes:
			c = cls() # create instance
			c.guiChecked = c.name in model.defaultChecked
			self.model.guiClassObjects.append(c)

		ecm = EntityClassModel(self.model.guiClassObjects)
		ecm.itemChanged.connect(ecm.checkStateChange)
#		ecm.connect(ecm, QtCore.SIGNAL('itemChanged( QStandardItem *)'), ecm.foo)
#		ecm.item(0).setCheckState(QtCore.Qt.Checked)
#		QtGui.QStandardItem.checkState()
		
		
		
#		if not can_be_drawn:
#			# all items checked and no entity found to connect to
#			if self.isRoot(): # we must be the first entity!
#				elm = None # we don't do links then
#				# AbstractEntity: Title, AbstractEntityType: Movie
##				if isinstance(self.model, dataset.AbstractEntity):
##					# root level entity type: fill sub entity classes
##					pass
##				ecm = EntityClassModel(self.model.subentities)
#				ecm = EntityClassModel(self.model.listSubentities())
#		else:
#			
#			
#			
#			if not isinstance(self.model, dataset.AbstractEntityType):
#				# root level type: fill subentity classes
##				ecm = EntityClassModel(self.model.subentities)
#				if linkclass.attrDepClass:
#					ecm = None # don't show the same twice
#			else: # specific entity type
#				# if link and class match, show class nor link
#				if linkclass.attrDepClass: # Class Actor and link actor
#					ecm = None
#					elm = None
#					# try to display the single choice
#					ecm = EntityClassModel((self.model,))
#					elm = EntityLinkModel(linkInst)
#		
		
		if ecm is None:
			self.ui.classList.setHidden(True)
			self.ui.classList.setDisabled(True)
		if elm is None:
			self.ui.linkList.setHidden(True)
			self.ui.linkList.setDisabled(True)
		if eam is None:
			self.ui.attributeList.setHidden(True)
			self.ui.attributeList.setDisabled(True)
		self.ui.classList.setModel(ecm)	 
		self.ui.linkList.setModel(elm)
		self.ui.attributeList.setModel(eam)
		
#		self.ui.classList.clicked.connect(self.classListClicked)
#		self.ui.linkList.clicked.connect(self.linkListClicked)
		self.ui.attributeList.clicked.connect(self.attributeListClicked)
		
		# so the generation code can reach the models if necessary
		self.ecm = ecm
		self.elm = elm
		self.eam = eam
		if ecm and debug:
			modeltest.ModelTest(self.ecm, self)
		if elm and debug:
			modeltest.ModelTest(self.elm, self)
		if eam and debug:
			modeltest.ModelTest(self.eam, self)
		
#	def classListClicked(self, index): # PyQt4.QtCore.QModelIndex
#		cls = self.ui.classList.model().data(index, role=QtCore.Qt.UserRole).toPyObject()
#		print cls.name
#
#	def linkListClicked(self, index):
#		attribute = str(index.data().toPyObject())
#		
#		index.model().linkclass.guiChecked[attribute] =  \
#			index.data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked
#			
#		print index.model().linkclass.guiChecked
		
	def attributeListClicked(self, index):
		attribute = index.data(QtCore.Qt.UserRole).toPyObject()
		
		if attribute.__doc__:
			# remove tabs or four spaces at the beginning of each line
			out = ""
			for line in attribute.__doc__.split("\n"):
				out += line.lstrip("\t").lstrip("    ") + "\n"
			myapp.ui.docViewer.setPlainText(out)
			
		myapp.hideAllConstraints()
		
		# set label constraints
		a = attribute.entity.name
		b = attribute.name
		myapp.ui.attributeLabel.setText(a + ": " + b)
		
		for constraint in attribute.constraints:
			if constraint.enabled:
				state = QtCore.Qt.Checked
			else:
				state = QtCore.Qt.Unchecked
			if constraint.type == dataset.Constraint.AVAILABILITY:
				myapp.ui.attributeBox.show()
				myapp.ui.attributeBox.model = constraint
				myapp.ui.attributeBox.setCheckState(state)
				
				myapp.ui.availabilityComboBox.show()
				myapp.ui.availabilityComboBox.setCurrentIndex(constraint.unique)
			if constraint.type == dataset.Constraint.RANGE:
				myapp.ui.rangeBox.show()
				myapp.ui.rangeBox.model = constraint
				myapp.ui.rangeBox.setCheckState(state)
				
				myapp.ui.dials.show()
				myapp.ui.spinners.show()
				curMin = constraint.curMin
				curMax = constraint.curMax
				myapp.ui.startSpinBox.setMinimum(constraint.minimum)
				myapp.ui.startSpinBox.setMaximum(constraint.maximum)
				myapp.ui.stopSpinBox.setMinimum(constraint.minimum)
				myapp.ui.stopSpinBox.setMaximum(constraint.maximum)
				myapp.ui.minimumDail.setMinimum(constraint.minimum)
				myapp.ui.minimumDail.setMaximum(constraint.maximum)
				myapp.ui.maximumDial.setMinimum(constraint.minimum)
				myapp.ui.maximumDial.setMaximum(constraint.maximum)
				myapp.ui.startSpinBox.setValue(curMin)
				myapp.ui.stopSpinBox.setValue(curMax)
			if constraint.type == dataset.Constraint.VALUES:
				myapp.ui.valueBox.show()
				myapp.ui.valueBox.model = constraint
				myapp.ui.valueBox.setCheckState(state)
		
				myapp.ui.listWidgetValues.show()
				myapp.ui.checkAllButton.show()

				myapp.ui.listWidgetValues.clear()
				for val in attribute.values:
					item = QtGui.QListWidgetItem(val)
					if constraint.values[val]:
						item.setCheckState(QtCore.Qt.Checked)
					else:
						item.setCheckState(QtCore.Qt.Unchecked)
					myapp.ui.listWidgetValues.addItem(item)

	def setRoot(self, rbool):
		"""This entity is the class where we start to generate from. The
		database queries will be generated from here. """
		self.model.generationRoot = rbool
		self._rootChange()
	def isRoot(self):
		return self.model.generationRoot
	generationRoot = property(fget=isRoot, fset=setRoot)
	
	def _rootChange(self):
		colour = "red'>[root] " if self.generationRoot else "black'>"
		template = "<font color='{colour}{text}</font>"
		text = template.format(colour=colour, text=self.model.name,)
		self.ui.entityLabel.setText(text)
		
class EntityLinkModel(QtGui.QStandardItemModel):
	"""Model of the Links list in the EntityWidget (middle)"""
	def __init__(self, linkclass, parent=None, *args):
		QtGui.QStandardItemModel.__init__(self, parent, *args) 
		items = linkclass.types.items()
		self.linkclass = linkclass
		
		# check all when there is only one link
		# (e.g. filmography with character)
		unique = False
		if len(items) == 1:
			unique = True

		for _key, v in items:
			item = QtGui.QStandardItem(v)
			item.setCheckable(True)
			item.setData(QtCore.QVariant(QtCore.Qt.Unchecked), 
						 QtCore.Qt.CheckStateRole)
			if unique:
				item.setCheckState(QtCore.Qt.Checked)
			self.appendRow(item)
		
	def checkStateChange(self, item):
		attribute = str(item.data(QtCore.Qt.DisplayRole).toPyObject())
		self.linkclass.guiChecked[attribute] =  \
			item.data(QtCore.Qt.CheckStateRole) == QtCore.Qt.Checked
		
class EntityAttributeModel(QtGui.QStandardItemModel):
	"""Model of the attributes list in the EntityWidget (bottom)""" 
	def __init__(self, attrlist, parent=None, *args): 
		""" attrlist: a list where each item is a row
		Stored data: AbstractAttribute """
		QtGui.QStandardItemModel.__init__(self, parent, *args) 
		self.listdata = attrlist
		
		for attribute in attrlist:
			item = QtGui.QStandardItem(attribute.name)
			item.setCheckable(True)
			item.setData(QtCore.QVariant(QtCore.Qt.Unchecked), 
						 QtCore.Qt.CheckStateRole) #QtCore.Qt.PartiallyChecked
			if attribute.guiChecked:
				item.setCheckState(QtCore.Qt.Checked)
			self.appendRow(item)
		
	def data(self, index, role): 
		if index.isValid() and role == QtCore.Qt.UserRole:
#			return self.listdata[index.row()]
			return QtCore.QVariant(self.listdata[index.row()])
		else: 
			return QtGui.QStandardItemModel.data(self, index, role)
		
	def checkStateChange(self, item):
		self.listdata[item.row()].guiChecked = (item.checkState() == QtCore.Qt.Checked)
		
class EntityClassModel(EntityAttributeModel):
	"""Model of the class list in the EntityWidget (top)"""
	def __init__(self, clslist, parent=None, *args): 
		""" clslist: a list where each item is a row 
		Stored data: subclasses of AbstractEntity """
		QtGui.QStandardItemModel.__init__(self, parent, *args) 
		self.listdata = clslist
		
		# one thing: LOCK it
		enabled = True 
		if len(self.listdata) == 1:
			enabled = False
			# check it
			self.listdata[0].guiChecked = True
		
		for cls in clslist:
			item = QtGui.QStandardItem(cls.name)
			item.setCheckable(True)
			item.setEnabled(enabled)
			item.setData(QtCore.QVariant(QtCore.Qt.Unchecked), 
						 QtCore.Qt.CheckStateRole)
			if cls.guiChecked:
				item.setCheckState(QtCore.Qt.Checked)
			self.appendRow(item)
			
#	# make sure checking changes the model too
#	def itemChanged(self, item):
#		self.listdata[item.row()].guiChecked = (item.checkState() == QtCore.Qt.Checked)
#		print 'item changed'
			
#	def checkStateChange(self, item):
#		self.listdata[item.row()].guiChecked = (item.checkState() == QtCore.Qt.Checked)
#		print 'item changed works'
			
class WidgetProxy(QtGui.QGraphicsProxyWidget):
	"""Modified QGraphicsProxyWidget so we can actually move the widget."""
	#http://www.qtcentre.org/threads/41800-QGraphicsProxyWidget-does-not-behave-as-child-of-QGraphicsWidget

	def __init__(self, widget, parent=None, wFlags=QtCore.Qt.Widget):
		QtGui.QGraphicsProxyWidget.__init__(self, parent, wFlags)
		self.setWidget(widget)
		self.setFlag(QtGui.QGraphicsItem.ItemIsSelectable, True)
		self.setFlag(QtGui.QGraphicsItem.ItemIsMovable, True)
		self.setFlag(QtGui.QGraphicsItem.ItemClipsToShape, False)
		self.setFlag(QtGui.QGraphicsItem.ItemSendsGeometryChanges, True)
		self.grabbedBlock = False
		
		self.links = []
		
	def representsRoot(self):
		return self.widget().generationRoot
		
	def mousePressEvent(self, e):
		alienWidget = self.widget().childAt(e.pos().toPoint())
		if not alienWidget:
			QtGui.QGraphicsProxyWidget.mousePressEvent(self, e)
			self.grabbedBlock = False
		elif isinstance(alienWidget, QtGui.QLabel):
			QtGui.QGraphicsItem.mousePressEvent(self, e)
			self.grabbedBlock = True
		else:
			QtGui.QGraphicsProxyWidget.mousePressEvent(self, e)
			self.grabbedBlock = False

	def mouseMoveEvent(self, e):
		if self.grabbedBlock:
			QtGui.QGraphicsItem.mouseMoveEvent(self, e)
		else:
			QtGui.QGraphicsProxyWidget.mouseMoveEvent(self, e)
		
	def mouseReleaseEvent(self, e):
		if self.grabbedBlock:
			QtGui.QGraphicsItem.mouseReleaseEvent(self, e)
		else:
			QtGui.QGraphicsProxyWidget.mouseReleaseEvent(self, e)
		self.grabbedBlock = False

	selectionChanged = QtCore.pyqtSignal(QtGui.QGraphicsItem)
	
	def itemChange(self, change, value):
		if change == QtGui.QGraphicsItem.ItemSelectedChange:
			if not self.isSelected(): # it will be selected
				self.selectionChanged.emit(self)
				# http://www.informit.com/articles/article.aspx?p=1174421&seqNum=4
		return value
	
	def addLink(self, link):
		self.links.append(link)
		
	def removeLink(self, link):
		self.links.remove(link)
		
	def paint(self, painter, option, widget=None):
		QtGui.QGraphicsProxyWidget.paint(self, painter, option, widget)
		
		if self.isSelected(): # color the block
			pen = QtGui.QPen(QtCore.Qt.DashLine)
			pen.setWidth(1)
			pen.setColor(QtCore.Qt.red)
			painter.setPen(pen)
			rect = self.rect()
			painter.drawRect(rect)
			
	def delink(self):
		links = self.links
#		print "before delink", links
		for link in iter(links):
			link.removeLinks()
			scene.removeItem(link)
#		print "after delink", links
		
	def __del__(self):
		self.delink()
		# bad
		# http://docs.python.org/library/gc.html#gc.garbage
		# http://excess.org/article/2011/12/unfortunate-python/
		
	def __lt__(self, other):
		"""The sort routines are guaranteed to use __lt__ when making 
		   comparisons between two objects."""
		# for putting the root entity at the beginning after "sorting"
		return self.representsRoot()
		
class DiagramScene(QtGui.QGraphicsScene):
	"""The QGraphicsScene class provides a surface for managing a large number
	of 2D graphical items. The class serves as a container for QGraphicsItems.
	Handles what can be drawn or not."""
	# http://www.informit.com/articles/article.aspx?p=1174421&seqNum=4
#	itemSelected = QtCore.pyqtSignal(QtGui.QGraphicsItem)
#	
	def __init__(self, parent=None):
		super(DiagramScene, self).__init__(parent)
		
	def dragEnterEvent(self, e):
		if e.mimeData().hasFormat('application/x-qabstractitemmodeldatalist'):
			e.accept()
		else:
			e.ignore()

	def dropEvent(self, event):
		event.acceptProposedAction()
		srcw = event.source()
		entity = srcw.model().data(srcw.currentIndex(), QtCore.Qt.UserRole)
		drawEntity(entity, event.scenePos())

	def dragMoveEvent(self, event):
		event.acceptProposedAction()

	def canNewEntityBeRoot(self):
		for item in self.items():
			if isinstance(item, WidgetProxy):
				if item.representsRoot():
					return False
		return True
	
	def getAllModelsAsPythonList(self):
		model_list = []
		for item in self.items():
			if isinstance(item, WidgetProxy):
				model_list.append(item.widget().model)
		return model_list
		
#http://www.qtcentre.org/threads/24328-PyQt-gt-QTreeWidget-to-QGraphicsView-drop-failure
#http://www.qtcentre.org/threads/17090-Drar-and-Drop-on-QGraphicsView

class Link(QtGui.QGraphicsLineItem):
	"""Line drawn to connect two QGraphicsProxyWidgets."""
	def __init__(self, oldItem, newItem, parent=None, scene=None):
		super(Link, self).__init__(parent, scene)
		self.myStartItem = oldItem
		self.myEndItem = newItem
		
		self.myStartItem.addLink(self);
		self.myEndItem.addLink(self);
		
		# so that it will always be drawn underneath the nodes it connects
		self.setZValue(-1)
		
	def removeLinks(self):
		try:
			self.myStartItem.removeLink(self)
		except ValueError:
			print("remove start link failed")
		try:
			self.myEndItem.removeLink(self)
		except ValueError:
			print("remove end link failed")

	def startItem(self):
		return self.myStartItem

	def endItem(self):
		return self.myEndItem

	def updatePosition(self):
		""" The updatePosition function is used to update the line's endpoints, 
		when the user drags a connected node into a different position. """
		s = self.myStartItem # proxy
		e = self.myEndItem
		sw = self.myStartItem.widget()
		ew = self.myEndItem.widget()
		line = QtCore.QLineF(self.mapFromItem(s, sw.width()/2, sw.height()/2), 
							 self.mapFromItem(e, ew.width()/2, ew.height()/2))
		self.setLine(line)

	def paint(self, painter, option, widget=None):
		if (self.myStartItem.collidesWithItem(self.myEndItem)):
			return
		self.updatePosition()
		painter.setPen(QtGui.QPen(QtCore.Qt.darkGreen, 5, QtCore.Qt.SolidLine))
		painter.setRenderHint(QtGui.QPainter.Antialiasing)
		painter.drawLine(self.line())
		
def showInStatusBar(message=""):
	myapp.statusBar().showMessage(message)
	
def drawEntity(entityClass, pos=QtCore.QPointF()):
	""" entityClass: kind of entity to draw e.g. Movie, Actor
	pos: if given, position to draw new block (when using drag and drop) """
	try:
		print "draw", entityClass
		try:
			einst = entityClass()
			einst.generationRoot = scene.canNewEntityBeRoot()
		except TypeError:
			einst = entityClass
			
		# None because EntityWidget needs proxy instance?
		proxy = WidgetProxy(None)
		ew = EntityWidget(einst, proxy)
		proxy.setWidget(ew)
		
		proxy.setPos(pos)
		scene.addItem(proxy)
		
		# draw the line between the two entities
		if not einst.generationRoot:
			Link(ew.newLinkedProxy, proxy, None, scene)
	except TypeError:
		print sys.exc_info()
		showInStatusBar("No entity is selected")
	except CannotAddEntityException:
		QtGui.QMessageBox.information(None, 'Message',
		"You cannot add this type of entity.", 
		QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
		
def removeSelectedEntities():
	si = scene.selectedItems()
	for item in si:
		scene.removeItem(item) # override this method in DiagramScene
		item.__del__()
		# one of the dual links stays drawn
		# only half of them actually get removed
		
def getRootWidget():
	for item in scene.items(): # iterates WidgetProxy objects
		try:
			if item.representsRoot():
				return item.widget()
		except AttributeError:
			pass
			
def generate():
	if myapp.thread.isRunning():
		print("Generation is already running.")
		return
		
	rw = getRootWidget()
	if not rw:
		QtGui.QMessageBox.information(None, 'Message',
		"No root entity found.", 
		QtGui.QMessageBox.Ok, QtGui.QMessageBox.Ok)
		return
	
	# let the user choose the output file if left empty
	myapp.output = str(myapp.ui.outputFilePath.text())
	while not myapp.output:
		myapp.askOutputFile()
		myapp.output = str(myapp.ui.outputFilePath.text())
	
	print("Starting...")
	# disable generate button and enable cancel button
	myapp.ui.actionGenerate.setEnabled(False)
	myapp.showCancelButton(True)
	
	amount = myapp.ui.rootEntityAmount.value()
	print("amount: %d" % amount)
	
	myapp.generationProgress(0, amount)
	
	random = myapp.ui.randomBox.checkState() == QtCore.Qt.Checked
	if random:
		print("Random!")
	
	# let this run in a separate thread
	myapp.thread.generate(amount, myapp.output, scene, random)
	
def sortOutputFile(pfile):
	"""Remove duplicate lines and sort the output file."""
	with open(pfile, 'r') as unsorted:
		lines = unsorted.readlines()
	
	with open(pfile, 'w') as sortedfacts:
		for line in sorted(set(lines)):
			sortedfacts.write(line)				
	
def importDataset(name):
	""" for imdbmodel.py -> imdbmodel """
	global dataset #@UnusedVariable
	try:
		dataset = __import__(name)
		print("Dataset %s is selected." % name)
	except:
		print("Unable to import '%s' dataset. Using IMDb." % name)

if __name__ == "__main__":
	try: # first parameter specifies the dataset
		importDataset(sys.argv[1])
	except IndexError:
		pass # no parameter given, do nothing, use default
	app = QtGui.QApplication(sys.argv)
	myapp = MainWindow()
	myapp.show()
	sys.exit(app.exec_())
