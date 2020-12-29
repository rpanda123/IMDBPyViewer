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

## Database configuration options
SQLDB = "postgresql" # mysql postgresql
LOGIN = "imdb"
PASSWORD = "imdbpwd"
HOST = "localhost"
PORT = "5432" # 3306 5432
DBNAME = "imdb"


from dfw import AbstractEntity, AbstractEntityType, AbstractLink
from imdbattr import *
import traceback

# http://www.blog.pythonlibrary.org/2012/08/02/python-101-an-intro-to-logging/
# CRITICAL ERROR WARNING INFO DEBUG
import logging
logging.basicConfig(level=logging.INFO, format=
				'%(asctime)s %(levelname)s %(message)s')
#logging.basicConfig(filename="sample.log", level=logging.INFO)

"""
Limitations:

 - PostgreSQL Unreliable Default Sort Order
   http://developer.newsdesk.se/2010/05/11/
   postgresql-random-sort-order-causing-random-rails-test-failures/

To debug threaded code:
 - http://code.google.com/p/winpdb/wiki/DebuggingTutorial
   Not tested myself
 - PyDev for Eclipse, but 
   http://stackoverflow.com/questions/3929036/eclipse-wont-break-in-threads

Ideeën voor het ontwerp:

http://stackoverflow.com/questions/5849020/how-can-i-retrieve-a-given-number-
of-movies-under-a-given-genre-using-imdbpy/7826575#7826575

To count the amount of titles in an output file:
  findall(X, title(X), Y), length(Y, S), writeln(S).

The amount of directors:  
  direc(X) :- person(X), director(_,X).
  findall(X, direc(X), Y), sort(Y, Z), length(Z, S), writeln(S).

"""

###############################################################################
## IMDbPY stuff ###############################################################
###############################################################################

def getConnectionString():
	"""More in README.sqldb file imdbpy.
	Where the 'URI' argument is a string representing the connection
	to your database, with the schema:
	  scheme://[user[:password]@]host[:port]/database[?parameters]
	"""
	return "%s://%s:%s@%s:%s/%s" % (SQLDB, LOGIN, PASSWORD, HOST, PORT, DBNAME)

imdbInstance = None

def getImdbpyInstance():
	"""Database stuff in external file for faster startup times."""
	global imdbInstance
	if not imdbInstance:
		import imdbdb
		imdbInstance = imdbdb.imdb.IMDb(accessSystem='sql',
			  uri=getConnectionString(), 
			  useORM='sqlalchemy')
	return imdbInstance

###############################################################################
## IMDb dataset construction ##################################################
###############################################################################

## Entity Mix-ins #############################################################

class ImdbEntity(AbstractEntity):
	def __init__(self):
		super(ImdbEntity, self).__init__()
		
		self.good_ids = []
		self.bad_ids = [] # to speed up when doing random
		self.toproc_ids = []
		self.link_ids = {} # list with linked Prolog lines
		
	def process(self, title_key, link_models, output_file):
		raise NotImplementedError("Implement this function with the entity.")
		
	def doAll(self, key, data, link_models, output_file):
		"""Check constraints and generate Prolog."""
		# CLASS
		try:
			good = self.checkClassConstraint(key, data)
		except KeyError:
			# IMDbParserError: invalid title: """"
			# if data['kind'] == Title.imdbpyType[cat-1]:
			# KeyError: 'kind'
			good = False
			logging.error("Class constraint failed on %d." % key)
		
		# ATTRIBUTE
		if good:	
			for attr in self.attributes:
				if not attr.checkConstraint(data):
					good = False
					break
		
		# add to good or bad list
		if good:
			# write Prolog
			lines = self.generatePrologEntity(key, data)
			with open(output_file, "at") as out:
				out.write(lines.encode("ascii", "replace"))
				out.write("\n")
				logging.debug(lines)
			
				# do links (not their content)
				for linkmodel in link_models: # links to other entities
					# grab checked links from model GUI (kind of link)
					checked_links = [l for l, status in 
									linkmodel.guiChecked.items() if status]
										
					for checked_link in checked_links: # string links
						try:
							# e.g. Persons
							for i, entity in enumerate(linkmodel
									.getLinkedEntities(data, checked_link)):
								eid = entity.getID()
								# so the next entity knows what to generate
								linkmodel.getTwo().toproc_ids.append(eid)
								
								line = linkmodel.constructLink(
										checked_link, key, eid, i+1)
								
								lst = linkmodel.getTwo().link_ids.get(eid, [])
								lst.append(line)
								linkmodel.getTwo().link_ids[eid] = lst
								
