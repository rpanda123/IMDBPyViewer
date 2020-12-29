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

'''
Created on 24-jun.-2011

data framework

@author: Jef Van den Brandt
'''
from abc import ABCMeta, abstractproperty

# --- basic -------------------------------------------------------------------
	
class AbstractEntity(object):
	""" e.g. Title """
	__metaclass__ = ABCMeta
	# http://www.doughellmann.com/PyMOTW/abc/
	
	def _toImplement(self):
		raise NotImplementedError()

	name = abstractproperty(_toImplement)
	
	subentities = [] # e.g. Actor for Person
	defaultChecked = [] # which subclasses will get checked after drawing
	rootLevelEntityType = None
	links = {} # the possible links between other entities
	generationRoot = False # where we start to generate everything from
	
	def __init__(self):
		# reinitialise to prevent the configuration of the parent
		pass
		
	def __str__(self):
		return self.name
	
	@classmethod
	def listSubentities(cls):
		"""Returns a list of all more specific entities."""
		return cls.__subclasses__()
	
class AbstractAttribute(object):
	""" Holds the value of an attribute after database access.
	e.g. year of a Movie """
	__metaclass__ = ABCMeta
	
	def __init__(self, concreteEntity, guiChecked=True):
		# entity of which this is an attribute
		if isinstance(concreteEntity, AbstractEntity):
			self.entity = concreteEntity
		else:
			raise AttributeError("Instance of a concrete entity expected.")
		
		# Whether this attribute is chosen for dataset generation.
		self.guiChecked = guiChecked
		
		self.constraints = []
		
	def checkConstraint(self, data):
		"""True: no constraint fails"""
		for constraint_checker in self.constraints:
			if not constraint_checker.check(self, data):
				return False
		return True
	
class AbstractConstraintChecker(object):
	""" Holds the value of an attribute after database access.
	e.g. year of a Movie """
	__metaclass__ = ABCMeta
	
	def __init__(self, enabled=False):
		self.enabled = enabled
	
	def check(self, attribute, data):
		"""Checks a constraint.
		True means the constraint succeeds."""
		return True
	
class AbstractEntityType(AbstractEntity):
	""" e.g. Movie
	More specific than AbstractEntity. Mix-in.
	It makes a difference for data generation. """
	
	subentities = [] # e.g. Actor for Person
	defaultChecked = [] # which subclasses will get checked after drawing
	
	def __init__(self):
		super(AbstractEntity, self).__init__()
	
class AbstractLink(object):
	"""Abstract Link class. Connects two AbstractEntity classes that can
	have a relation defined between them."""
	__metaclass__ = ABCMeta
	
	def __init__(self, one, two):
		"""One is the owning relationship."""
		self.setOne(one)
		self.setTwo(two)
		if not self._canLink():
			raise ValueError("No link possible between these two entities.")
		
		# dict: link: True/False for being checked
		self.guiChecked = {}
	
	def _canLink(self):
		try: # checks if entities can be linked together
			return bool(self._one.links[self._two.rootLevelEntityType])
		except KeyError:
			return False
		
	def getOne(self):
		return self._one
	def getTwo(self):
		return self._two
	def setOne(self, value):
		if isinstance(value, AbstractEntity):
			self._one = value
		else:
			raise ValueError("AbstractEntity instance required.")
	def setTwo(self, value):
		if isinstance(value, AbstractEntity):
			self._two = value
		else:
			raise ValueError("AbstractEntity instance required.")
	
#	one = abstractproperty(getOne, setOne)
#	two = abstractproperty(getTwo, setTwo)
	
def esc(text):
	"""Make sure all the Prolog facts can be loaded."""
	return text.encode("ascii", "replace").encode('string-escape')