#								# write link Prolog
#								out.write(line)
#								print(line) # XXX: Prolog
						except KeyError:
							pass # Entity doesn't have a certain checked_link
			
			# so we will know what to skip directly when doing random
			self.good_ids.append(key)
		else:
			self.bad_ids.append(key)
			
		return good
	
	def generatePrologEntity(self, key, data):
		return_lines = ""
		
		# do the links from previous entities to this entity
		for line in self.link_ids.get(key, []):
			return_lines += line
			
		return_lines += "\n"
		
		return_lines += self.genPrologEntityFact(key, data)
		
		for attr in self.attributes:
			if attr.guiChecked:
				try:
					lines = attr.generateProlog(key, data)
				except KeyError:
					# the attribute isn't available
					lines = ""
				except: # catch unknown errors
					print("Unknown error!!! See problem.txt")
					logging.critical(sys.exc_info())
					with open("problem.txt", "a") as problem_file:
						traceback.print_exc(file=problem_file)
					lines = ""
				return_lines += lines
		
		return return_lines
	
	def genPrologEntityFact(self, key, item):
		"""All the basic facts. Reimplement for more facts."""
		ret = "%s(%s%d).\n" % (self.rootLevelEntityType.name.lower(), 
							self.key_prefix, key)
		return ret

	def checkClassConstraint(self, key, data):
		logging.error("default function called! checkClassConstraint()")
		return True

class ClassConstraintLinkMixin(object):
#	def checkClassConstraint2(self, key, data):
#		"""All the links must exist."""
#		success = True
#		for ecm in self.guiClassObjects:
#			if ecm.guiChecked:
#				# the link must exist
#				try:
#					if not len(data[ecm.imdbpyType]):
#						success = False
#						break
#				except KeyError:
#					success = False
#					break
#		return success

	# XXX: change behaviour of the class box here
	
	def checkClassConstraint(self, key, data):
		"""One of the links must exist."""
		success = False
		for ecm in self.guiClassObjects:
			if ecm.guiChecked:
				try:
					if len(data[ecm.imdbpyType]):
						success = True
						break
				except KeyError:
					pass
		return success
		
# -----------------------------------------------------------------------------

class Title(ImdbEntity):
	name = "Title"
	key_prefix = "t"
	
#	# defines the list of available groups that contain a bunch of properties
#	# for querying through IMDbPy
#	infoGroups = ('main', 'plot', 'taglines', 'keywords', 'alternate versions',
#				  'crazy credits', 'goofs', 'quotes', 'release dates', 
#				  'vote details', 'connections', 'trivia')
	
	# table kind_type
	imdbpyType = ['movie', 'tv series', 'tv movie', 'video movie',
						'tv mini series', 'video game', 'episode']
	
	def __init__(self):
		super(Title, self).__init__()
		self.defaultChecked = ['Movie', 'TV Movie']
		self.votes = Votes(self, True) # for faster querying
		self.attributes = [
				TitleKind(self),
				TitleName(self),
				Year(self),
				SeriesEndYear(self),
#				EpisodeCount(self),
#				SeasonCount(self),
				Genres(self),
				Countries(self),
				Keywords(self, True),
				
				VotesDistribution(self, True),
				self.votes,
				Rating(self, True),
				Top250Rank(self, True),
				Bottom10Rank(self),
				
				AlternateVersions(self),
				Runtime(self),
				ColorInfo(self),
				
				CameraModel(self),
				FilmLength(self),
				FilmNegativeFormat(self),
				PrintedFilmFormat(self),
				AspectRatio(self),
				CinematographicProcess(self),
				Laboratory(self),
				
				Languages(self),
				Certificates(self),
				SoundMix(self),
				ReleaseDates(self, True),
#				GoofTypes(self),
#				Locations(self),
#				SoundTrack(self),

		#	   Novel(self),
		#	   Adaptation(self),
		#	   Book(self),
		
				ProductionDays(self),
				FilmingDays(self),

				Budget(self),
				WeekendGross(self),
				OpeningWeekend(self),
				Gross(self),
				Rentals(self),
				Admissions(self),
			]
		
#		self.guiClassObjects = [Movie] # for unit tests declared here
	
	def _getListTypesClasses(self):
		"""Converts the imdbpyType name to the corresponding number
		in the database so we can filter on the type of title (movie,...)
		(table kind_type)"""
		numberList = []
		for ecm in self.guiClassObjects:
			if ecm.guiChecked:
				for i, name in enumerate(Title.imdbpyType):
					if name == ecm.imdbpyType:
						numberList.append(i+1)
						break
		return numberList
						
	def grabIds(self, amount, offset=0, random=False):
		"""Grabs the given amount of ids. The ids will be used to grab
		the attributes of this entity later."""
		# we can already filter on movie, serie,...
		categories = self._getListTypesClasses()
		logging.debug("Title categories checked: %s" % categories)
		if not len(categories):
			raise AttributeError("No classes selected.") # TODO: show in GUI
		
		ok = True
		for const in self.votes.constraints:
			if const.type == Constraint.RANGE:
				ok = const.enabled and ok
				minval = const.curMin 
			if const.type == Constraint.AVAILABILITY:
				ok = const.enabled and ok
		
		if ok:
			votes = minval
			logging.info("Using FAST vote amount query.")
		else:
			votes = None
		
		for tid in getImdbpyInstance().getTitles(categories=categories,
				offset=offset, limit=amount, random=random, votes=votes):
			# skip ids that were already processed before (when doing random)
			if not tid in self.good_ids and not tid in self.bad_ids:
				self.toproc_ids.append(tid)
				
	def process(self, title_key, link_models, output_file):
		"""title_key: PK of title record IMDbPY"""
		# grab movie info
		title_data = getImdbpyInstance().get_movie(title_key, 'main')
		
		return super(Title, self).doAll(title_key, title_data, 
									link_models, output_file)
	
	def checkClassConstraint(self, key, data):
		success = False
		
		# succeed if one of the categories is ok for this entity
		categories = self._getListTypesClasses()
		
		if not len(categories):
			print("class failure!")
			raise AttributeError("One of the categories must be selected.")
		
		for cat in categories:
			if data['kind'] == Title.imdbpyType[cat-1]:
				success = True
		
		return success

	
	def genPrologEntityFact(self, key, item):
		ret = super(Title, self).genPrologEntityFact(key, item)
		ret += "%s(%s%d).\n" % (item['kind'].replace(' ', '_').lower(), 
							self.key_prefix, key)
		return ret
	
class Movie(Title, AbstractEntityType):
	name = "Movie"
	imdbpyType = "movie" # 1 (key in database table kind_type)
	defaultChecked = [name]

class Series(Title, AbstractEntityType):
	name = "Series"
	imdbpyType = "tv series" # 2
	defaultChecked = [name]
	
class TVMovie(Title, AbstractEntityType):
	name = "TV Movie"
	imdbpyType = "tv movie" # 3
	defaultChecked = [name]

class Video(Title, AbstractEntityType):
	name = "Straight to video"
	imdbpyType = "video movie" # 4
	defaultChecked = [name]

class MiniSeries(Title, AbstractEntityType):
	# does not exist in my db
	name = "Miniseries"
	imdbpyType = "tv mini series" # 5
	defaultChecked = [name]

class VideoGame(Title, AbstractEntityType):
	name = "Video Game"
	imdbpyType = "video game" # 6
	defaultChecked = [name]
	
class Episode(Title, AbstractEntityType):
	name = "Episode"
	imdbpyType = "episode" # 7 
	defaultChecked = [name]
	
# -----------------------------------------------------------------------------

class Person(ClassConstraintLinkMixin, ImdbEntity):
	# XXX: notice that every name in the cast is a Person object, with a
	#      currentRole instance variable, which is a string for the played role.
	#cast = movie.get('cast')
	#if cast:
	#    print 'Cast: '
	#    cast = cast[:5]
	#    for name in cast:
	#        print '      %s (%s)' % (name['name'], name.currentRole)
			
	#TODO: extra addidtional attribute for Person roles (invisible) so can be used as output	
	# Character: http://www.imdb.com/character/ch0000741/
	# not all in sql db
	
	name = "Person"
	key_prefix = "p"
#	infoGroups = ('main', 'filmography', 'biography', 'other works')

	def __init__(self):
		super(Person, self).__init__()
		self.defaultChecked = ['Actor', 'Actress', 'Director', 'Writer']
		self.attributes = [
						PersonName(self),
						
						BirthCountry(self),
						BirthState(self),
						BirthCity(self),
						BirthYear(self),
						BirthMonth(self),
						BirthDay(self),
						
						DeathCountry(self),
						DeathState(self),
						DeathCity(self),			
						DeathYear(self),
						DeathMonth(self),
						DeathDay(self),
						
						BirthName(self, False), # not checked by default
						Spouses(self),
						Children(self),
						FirstMarriageYear(self),
						LastDivorceYear(self),
						
						Gender(self),
						Height(self),
		]
		
	def grabIds(self, amount, offset=0, random=False):
		"""Grabs the given amount of ids. The ids will be used to grab
		the attributes of this entity later."""
		for pid in getImdbpyInstance().getPersons(offset=offset, limit=amount,
		                                          random=random):
			# skip ids that were already processed before (when doing random)
			if not pid in self.good_ids and not pid in self.bad_ids:
				self.toproc_ids.append(pid) 
				
	def process(self, person_key, link_models, output_file):
		person_data = getImdbpyInstance().get_person(person_key)
		
		return super(Person, self).doAll(person_key, person_data, 
										link_models, output_file)
	
class Actor(Person, AbstractEntityType):
	name = "Actor"
	imdbpyType = "actor"

class Actress(Person, AbstractEntityType):
	name = "Actress"
	imdbpyType = "actress"

class Producer(Person, AbstractEntityType):
	name = "Producer"
	imdbpyType = "producer"

class Writer(Person, AbstractEntityType):
	name = "Writer"
	imdbpyType = "writer"
	
class Director(Person, AbstractEntityType):
	name = "Director"
	imdbpyType = "director"

class Cinematographer(Person, AbstractEntityType):
	name = "Cinematographer"
	imdbpyType = "cinematographer"

class Composer(Person, AbstractEntityType):
	name = "Composer"
	imdbpyType = "composer"

class CostumeDesigner(Person, AbstractEntityType):
	name = "CostumeDesigner"
	imdbpyType = "costume designer"

class Editor(Person, AbstractEntityType):
	name = "Editor"
	imdbpyType = "editor"
	
class MiscCrew(Person, AbstractEntityType):
	name = "MiscCrew"
	imdbpyType = "miscellaneous crew"

class ProductionDesigner(Person, AbstractEntityType):
	name = "ProductionDesigner"
	imdbpyType = "production designer"

class Guest(Person, AbstractEntityType):
	name = "Guest"
	imdbpyType = "guest"

# -----------------------------------------------------------------------------	
	
class Company(ClassConstraintLinkMixin, ImdbEntity):
	name = "Company"
	key_prefix = "co"

	def __init__(self):
		super(Company, self).__init__()
		
		self.defaultChecked = ["Distributor", "Production company",
							"Special effects company", "Miscellaneous company"]
		self.attributes = [
				CompanyName(self),
				CompanyCountry(self),
				]
	
		
	def grabIds(self, amount, offset=0, random=False):
		"""Grabs the given amount of ids. The ids will be used to grab
		the attributes of this entity later."""
		for pid in getImdbpyInstance().getCompanies(offset=offset, 
											limit=amount, random=random):
			# skip ids that were already processed before (when doing random)
			if not pid in self.good_ids and not pid in self.bad_ids:
				self.toproc_ids.append(pid) 
				
	def process(self, company_key, link_models, output_file):
		if not len(link_models) and self.allCompaniesSelected():
			# speed up by not processing company links
			company_data = getImdbpyInstance().getCompany(company_key)
		else:
			company_data = getImdbpyInstance().get_company(company_key)
		
		return super(Company, self).doAll(company_key, company_data, 
										link_models, output_file)
		
	def allCompaniesSelected(self):
		result = True
		for ecm in self.guiClassObjects:
			if not ecm.guiChecked:
				result = False
				break
		logging.debug("All companies selected: %s" % str(result))
		return result

class Distributor(Company, AbstractEntityType):
	name = "Distributor"
	imdbpyType = "distributors"

class Production(Company, AbstractEntityType):
	name = "Production company"
	imdbpyType = "production companies"
	
class SpecialEffects(Company, AbstractEntityType):
	name = "Special effects company"
	imdbpyType = "special effects companies"
	
class Miscellaneous(Company, AbstractEntityType):
	name = "Miscellaneous company"
	imdbpyType = "miscellaneous companies"

# -----------------------------------------------------------------------------

class Character(ImdbEntity):
	name = "Character"
	key_prefix = "ch"
	
	def __init__(self):
		super(Character, self).__init__()
		
		self.defaultChecked = ['Character']
		self.attributes = [
				CharacterName(self, True),
				]
		
	def process(self, character_key, link_models, output_file):
		character_data = getImdbpyInstance().get_character(character_key)
		
		return super(Character, self).doAll(character_key, character_data, 
										link_models, output_file)
		
	def grabIds(self, amount, offset=0, random=False):
		"""Grabs the given amount of ids. The ids will be used to grab
		the attributes of this entity later."""

		for cid in getImdbpyInstance().getCharacters(offset=offset,
													 limit=amount,
													 random=random):
			# skip ids that were already processed before (when doing random)
			if not cid in self.good_ids and cid not in self.bad_ids:
				self.toproc_ids.append(cid)
				
	def checkClassConstraint(self, key, data):
		# we are always a character
		return True
	
###############################################################################

class ImdbLink(AbstractLink):
	def constructLink(self, link_string, parent_key, linked_key, *args):
		parent = self.getOne()
		linked = self.getTwo()
		link_kind = link_string.replace(" ", "_")
		return "%s(%s%d, %s%d).\n" % (link_kind, 
									parent.key_prefix, parent_key, 
									linked.key_prefix, linked_key)

	def getLinkedEntities(self, pvalue, checked_link):
		"""TitleLinkTitle has an additional layer."""
		return pvalue[checked_link]
	
class TitleLinkTitle(ImdbLink):
	""" link_type table """
	types = {   1: 'follows',
				2: 'followed by',
				3: 'remake of',
				4: 'remade as',
				5: 'references',
				6: 'referenced in',
				7: 'spoofs',
				8: 'spoofed in',
				9: 'features',
				10: 'featured in',
				11: 'spin off from',
				12: 'spin off',
				13: 'version of',
				14: 'similar to',
				15: 'edited into',
				16: 'edited from',
				17: 'alternate language version of',
				18: 'unknown link',
			}
	
	def getLinkedEntities(self, pvalue, checked_link):
		return pvalue['connections'][checked_link]
	
class TitleLinkPerson(ImdbLink):
	types = {   1: 'cast',
#				1: 'actor', # cast
#				2: 'actress', # cast
				3: 'producer',
				4: 'writer',
				5: 'cinematographer',
				6: 'composer',
				7: 'costume designer',
				8: 'director',
				9: 'editor',
				10: 'miscellaneous crew',
				11: 'production designer',
				12: 'guest',
			}
	
	def constructLink(self, link_string, parent_key, linked_key, index):
		if link_string != 'cast':
			return super(TitleLinkPerson, self).constructLink(link_string,
													parent_key,
													linked_key)
		else: # add the cast order
			parent = self.getOne()
			linked = self.getTwo()
			return "cast(%s%d, %s%d, %d).\n" % (
										parent.key_prefix, parent_key, 
										linked.key_prefix, linked_key,
										index)

class TitleLinkCompany(ImdbLink):
	types = {   1: 'distributors',
				2: 'production companies',
				3: 'special effects companies',
				4: 'miscellaneous companies',
			}
	
class PersonLinkTitle(TitleLinkPerson):
	types = {	1: 'actor',
				2: 'actress',
				3: 'producer',
				4: 'writer',
				5: 'cinematographer',
				6: 'composer',
				7: 'costume designer',
				8: 'director',
				9: 'editor',
				10: 'miscellaneous crew',
				11: 'production designer',
				12: 'guest', 
			}
	
class CompanyLinkTitle(TitleLinkCompany): 
	pass

class CharacterLinkTitle(ImdbLink):
	types = {   1: 'filmography' }
	
###############################################################################

# possible relationships between entities (the most generic types)
Title.links = {
	Title: TitleLinkTitle, 
	Person: TitleLinkPerson, 
	Company: TitleLinkCompany,
}
Person.links = {
	Title: PersonLinkTitle,
}
Company.links = {
	Title: CompanyLinkTitle,
}
Character.links = {
	Title: CharacterLinkTitle,
}

# indicate the most specific top level entities
Title.rootLevelEntityType = Title
Person.rootLevelEntityType = Person
Company.rootLevelEntityType = Company
Character.rootLevelEntityType = Character
	
###############################################################################
## Global dataset configurations ##############################################
###############################################################################

# list of all mayor entities from above
entities = [Title, Person, Company, Character]

# name of the dataset
name = "IMDb"

###############################################################################
## GeneratorThread ############################################################
###############################################################################

from PyQt4 import QtCore
		
def getRootModel(scene):
	for item in scene.items(): # iterates WidgetProxy objects
		try:
			if item.representsRoot():
				return item.widget().model
		except AttributeError:
			pass
		
def getLinkModels(scene):
	links = []
	for widget in scene.items():
		try:
			# widget.myEndItem -> only the links
			# (Proxy -> EntityWidget -> models)
			links.append(widget.myEndItem.widget().elm.linkclass)
		except AttributeError:
			pass
	return links
		
class GeneratorThread(QtCore.QThread):
	"""Thread that will generate the Prolog code.
	Inherits from QThread so it can emit signals for the process bar."""
	
	# progress/total amount are the signal parameters
	progress = QtCore.pyqtSignal(int, int)

	def __init__(self, parent=None):
		super(GeneratorThread, self).__init__(parent)
		self.exiting = False
		
	def run(self):
		# Note: This is never called directly. It is called by Qt once the
		# thread environment has been set up.
		
		# debugging with pydev fails because QThread is C
		# import pydevd;pydevd.settrace()	
		
		rm = getRootModel(self.scene)
		links = getLinkModels(self.scene)
		
		def giveLinkModels(parent_model):
			"""AbstractLink objects for a given entity."""
			result_list = []
			for link_model in links:
				if link_model.getOne() == parent_model:
					result_list.append(link_model)
			return result_list
				
		# write out diagram to file
		def writeDiagram(model, level=0):
			out = ""
			out += "  "*level + ".-" + "-"*len(model.name) + "-.\n"
			out += "  "*level + "| %s |\n" % model.name
			out += "  "*level + "`-" + "-"*len(model.name) + u"-^\n"
			
			# selected entity classes
			out += "  "*level + "Classes:\n"
			for ecm in model.guiClassObjects:
				if ecm.guiChecked:
					out += "  "*level + " - %s\n" % ecm.name
			
			# selected attributes + constraints
			out += "  "*level + "Attributes:\n"
			for attr in model.attributes:
				if attr.guiChecked:
					checked = ": enabled"
				else:
					checked = ""
				out += "  "*level + " - %s%s\n" % (attr.name, checked)
				for constr in attr.constraints:
					out += "  "*level + "    *%s\n" % constr
				
			# links
			lm = giveLinkModels(model)
			if len(lm):
				out += "  "*level + "Links:\n"
			for linkmodel in lm:
				for link, _status in linkmodel.guiChecked.items():
					out += "  "*level + " - %s\n" % link
				parent = linkmodel.getOne()
				assert(parent == model)
				linked = linkmodel.getTwo()
				out += "  "*level + " \\\n"
				out += writeDiagram(linked, level+1)
			return out
		
		with open(self.output_file + ".diagram.txt", "w") as dia:
			dia.write(writeDiagram(rm))
		
		# make Prolog file empty
		with open(self.output_file, "w") as pf:
			pf.write("")

		
		logging.info("Grabbing IDs root entity.")
		offset = 0
		more_sentinel = True
		amount = self.amount
		while amount > 0 and more_sentinel: 
			"""Grabs the right amount of IDs that don't fail 
			the constraints by recursion."""
			# only grab ids: data later
			rm.grabIds(amount, offset, self.random)
			logging.debug(str(rm.toproc_ids))
			if not self.random:
				offset += amount
			
			# prevent infinite run (no new ids found)
			if len(rm.toproc_ids) == 0:
				# self.exiting = True
				# let linked entities finish too
				more_sentinel = False
			
			while len(rm.toproc_ids) and not self.exiting:
				key = rm.toproc_ids.pop()
				logging.info("%d/%d - %d" % (len(rm.good_ids) + 1, 
											self.amount, key))
				
				# adds key to good or bad list, write prolog, grab link ids
				result = rm.process(key, giveLinkModels(rm), self.output_file)
			
				if result: # advance process bar
					self.progress.emit(len(rm.good_ids), self.amount)
		
			amount = self.amount - len(rm.good_ids)
			if self.exiting:
				more_sentinel = False
		
		def doLinkedEntities(parent_model):
			"""Grabs data for the linked entities."""
			for linkmodel in giveLinkModels(parent_model):
				parent = linkmodel.getOne()
				assert(parent == parent_model)
				linked = linkmodel.getTwo()
											
			
				# don't do a person twice because he is a writer and a cast member
				linked.toproc_ids = list(set(linked.toproc_ids))
													
				total = len(linked.toproc_ids)
				print("--------------------------------------------") 
				print("Populating %s, amount: %d" % (linked, total))
				print("--------------------------------------------") 
				print(linked.toproc_ids)
				for i, entity_id in enumerate(linked.toproc_ids):
					# send progress signal
					self.progress.emit(i + 1, total)
					if self.exiting:
						break
					logging.info("%d/%d - %d" % (i+1, total, entity_id))
					
#					# don't add if Title already in other Title list!!
#					if (entity_id not in parent.good_ids and 
#						parent.rootLevelEntityType == linked.rootLevelEntityType or
#						parent.rootLevelEntityType != linked.rootLevelEntityType):
					linked.process(entity_id, giveLinkModels(linked), 
								self.output_file)
				doLinkedEntities(linked)
		doLinkedEntities(rm)
		
		print("Clearing key cache from models.")
		def clearCache(model):
			model.good_ids = []
			model.bad_ids = []
			model.toproc_ids = [] # should be empty here anyway
			model.link_ids = {}
			
			for linkmodel in giveLinkModels(model):
				clearCache(linkmodel.getTwo())
		clearCache(rm)

	def halt(self):
		"""Gracefully stop the generation."""
		self.exiting = True
	
	def generate(self, amount, output_file, scene, random):
		"""Start the generation."""
		self.exiting = False
		self.amount = amount
		self.output_file = output_file
		self.random = random
		self.scene = scene
		self.start()
		
	def __del__(self):
		self.exiting = True
		self.wait()
		super(QtCore.QThread, self).__del__()

###############################################################################
## Some tests #################################################################
###############################################################################

class TestImdbpy(unittest.TestCase):
	def test_database(self):
#		print getImdbpyInstance().getTitlesCount()
#		print getImdbpyInstance().getPersons()
#		print getImdbpyInstance().getCompanies()
#		print getImdbpyInstance().getCharacters()
		pass
		
	def test_show_data(self):
#		character_data = getImdbpyInstance().get_character(4)
#		person_data = getImdbpyInstance().get_person(5)
#		company_data = getImdbpyInstance().get_company(77)
#		
#		pprint.pprint(character_data.data)
#		pprint.pprint(person_data.data)
#		pprint.pprint(company_data.data)
#		pprint.pprint(getImdbpyInstance().get_keyword('stamp-collecting'))
		pass
	
	def test_movie(self):
		t = Title()
		data = getImdbpyInstance().get_movie(40360)
		print t.generatePrologEntity(40360, data)
		
	def test_company(self):
		c = Company()
		data = getImdbpyInstance().get_company(65570)
		print c.generatePrologEntity(65570, data)
	
# when this file is not imported, but ran directly: run test code
if __name__ == '__main__':
	suites = list()
	suites.append(unittest.TestLoader().loadTestsFromTestCase(TestImdbpy))
	alltests = unittest.TestSuite(suites)
	
	unittest.TextTestRunner(verbosity=2).run(alltests)