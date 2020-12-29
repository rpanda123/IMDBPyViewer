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

from dfw import AbstractConstraintChecker, AbstractAttribute, esc
from datetime import date
import re
import unittest
from imdb.utils import analyze_name

## Constraints ################################################################

class Constraint(object): # enum
	AVAILABILITY, RANGE, VALUES = list(range(3))

class AvailabilityConstraintBase(AbstractConstraintChecker):
	"""Checks whether an attribute is available/unique.
	Based on the lines of generated Prolog."""
	type = Constraint.AVAILABILITY
	
	def __init__(self, unique=False, enabled=False):
		super(AvailabilityConstraintBase, self).__init__(enabled)
		self.unique = unique

	def check(self, attribute, data):
		if not self.enabled:
			return True # constraint succeeds
		try:
			length = len(attribute.generateProlog(007, data).splitlines())
			if self.unique:
				return length == 1 
			else:
				return length >= 1 
		except KeyError:
			# not available
			return False
		
	def __str__(self):
		en = "enabled" if self.enabled else "disabled"
		return "Availability: %s" % en
	
class RangeConstraint(AbstractConstraintChecker):
	type = Constraint.RANGE
	
	def __init__(self, minimum, maximum, enabled=False):
		super(RangeConstraint, self).__init__(enabled)
		self.minimum = minimum
		self.maximum = maximum
		
		self.curMin = minimum
		self.curMax = maximum
		
	def check(self, attribute, data):
		if not self.enabled:
			return True # constraint succeeds
		
		try:
			value = attribute.getValue(data)
		except KeyError:
			# not available, but don't fail as this is for a range
			return True
		except ValueError:
			# not a number, ???? for example; don't fail
			return True
		
		return self.curMin <= value <= self.curMax
	
	def __str__(self):
		en = "enabled" if self.enabled else "disabled"
		if not self.enabled:
			return "Range: %s" % en
		else:
			return "Range: %s -- %d-%d" % (en, self.curMin, self.curMax)
	
class RangeConstraintMultiple(RangeConstraint):
		
	def check(self, attribute, data):
		if not self.enabled:
			return True # constraint succeeds
		
		try:
			values = attribute.getValues(data)
		except KeyError:
			# not available, but don't fail as this is for a range
			return True

		# one number in the range is enough
		for number in values:
			if self.curMin <= number <= self.curMax:
				return True
		return False
			
class ValueConstraint(AbstractConstraintChecker):
	type = Constraint.VALUES

	def __init__(self, values, enabled=False):
		super(ValueConstraint, self).__init__(enabled)
		
		self.values = {}
		
		for v in values:
			self.values[v] = False
		
	def check(self, attribute, data):
		if not self.enabled:
			return True # constraint succeeds
		
		try:
			attrval = attribute.getValues(data)
		except KeyError:
			# not available, but don't fail 
			return True
		
		for key, checked in self.values.items():
			if checked and key in attrval:
				# one is enough to succeed
				return True
		return False
	
	def __str__(self):
		en = "enabled" if self.enabled else "disabled"
		if not self.enabled:
			return "Value: %s" % en
		else:
			chk = []
			for key, checked in self.values.items():
				if checked:
					chk.append(key)
			return "Range: %s -- %s" % (en, ",".join(chk))
	
## Attribute Mix-ins ##########################################################
	
class ImdbAttribute(AbstractAttribute):
	def __init__(self, *args, **kwargs):
		super(ImdbAttribute, self).__init__(*args, **kwargs)
		
		self.constraints.append(AvailabilityConstraintBase())
		
	def generateProlog(self, key, item):
		"""Don't generate anything by default."""
		return ""

class SimpleStringMixIn(AbstractAttribute):
	def generateProlog(self, key, item):
		return "%s(%s%d, '%s').\n" % (self.name, self.entity.key_prefix,
								key, esc(item[self.imdbpykey]))
		
class SimpleIntMixIn(AbstractAttribute):
	def generateProlog(self, key, item):
		try:
			return "%s(%s%d, %d).\n" % (self.name, self.entity.key_prefix,
								key, item[self.imdbpykey])
		except TypeError:
#			print("DEBUG: not an int: %s" % item[self.imdbpykey])
#			# assume list with int value (top 250 rank)
#			print("Length list = %d, good:" % len(item[self.imdbpykey]))
#			print(self.imdbpykey) # top 250 rank
			return "%s(%s%d, %d).\n" % (self.name, self.entity.key_prefix,
								key, int(item[self.imdbpykey][0]))
		
class SimpleFloatMixIn(AbstractAttribute):
	def generateProlog(self, key, item):
		return "%s(%s%d, %.2f).\n" % (self.name, self.entity.key_prefix,
								key, item[self.imdbpykey])
	
class SimpleStringListMixIn(AbstractAttribute):
	def generateProlog(self, key, item):
		result_string = ""
		for element in item[self.imdbpykey]:
			result_string += "%s(%s%d, '%s').\n" % (self.name, 
													self.entity.key_prefix,
													key, esc(element))
		return result_string
	
class SimpleListCount(AbstractAttribute):
	"""Shows the amount of entries in a given list."""
	def generateProlog(self, key, item):
		return "%s(%s%d, %d).\n" % (self.name, self.entity.key_prefix,
								key, len(item[self.imdbpykey]))
	

## Title attributes ###########################################################
		
class TitleKind(SimpleStringMixIn, ImdbAttribute):
	"""The kind of title is one of the following:
	'movie', 
	'tv series', 
	'tv movie', 
	'video movie', 
	'tv mini series', 
	'video game', 
	'episode'
	
	type(t100526, 'movie').
	type(t101028, 'video movie').
	
	The attribute is available for each title."""
	name = "type"
	imdbpykey = "kind"
	
class TitleName(SimpleStringMixIn, ImdbAttribute):
	"""The name this title has.
	The attribute is available for each title.
	
	title_name(t101028, 'Cape and Cowl').
	title_name(t101034, 'Cape Fear')."""
	name = "title_name"
	# one of those: 'title', 'canonical title', 'long imdb title',
	# 'long imdb canonical title', 'smart canonical title',
	# 'smart long imdb canonical title']
	imdbpykey = "title"

class Year(SimpleIntMixIn, ImdbAttribute):
	"""Release year of the title.
	The attribute is available for most titles.
	
	year(t100296, 1976).
	year(t100441, 1968)."""
	name = "year"
	imdbpykey = "year"
	maxYear = 2050
	minYear = 1888
	
	def __init__(self, *args, **kwargs):
		super(Year, self).__init__(*args, **kwargs)
		
		# http://www.imdb.com/title/tt0392728/
		self.constraints.append(RangeConstraint(self.minYear, self.maxYear))
	
	def getValue(self, data):
		return int(data[self.imdbpykey])
		
class SeriesEndYear(ImdbAttribute):
	"""The end year of the series. No end year if still running.
	71507 titles have this value.
	The result is a number.
	
	Some data examples from the db:
	"1965-1966,1969-1970"
	"2004-????"
	"1997"
	"1964-1967"
	
	Nothing if end year is "????".
	"""
	name = "series_years"
	imdbpykey = "series years"
	
	def generateProlog(self, key, item):
		end_year = item[self.imdbpykey][-4:]
		if end_year != "????":
			return "%s(%s%d, %s).\n" % (self.name, self.entity.key_prefix,
										key, item[self.imdbpykey][-4:])
		else:
			return ""
		
	def __init__(self, *args, **kwargs):
		super(SeriesEndYear, self).__init__(*args, **kwargs)
		
		# http://www.imdb.com/title/tt0392728/
		self.constraints.append(RangeConstraint(1888, Year.maxYear))
	
	def getValue(self, data):
		return int(data[self.imdbpykey])
	
#class SeasonCount(ImdbAttribute, SimpleStringMixIn):
#	"""The amount of seasons for these series."""
#	name = "season_count"
#	imdbpykey = "number of seasons"
#	
#class EpisodeCount(ImdbAttribute, SimpleIntMixIn):
#	name = "number_of_episodes"
#	imdbpykey = "series years"
	
class Keywords(SimpleStringListMixIn, ImdbAttribute):
	"""General keywords associated with a title.
	
	keywords(t100441, 'acid-trip').
	keywords(t100441, 'actor-playing-multiple-roles')."""
	name = "keywords"
	imdbpykey = "keywords"

class VotesDistribution(ImdbAttribute): # 99;"votes distribution"
	"""The vote distribution uses a single character to represent 
	the percentage of votes for each ranking.  
	The following characters codes can appear:

	 "." no votes cast
	 "0"  1-9%  of the votes
	 "1" 10-19% of the votes
	 "2" 20-29% of the votes
	 "3" 30-39% of the votes
	 "4" 40-49% of the votes
	 "5" 50-59% of the votes
	 "6" 60-69% of the votes
	 "7" 70-79% of the votes
	 "8" 80-89% of the votes
	 "9" 90-99% of the votes
	 "*" 100%   of the votes
	 
	358612 titles with a vote distribution.
	
	votes_distribution(t100441, '0', '0', '0', '1', '1', '1', '1', '0', '0', '1').
	votes_distribution(t641145, '6', '0', '0', '0', '0', '0', '0', '0', '0', '1').
	"""
	name = "votes_distribution"
	imdbpykey = "votes distribution"
	
	def generateProlog(self, key, item):
		# other way is easier for the uniqueness constraint
#		result = ""
#		for (i, char) in enumerate(item[self.imdbpykey]):
#			result += "%s(%s%d, %d, '%s').\n" % (self.name, 
#					self.entity.key_prefix, key, i+1, char)
#		return result
		result = "%s(%s%d, " % (self.name, self.entity.key_prefix, key)
		for char in item[self.imdbpykey]:
			result += "'%s', " % char
		return result[:-2] + ").\n"
	
class Votes(SimpleIntMixIn, ImdbAttribute): # 100;"votes"
	"""The amount of votes for this title.
	
	Value only available if the title has more than 5 votes.
	358612 titles with a vote amount.
	
	votes(t98638, 8).
	votes(t98941, 122)."""
	name = "votes"
	imdbpykey = "votes"
	
	def __init__(self, *args, **kwargs):
		super(Votes, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(1, 1000000))
	
	def getValue(self, data):
		return int(data[self.imdbpykey])
	
class Rating(SimpleFloatMixIn, ImdbAttribute): # 101;"rating"
	"""The rating this title got from the IMDb users. 
	Movies have been rated on a scale from 1 to 10, 
	10 being good and 1 being bad.
	
	358612 titles with a rating.
	
	rating(t101367, 7.30).
	rating(t101370, 7.50)."""
	name = "rating"
	imdbpykey = "rating"
	
	def __init__(self, *args, **kwargs):
		super(Rating, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(1, 10))
	
	def getValue(self, data):
		return int(data[self.imdbpykey])
	
class Top250Rank(SimpleIntMixIn, ImdbAttribute): # 112;"top 250 rank"
	"""Position in the top 250 list.
	
	TOP 250 MOVIES (3000+ VOTES)
	
	The formula used to calculate the top 250 movies is:
	
	  weighted rank = (v/(v+k))*X + (k/(v+k))*C
	
	  where:

    X = average for the movie (mean)
    v = number of votes for the movie
    k = minimum votes required to be listed in the top 250 (currently 3000)
    C = the mean vote across the whole report (currently 6.90)

	note: for this top 250, only votes from regular voters are considered.
	
	top_250_rank(t10201, 56).
	top_250_rank(t103529, 17).
	"""
	name = "top_250_rank"
	imdbpykey = "top 250 rank"
	
	def __init__(self, *args, **kwargs):
		super(Top250Rank, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(1, 250))
	
	def getValue(self, data):
		return int(data[self.imdbpykey][0])
	
class Bottom10Rank(SimpleIntMixIn, ImdbAttribute): # 113;"bottom 10 rank"
	"""Place of the movie on the bottom 10 list."""
	name = "bottom_10_rank"
	imdbpykey = "bottom 10 rank"
	
	def __init__(self, *args, **kwargs):
		super(Bottom10Rank, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(1, 10))
	
	def getValue(self, data):
		return int(data[self.imdbpykey][0]) # TODO: not sure here
	
class AlternateVersions(SimpleListCount, ImdbAttribute): # '11', 'alternate versions', '16936'
	"""The amount of alternate versions. 16936 entries total.
	An integer.
	
	A list of strings in the db:
	[u'The FOX televised version omits the "There is no spoon" scene...',
     u"In the DVD version that was released in Israel, you don't see ...",...]
     
    alternate_version_amount(t101034, 1).
	alternate_version_amount(t10201, 5).
    """
	name = "alternate_version_amount"
	imdbpykey = "alternate versions"
	
	def __init__(self, *args, **kwargs):
		super(AlternateVersions, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(0, 20))
	
	def getValue(self, data):
		return int(data[self.imdbpykey][0])
	
def parseRuntime(text):	
	country = note = ""
	split = text.split('::')
	if len(split) == 2:
		note = split[1]
	split = split[0].split(':')
	if len(split) == 2:
		country = split[0]
	runtime = split[-1]
	return runtime, country, note

class Runtime(ImdbAttribute): # '1', 'runtimes', '620330'
	"""The runtime of this title in minutes.
	620330 entries in the database.
	
	runtime(t100296, 115, '', '').
	runtime(t100296, 99, 'Spain', '(DVD edition)').
	runtime(t100441, 113, 'Portugal', '')."""
	name = "runtime"
	imdbpykey = "runtimes"
	
	def generateProlog(self, key, item):
		result = ""
		for element in item[self.imdbpykey]:
			runtime, country, note = parseRuntime(element)
			result += "%s(%s%d, %s, '%s', '%s').\n" % (self.name, 
						self.entity.key_prefix, key,
						runtime, esc(country), esc(note))
		return result
	
	def __init__(self, *args, **kwargs):
		super(Runtime, self).__init__(*args, **kwargs)
		
		# https://en.wikipedia.org/wiki/List_of_longest_films_by_running_time
		self.constraints.append(RangeConstraintMultiple(0, 15000))
	
	def getValues(self, data):
		result = []
		for element in data[self.imdbpykey]:
			runtime, _country, _note = parseRuntime(element)
			try:
				result.append(int(runtime))
			except ValueError:
				pass
		return result
		
class ColorInfo(SimpleStringListMixIn, ImdbAttribute): # '2', 'color info', '913715'
	"""The color of the movie. Can have multiple values.
	913715 titles have this info.
	
	There are two possible values:
		"Color";683600
		"Black and White";249669
	
	Sometimes some extra info is added:
		"Color";"";635982
		"Black and White";"";246964
		"Color";"(Technicolor)";12771
		"Color";"(Eastmancolor)";11335
		"Color";"(HD)";3985
		"Color";"(NTSC Color)";3030
		"Color";"(MiniDV)";1809
		"Color";"(Metrocolor)";1332
		"Color";"(Fujicolor)";1151
		"Color";"(HDCAM)";1107
		"Color";"(PAL)";951
		"Color";"(35 mm version)";772
		"Color";"(High Definition)";667
		"Black and White";"(archive footage)";600
		"Color";"(16 mm version)";546
		
	color_info(t481744, blackandwhite, '').
	color_info(t481744, color, '(Eastmancolor)').
	"""
	name = "color_info"
	imdbpykey = "color info"

	def generateProlog(self, key, item):
		result = ""
		for item in item[self.imdbpykey]:
			split = item.split('::')
			if "Black" in split[0]:
				color = "blackandwhite"
			else:
				color = "color"
			extra = ""
			if len(split) >= 2:
				extra = split[1]
			result += "%s(%s%d, %s, '%s').\n" % (self.name, 
								self.entity.key_prefix, key, 
								color, extra)
		return result
		
	values = ['Color', 'Black and White']
	
	def __init__(self, *args, **kwargs):
		super(ColorInfo, self).__init__(*args, **kwargs)
		
		self.constraints.append(ValueConstraint(self.values))
		
	def getValues(self, data):
		return data[self.imdbpykey] # a list
	
# - 7 -- tech info ------------------------------------------------------------

def parseTechInfo(text):
	"""
	"RAT:1.78 : 1 / (high definition)"
	"RAT:1.33 : 1::(16mm)"
	
	also for certificates:
	"UK:15::(re-rating) (2006) (uncut)"
	"""
	i = text.index(':')
	kind = text[:i]
	details = text[i+1:].split('::')
	extra = ""
	if len(details) == 2:
		extra = details[1]
	data = details[0]
	
	# for IMDbPY parser bug
	if not extra and " / (" in data:
		data, extra = data.split(' / ')
	return kind, data, extra

class TechInfoMixIn(ImdbAttribute):
	def generateProlog(self, key, item):
		result = ""
		for element in item[self.imdbpykey]:
			kind, data, extra = parseTechInfo(element)
			if kind == self.kind:
				result += "%s(%s%d, '%s', '%s').\n" % (self.name, 
							self.entity.key_prefix, key,
							esc(data), esc(extra))
		return result
	
class CameraModel(TechInfoMixIn): # '7', 'tech info', '1114008'
	""" CAM   Camera model and Lens information 
	
	camera_model(t239210, 'Panavision Cameras and Lenses', '(segment "Death Proof")').
	camera_model(t239210, 'Panavision Genesis HD Camera', '').
	
	'CAM', '29801' 
	
	1114008 Tech entries in the database.
	(CAM, MET, OFM, PFM, RAT, PCS, LAB)"""
	name = "camera_model"
	imdbpykey = "tech info"
	kind = "CAM"
	
class FilmLength(TechInfoMixIn):
	""" MET   Length of a film in meter 
	
	film_length(t33635, '300 m', '(1 reel)').
	film_length(t103827, '2.978 m', '(Portugal, 35 mm)').
	film_length(t103832, '3597.86 m', '').
	film_length(t143065, '', '(10 reels)').
	film_length(t579828, '3220 m', '(Finland) (1954)').
	
	film_length(t590979, '4150 m', '(Sweden)').
	film_length(t590979, '4230 m', '(Finland)').
	
	'MET', '108500'
	
	Film length is generally measured in feet (in the US) to where 2100 feet 
	of film roughly equals one hour of content."""
	name = "film_length"
	imdbpykey = "tech info"
	kind = "MET"
	
class FilmNegativeFormat(TechInfoMixIn):
	""" OFM   Film negative format in mm or "Video" with an additional
			  attribute for the TV standard 
			  
	film_negative_format(t33635, '35 mm', '').
	film_negative_format(t102248, '35 mm', '(Eastman)').
	film_negative_format(t102812, '16 mm', '').
	film_negative_format(t116406, 'Video', '(PAL)').
	film_negative_format(t117312, 'Video', '(HDTV)').
	film_negative_format(t209047, 'Digital', '').
			  
	'OFM', '249530' """
	name = "film_negative_format"
	imdbpykey = "tech info"
	kind = "OFM"
	
class PrintedFilmFormat(TechInfoMixIn):
	""" PFM   Printed film format in mm or "Video" with an additional
			  attribute for the TV standard 
			  
	printed_film_format(t33635, '35 mm', '').
	printed_film_format(t102812, '35 mm', '(blow-up)').
	printed_film_format(t128032, 'HDTV', '').
			  
	'PFM', '245395' """
	name = "printed_film_format"
	imdbpykey = "tech info"
	kind = "PFM"
	
class AspectRatio(TechInfoMixIn):
	""" RAT   Aspect Ratio, width to height (_.__ : 1) 
	
	aspect_ratio(t10201, '1.37 : 1', '(negative ratio)').
	aspect_ratio(t10201, '1.66 : 1', '(intended ratio)').
	aspect_ratio(t103127, '1.37 : 1', '').
	aspect_ratio(t103127, '1.85 : 1', '(theatrical ratio)').
	
	'RAT', '295984' """
	name = "aspect_ratio"
	imdbpykey = "tech info"
	kind = "RAT"
	
class CinematographicProcess(TechInfoMixIn):
	""" PCS   Cinematographic process or video system 
	
	cinematographic_process(t54904, 'CinemaScope', '').
	cinematographic_process(t10201, 'Spherical', '').
	cinematographic_process(t102248, 'Panavision', '(anamorphic)').
	cinematographic_process(t106227, 'Digital Intermediate', '(2K) (master format)').
	
	'PCS', '148588' """
	name = "cinematographic_process"
	imdbpykey = "tech info"
	kind = "PCS"
	
class Laboratory(TechInfoMixIn):
	""" LAB   Laboratory (Syntax: Laboratory name, Location, Country) 
	
	laboratory(t102812, 'General Labs, California, USA', '').
	laboratory(t103078, 'DeLuxe', '').
	laboratory(t103816, 'Technicolor, USA', '(color)').
	laboratory(t103832, 'Technicolor', '').

	'LAB', '36209' """
	name = "laboratory"
	imdbpykey = "tech info"
	kind = "LAB"
	
# -----------------------------------------------------------------------------
	
class Genres(SimpleStringListMixIn, ImdbAttribute): # '3', 'genres', '1147102'
	"""The genres of this title. A title can have multiple genres.
	
	1147102 genre entries exist.
	All the possible genres: (genre, amount of titles with that genre)
	'Short', '254109'
	'Drama', '186314'
	'Comedy', '142932'
	'Documentary', '119752'
	'Adult', '51607'
	'Romance', '37497'
	'Action', '35860'
	'Animation', '34242'
	'Thriller', '30568'
	'Family', '29525'
	'Crime', '28163'
	'Adventure', '23364'
	'Music', '22741'
	'Horror', '21285'
	'Fantasy', '16636'
	'Mystery', '14599'
	'Sci-Fi', '14033'
	'Western', '12286'
	'Musical', '12135'
	'Biography', '10551'
	'Sport', '10466'
	'War', '9843'
	'History', '9543'
	'Reality-TV', '6266'
	'Talk-Show', '4546'
	'News', '4160'
	'Game-Show', '3592'
	'Film-Noir', '486'
	
	genre(t101034, 'Crime').
	genre(t101034, 'Drama').
	genre(t101034, 'Thriller').
	"""
	name = "genre"
	imdbpykey = "genres"
	values = ['Short', 'Drama', 'Comedy', 'Documentary', 'Adult', 'Romance', 
		'Action', 'Animation', 'Thriller', 'Family', 'Crime', 'Adventure', 
		'Music', 'Horror', 'Fantasy', 'Mystery', 'Sci-Fi', 'Western', 
		'Musical', 'Biography', 'Sport', 'War', 'History', 'Reality-TV', 
		'Talk-Show', 'News', 'Game-Show', 'Film-Noir']
	
	def __init__(self, *args, **kwargs):
		super(Genres, self).__init__(*args, **kwargs)
		
		self.constraints.append(ValueConstraint(self.values))
		
	def getValues(self, data):
		result = []
		for element in data[self.imdbpykey]:
			result.append(element)
		return result
	
class Languages(SimpleStringListMixIn, ImdbAttribute): # '4', 'languages', '912304'
	"""The language(s) used for a title.
	912304 language entries.
	334 different languages.
	
	25 most used languages are shown:
		"English";535688
		"Spanish";57227
		"German";51336
		"French";47034
		"Japanese";31566
		"Italian";26071
		"Portuguese";17769
		"Dutch";10367
		"Russian";9625
		"Hindi";9212
		"Greek";8420
		"Danish";7920
		"Filipino";7059
		"Tagalog";6828
		"Serbo-Croatian";6810
		"Finnish";6656
		"Turkish";6618
		"Mandarin";6225
		"Swedish";5887
		"Czech";5030
		"Cantonese";4957
		"Korean";4908
		"Polish";4609
		"Hungarian";4243
		"Arabic";3737
		
	language(t101370, 'English').
	language(t101370, 'French').
	language(t101370, 'Spanish').
	"""
	name = "language"
	imdbpykey = "languages"
	
	# 25 most used languages
	values = ["English", "Spanish", "German", "French", "Japanese", "Italian", 
		"Portuguese", "Dutch", "Russian", "Hindi", "Greek", "Danish", 
		"Filipino", "Tagalog", "Serbo-Croatian", "Finnish", "Turkish", 
		"Mandarin", "Swedish", "Czech", "Cantonese", "Korean", "Polish", 
		"Hungarian", "Arabic", "Malayalam", "None", "Telugu", "Hebrew", 
		"Norwegian", "Tamil", "Romanian", "Persian", "Bengali", "Bulgarian", 
		"Catalan", "Indonesian", "Georgian", "Albanian", ]
	
	# to get them all:
	#SELECT 
	#  movie_info.info, count(*) as count
	#FROM 
	#  public.movie_info
	#WHERE 
	#  movie_info.info_type_id = 4
	#GROUP BY
	#  movie_info.info
	#ORDER BY
	#  count desc;

	def __init__(self, *args, **kwargs):
		super(Languages, self).__init__(*args, **kwargs)
		
		self.constraints.append(ValueConstraint(self.values))
		
	def getValues(self, data):
		result = []
		for element in data[self.imdbpykey]:
			result.append(element)
		return result
	
class Certificates(ImdbAttribute): # '5', 'certificates', '418839'
	"""The certificates of this title.
	418839 entries in the database.
	
	certificate(t100441, 'Australia', 'M').
	certificate(t100441, 'Finland', 'K-16').
	certificate(t100441, 'Italy', 'VM14').
	certificate(t100441, 'Sweden', '15').
	certificate(t100441, 'UK', '15').
	certificate(t100441, 'UK', 'X').
	certificate(t100441, 'USA', 'R').
	certificate(t100441, 'West Germany', '18').
	
	Format in database:
	u'UK:15::(re-rating) (2006) (uncut)',
	u'Philippines:PG-13',
	u'France:U::(with warning)',
	u'Belgium:KT',"""
	name = "certificate"
	imdbpykey = "certificates"
	
	def generateProlog(self, key, item):
		result = ""
		for element in item[self.imdbpykey]:
			country, cert, _extra = parseTechInfo(element)
			# ignore extra stuff
			result += "%s(%s%d, '%s', '%s').\n" % (self.name, 
							self.entity.key_prefix, key,
							esc(country), esc(cert))
		return result
	
class SoundMix(ImdbAttribute): # '6', 'sound mix', '385541'
	""" 89 records different records, but usually just Mono or Stereo 
	
	sound_mix(id, 'Mono', '(RCA Sound System)').
	sound_mix(id, 'Silent', '').
	sound_mix(id, 'Dolby Digital', '').
	
	385541 entries in the database.
	
	'70 mm 6-Track'
	'Afifa Ton-Kopie'
	'AGA Sound System'
	'Animatophone'
	'Mono::(Western Electric Sound System) (A Victor Recording)'
	'Mono::(Westrex Recording System)'
	"""
	name = "sound_mix"
	imdbpykey = "sound mix"
	
	def generateProlog(self, key, item):
		result = ""
		for element in item[self.imdbpykey]:
			spl = element.split("::")
			sound = spl[0]
			extra = spl[1] if len(spl) >= 2 else ""
			result += "%s(%s%d, '%s', '%s').\n" % (self.name, 
							self.entity.key_prefix, key,
							esc(sound), esc(extra))
		return result
	
class Countries(SimpleStringListMixIn, ImdbAttribute): # '8', 'countries', '964469'
	"""The countries where this title was produced.
	220 different countries.
	
	country(t245377, 'Czech Republic').
	country(t245377, 'France').
	country(t245377, 'Italy').
	country(t245377, 'UK').
	
	964469 countries in the whole database.
	Multiple possible countries for a movie.
	'countries': [u'USA', u'Australia'],
	
	The 50 most encountered countries shown in list:
		"USA";395968
		"UK";90067
		"France";51369
		"Germany";37668
		"Canada";34390
		"Japan";33543
		"Italy";29873
		"India";24930
		"Spain";22178
		"Mexico";19958
		"Australia";18368
		"Argentina";14884
		"West Germany";14680
		"Brazil";11897
		"Denmark";9746
		"Greece";8634
		"Netherlands";8463
		"Belgium";8363
		"Portugal";8302
		"Philippines";7819
		"Finland";7697
		"Soviet Union";7398
		"Hong Kong";7302
		"Sweden";7114
		"Yugoslavia";6898
		"Austria";6499
		"Turkey";6484
		"Hungary";5196
		"Poland";4929
		"South Korea";4863
		"Switzerland";4093
		"Czechoslovakia";3905
		"Russia";3347
		"Nigeria";3257
		"East Germany";3249
		"Israel";2972
		"Norway";2955
		"China";2711
		"Ireland";2697
		"Czech Republic";2652
		"Romania";2161
		"Egypt";2062
		"Taiwan";2038
		"Iran";1912
		"Bulgaria";1838
		"New Zealand";1833
		"Chile";1610
		"Cuba";1555
		"Indonesia";1352
		"Croatia";1248
		"""
	name = "country"
	imdbpykey = "countries"
	
	# 50 most used countries
	values = ["USA", "UK", "France", "Germany", "Canada", "Japan", "Italy", 
		"India", "Spain", "Mexico", "Australia", "Argentina", "West Germany", 
		"Brazil", "Denmark", "Greece", "Netherlands", "Belgium", "Portugal", 
		"Philippines", "Finland", "Soviet Union", "Hong Kong", "Sweden", 
		"Yugoslavia", "Austria", "Turkey", "Hungary", "Poland", "South Korea", 
		"Switzerland", "Czechoslovakia", "Russia", "Nigeria", "East Germany", 
		"Israel", "Norway", "China", "Ireland", "Czech Republic", "Romania", 
		"Egypt", "Taiwan", "Iran", "Bulgaria", "New Zealand", "Chile", "Cuba", 
		"Indonesia", "Croatia", ]
	
	def __init__(self, *args, **kwargs):
		super(Countries, self).__init__(*args, **kwargs)
		
		self.constraints.append(ValueConstraint(self.values))
		
	def getValues(self, data):
		result = []
		for element in data[self.imdbpykey]:
			result.append(element)
		return result

class ReleaseDates(ImdbAttribute): # '16', 'release dates', '2173855'
	"""A title can have multiple release dates.
	
	IMDbPY structure of its result:
	Country:date::optional info -> 'Canada:September 2010' 
	
	Countries with the largest amount of release dates:
	'USA', '763179'
	'UK', '232519'
	'Germany', '106889'
	'France', '98756'
	'Spain', '89275'

	158 countries
	2173855 entries in the database.
	
	release_date(t100441, 'Italy', 1970, february, 4, '(Rome) (premiere)').
	release_date(t100441, 'Italy', 1970, february, 5, '').
	release_date(t100441, 'Japan', 1970, september, 5, '').
	release_date(t10201, 'France', 2001, september, '', '(Deauville Film Festival)').
	
	'USA:1 March 1936',
	'Denmark:17 August 1936',
	'Finland:28 February 1937',
	'Portugal:29 March 1938',
	'USA:27 March 1948::(re-release)'"""
	name = "release_date"
	imdbpykey = "release dates"	

	def generateProlog(self, key, item):
		res = ""
		for date in item[self.imdbpykey]:
			country, date, extra = parseTechInfo(date)
			d = parseDate(date)
			res += "%s(%s%d, '%s', %s, %s, %s, '%s').\n" % (self.name, 
						self.entity.key_prefix, key, 
						esc(country), d.get('year', "''"), 
						d.get('month', "''"), d.get('day', "''"), esc(extra))
		return res
	
	def __init__(self, *args, **kwargs):
		super(ReleaseDates, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraintMultiple(1888, Year.maxYear))
	
	def getValues(self, data):
		result = []
		for element in data[self.imdbpykey]:
			_country, date, _extra = parseTechInfo(element)
			d = parseDate(date)
			try:
				result.append(int(d.get('year', "''")))
			except ValueError:
				pass
		return result
		
#class CrazyCredits(ImdbAttribute): # '12', 'crazy credits', '12703'
#	name = "crazy_credits"
#	imdbpykey = "crazy credits"
#	# yes/no, amount?

#class GoofTypes(ImdbAttribute): # '13', 'goofs', '147573'
#	""" 'CONT', '64449'
#	'FAKE', '22032'
#	'FACT', '15731'
#	'DATE', '9379'
#	'CHAR', '8348'
#	'CREW', '7824'
#	'SYNC', '5056'
#	'GEOG', '4997'
#	'FAIR', '3147'
#	'PLOT', '2883'
#	'MISC', '2133'
#	'BOOM', '1561'
#	'', '33' """
#	name = "goofs"

# soundtrack
	
#class Locations(ImdbAttribute): # '18', 'locations', '518024'
#	"""Countries of the locations same as the countries.
#	
#	'Los Angeles, California, USA', '16953'
#	'New York City, New York, USA', '11978'
#	'Mexico', '9649'
#	'Buenos Aires, Federal District, Argentina', '8164'
#	'London, England, UK', '5117' """
#	name = "locations"
#	imdbpykey = "locations"
		
#class Novel(ImdbAttribute): # '90', 'novel', '17186'
#	""" NOVL: Bibliographical information of the original literary source
#	  (only if published)
#	  -> original novel, theatre play, short story """
#	name = "novel"
#	# yes/no
#		
#class Adaptation(ImdbAttribute): # '91', 'adaption', '2721'
#	""" ADPT: Bibliographical information of the adaption of the literary source
#	  (only if published)
#	  -> adaption of novel, play, short story """
#	name = "adaptation"
#	# yes/no
#		
#class Book(ImdbAttribute): # '92', 'book', '4203'
#	""" BOOK: Monographic book related to this film production """
#	name = "book"
#	# yes/no
		

def parseDateRange(date_range):
	"""Returns amount of days or raises AttributeError."""
	try:
		first, second = date_range.split(' - ')
		f = parseDate(first.split(' (')[0])
		s = parseDate(second.split(' (')[0])
		
		m = ["January", "February", "March", "April", "May", "June", "July", 
			"August", "September", "October", "November", "December"]
		m = [month.lower() for month in m]
		
		a = date(int(f['year']),m.index(f['month']) + 1,int(f.get('day', 1)))
		b = date(int(s['year']),m.index(s['month']) + 1,int(s.get('day', 1)))
		
		return abs((a-b).days)
	except (ValueError, KeyError):
		# ValueError: need more than 1 value to unpack
		# KeyError: 'month'
		raise AttributeError("Date range not possible to parse.")

class ProductionDays(ImdbAttribute): # '102', 'production dates', '14155'
	"""Amount of days the movie was in production.
	14155 entries in the database.
	Many of them aren't usable.
	Will assume first of the month when no day is given.
	See also FilmingDays.
	
	Two dates from when the movie was in production.
	'August 1896 - August 1896'
	'17 March 1897 -'
	'1893 - 1893'
	'? - 21 May 1913'
	"19 September 2010 - 10 January 2011 (EP Films)"
	
	productiondays(t135368, 128).
	productiondays(t135428, 162).
	productiondays(t135492, 122).
	
	It will only work when we have two valid dates."""
	name = "productiondays"
	imdbpykey = "production dates"
	
	def generateProlog(self, key, item):
		amount_days = 0
		try:
			for date_range in item['business'][self.imdbpykey]:
				amount_days += parseDateRange(date_range)
		except AttributeError:
			amount_days = 0
			
		if amount_days:
			return "%s(%s%d, %s).\n" % (self.name, 
										self.entity.key_prefix, key, 
										amount_days)
		else:
			return ""
		
	def __init__(self, *args, **kwargs):
		super(ProductionDays, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(0, 9999))
	
	def getValue(self, data):
		amount_days = 0
		try:
			for date_range in data['business'][self.imdbpykey]:
				amount_days += parseDateRange(date_range)
			return amount_days
		except AttributeError:
			raise KeyError("Same effect as it not being there.")
	
class FilmingDays(ProductionDays): # '104', 'filming dates', '28760'
	"""Amount of days of filming the movie.
	See ProductionDays.
	
	filmingdays(t101034, 118).
	filmingdays(t10201, 182).
	filmingdays(t102248, 120).
	
	28760 entries in the database."""
	name = "filmingdays"
	imdbpykey = "filming dates"
	
def parseBudget(amount):
	"""assumptions: 
	- currency is always before the number
	- no fractions"""
	
	# find index first number
	for i in range(len(amount)):
		if amount[i] in "0123456789":
			amount_idx = i
			break
	
	currency = amount[:amount_idx].strip()
	amount = re.sub("\D", "", amount[amount_idx:])

	return amount, currency
		
class Budget(ImdbAttribute): # '105', 'budget', '80764'
	"""The budget of the movie.
	80764 entries in the database.
	Multiple budgets are possible.
	
	budget(t102248, 30000000, '$').
	budget(t102812, 30000, '$').
	budget(t103003, 6349, '$').

	'AUD 1,000'
	'$1,000'
	'£180'
	'FFR 50,000'"""
	name = "budget"
	imdbpykey = "budget"
	max = 9999999
	
	def generateProlog(self, key, item):
		res = ""
		for budget in item['business'][self.imdbpykey]:
			amount, currency = parseBudget(budget)
			res += "%s(%s%d, %s, '%s').\n" % (self.name, 
											self.entity.key_prefix, key, 
											amount, esc(currency))
		return res
	
	def __init__(self, *args, **kwargs):
		super(Budget, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraintMultiple(0, Budget.max))
	
	def getValues(self, data):
		result = []
		for element in data['business'][self.imdbpykey]:
			amount, _currency = parseBudget(element)
			try:
				result.append(int(amount))
			except ValueError:
				pass
		return result
	
def parseWeekendGross(gross_text):
	g = gross_text.split(' (')
	if not len(g) == 4:
		return ""
	amount, currency = parseBudget(g[0])
	country = g[1].lstrip('(').rstrip(')')
	date = parseDate(g[2].lstrip('(').rstrip(')'))
	day, month, year = date['day'], date['month'], date['year']
	screens = re.sub("\D", "", g[3])
	if not screens:
		screens = "''"
	
	return amount, currency, country, day, month, year, screens

class WeekendGross(ImdbAttribute): # '106', 'weekend gross', '94816'
	"""Gross income of a given weekend.
	94816 entries in the database.
	
	weekend_gross(t625127, 491184, '$', 'USA', 23, december, 2007, 32).
	weekend_gross(t625127, 50926, '$', 'USA', 7, january, 2007, '').
	
	'$1,194 (USA) (13 February 2011) (1 screen)'
	'$66 (USA) (6 February 2011) (1 screen)'
	u'$1,011,566 (USA) (27 June 1999) (1,139 screens)'

	gross
	country
	date opening weekend
	number of screens in opening weekend """
	name = "weekend_gross"
	imdbpykey = "weekend gross"
	
	def generateProlog(self, key, item):
		res = ""
		for gross in item['business'][self.imdbpykey]:
			result = parseWeekendGross(gross)
			if result:
				amount, currency, country, day, month, year, screens = result
				res += "%s(%s%d, %s, '%s', '%s', %s, %s, %s, %s).\n" % (
						self.name, self.entity.key_prefix, key, 
						amount, esc(currency), esc(country), 
						day, month, year, screens)
			else:
				res += ""
		return res
	
	def __init__(self, *args, **kwargs):
		super(WeekendGross, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraintMultiple(0, Budget.max))
	
	def getValues(self, data):
		result = []
		for element in data['business'][self.imdbpykey]:
			parse = parseWeekendGross(element)
			try:
				result.append(int(parse[0])) # amount
			except ValueError:
				pass
		return result
	
class OpeningWeekend(WeekendGross): # '108', 'opening weekend', '15667'
	"""Same as weekend gross, but only for the opening weekends.
	15667 entries in the database.
	
	opening_weekend(t103529, 181494, '$', 'USA', 12, april, 1992, 11).
	opening_weekend(t103529, 34698, '?', 'UK', 9, july, 1992, 1).
	opening_weekend(t103827, 34528, '$', 'USA', 19, december, 2010, 7)."""
	name = "opening_weekend"
	imdbpykey = "opening weekend"
	
def parseGross(gross_text):
	g = gross_text.split(' (')
	d = m = y = "''"
	amount, currency = parseBudget(g[0])
	country = g[1].lstrip('(').rstrip(')')
	if len(g) >= 3:	
		date = parseDate(g[2].lstrip('(').rstrip(')'))
		d = date.get('day', "''") 
		m = date.get('month', "''")
		y = date.get('year', "''")
	
	return amount, currency, country, d, m, y
	
class Gross(ImdbAttribute): # '107', 'gross', '130853'
	"""Gross on a given day up until given date.
	130853 entries in the database.
	
	gross(t101034, 8125975, 'AUD', 'Australia', '', '', 1992).
	gross(t10201, 1010300000, 'ITL', 'Italy', '', '', 1983).
	gross(t10201, 1362322, '?', 'UK', 26, march, 2000).
	gross(t10201, 1675124, '?', 'UK', 2, april, 2000).

	u'$175,400,000 (Worldwide) (15 August 1999) (except USA)',
    u'DEM 50,400,000 (Germany)',
    u'\u20ac 10,695,801 (Spain) (10 March 2003)',
    """
	name = "gross"
	imdbpykey = "gross"
	
	def generateProlog(self, key, item):
		res = ""
		for gross in item['business'][self.imdbpykey]:
			result = parseGross(gross)
			if result:
				amount, currency, country, day, month, year = result
				res += "%s(%s%d, %s, '%s', '%s', %s, %s, %s).\n" % (
						self.name, self.entity.key_prefix, key, 
						amount, esc(currency), esc(country), day, month, year)
			else:
				res += ""
		return res

	def __init__(self, *args, **kwargs):
		super(Gross, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraintMultiple(0, Budget.max))
	
	def getValues(self, data):
		result = []
		for element in data['business'][self.imdbpykey]:
			parse = parseGross(element)
			try:
				result.append(int(parse[0])) # amount
			except ValueError:
				pass
		return result
	
def parseRental(rental_text):
	r = rental_text.split(' (')
	amount, currency = parseBudget(r[0])
	try:
		country = r[1].lstrip('(').rstrip(')')
	except IndexError: # IndexError: list index out of range
		country = ""
	return amount, currency, country
	
class Rentals(ImdbAttribute): # '109', 'rentals', '1819'
	"""1819 entries in the database.
	
	rentals(t170702, 23840000, '$', 'Worldwide').
	rentals(t170702, 6435000, '$', 'USA').
	
	Country not always available.
	'PTE 95,000 (Portugal)'
	'$940,872 (USA)'
	"""
	name = "rentals"
	imdbpykey = "rentals"
	
	def generateProlog(self, key, item):
		res = ""
		for gross in item['business'][self.imdbpykey]:
			amount, currency, country = parseRental(gross)
			res += "%s(%s%d, %s, '%s', '%s').\n" % (
						self.name, self.entity.key_prefix, key, 
						amount, esc(currency), esc(country))
		return res	
	
	def __init__(self, *args, **kwargs):
		super(Rentals, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraintMultiple(0, Budget.max))
	
	def getValues(self, data):
		result = []
		for element in data['business'][self.imdbpykey]:
			parse = parseRental(element)
			try:
				result.append(int(parse[0])) # amount
			except ValueError:
				pass
		return result
		
class Admissions(Gross): # '110', 'admissions', '29140'
	""" The number of tickets that were actually sold at the box office in a 
	specific country as of the specified date. The figure is cumulative, 
	i.e., it represents all tickets that have been sold up to 
	and including that date. 
	
	admissions(t103816, 126427, '', 'Netherlands', 1, january, 1997).
	admissions(t103816, 126540, '', 'Netherlands', 31, december, 1997).
	admissions(t103816, 1364638, '', 'France', 16, april, 1996).
	admissions(t103816, 181323, '', 'Portugal', 18, april, 1996).
	admissions(t103816, 528921, '', 'Germany', 31, december, 1996).
	admissions(t103816, 530204, '', 'Germany', 20, january, 1997).

	'12,172 (Spain)'
	'937,365 (Netherlands) (1950)'
	
	29140 entries in the database."""
	name = "admissions"
	imdbpykey = "admissions"


## Person attributes ##########################################################

class PersonName(SimpleStringMixIn, ImdbAttribute):
	"""The name of the person."""
	name = "person_name"
	imdbpykey = "name"
	
def parseLocation(text):
	return re.match("(?P<location>.*?)(?P<extrainfo> [\[\(].*)?$", text)

def getPart(location, place='country'):
	"""Returns 'country', 'state' or 'city'."""
	places = location.split(', ')
	places = [str(p.group('location')) for p in map(parseLocation, places)]
	
	if place == 'country':
		return places[-1]
	
	# USA states
	list_states = ("Alabama", "Alaska", "Arizona", "Arkansas", "California", 
		"Colorado", "Connecticut", "Delaware", "Florida", "Georgia", "Hawaii", 
		"Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", 
		"Louisiana", "Maine", "Maryland", "Massachusetts", "Michigan", 
		"Minnesota", "Mississippi", "Missouri", "Montana", "Nebraska", 
		"Nevada", "New Hampshire", "New Jersey", "New Mexico", "New York", 
		"North Carolina", "North Dakota", "Ohio", "Oklahoma", "Oregon", 
		"Pennsylvania", "Rhode Island", "South Carolina", "South Dakota", 
		"Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
		"West Virginia", "Wisconsin", "Wyoming")
	
	# Canada provinces and territories
	list_states += ("Alberta", "British Columbia", "Manitoba", "New Brunswick",
		"Newfoundland and Labrador", "Nova Scotia", "Ontario", 
		"Prince Edward Island", "Quebec", "Saskatchewan", 
		"Northwest Territories", "Nunavut", "Yukon")
	
	"""Example SQL to find the irregularities:
	SELECT 
	  person_info.info
	FROM 
	  public.person_info, 
	  public.info_type
	WHERE 
	  person_info.info_type_id = info_type.id AND
	  info_type.id = 20 AND 
	  person_info.info LIKE '%UK%' AND
	  person_info.info NOT LIKE '%Scotland%' AND
	  person_info.info NOT LIKE '%Wales%' AND
	  person_info.info NOT LIKE '%Ireland%' AND
	  person_info.info NOT LIKE '%Northern Ireland%' AND
	  person_info.info NOT LIKE '%Channel Islands%' AND
	  person_info.info NOT LIKE '%Isle of Man%' AND
	  person_info.info NOT LIKE '%England%';"""
	# UK states
	list_states += ("Scotland", "England", "Wales", "Northern Ireland", 
		"Ireland", "Channel Islands", "Isle of Man", 
		"South Wales", "North Wales")
	# Belgian states/provinces
	list_states += ("Flanders", "Wallonia", "Antwerp", "Brussels", "Brussel", 
		"Bruxelles", "Oost-Vlaanderen", "West-Vlaanderen", "Limburg", 
		"Brabant", "Liège", "Luxembourg", "Namur", "Hainaut")
	
	state_countries = ("USA", "Canada", "UK", "Belgium")
	
	# do more countries if wanted/needed? -> guessing code seems solid enough
	
	if len(places) >= 2 and places[-2] in list_states: 
		state = 1
	else:
		state = 0
		
	# try to guess state for those that aren't defined above
	if len(places) >= 3 and places[-1] not in state_countries:
		state = 1
		
	if place == 'state':
		if state:
			return places[-2]
		else:
			return ""
	
	if place == 'city' and len(places) >= 2+state:
			return places[-2-state]
		
	return ""
	
class BirthCountry(ImdbAttribute): # '20', 'birth notes', '299548'
	"""Country of birth. 299548 entries.
	
	country_of_birth(p1003290, 'USA').
	country_of_birth(p1003338, 'UK').
	country_of_birth(p1003416, 'French Protectorate of Morocco').
	
	Data looks like this:
	'Leningrad, USSR [now St. Petersburg, Russia]'
	'British Guiana (now Guyana)'
	'Dearborn, Michigan, USA'
	'Brooklyn, New York City, New York, USA'
	'Aubervilliers, Seine [now Seine-Saint-Denis], France'
	
	Part after the last comma without the comments is used."""
	name = "country_of_birth"
	imdbpykey = "birth notes"
	part = 'country'
	
	def generateProlog(self, key, item):
		raw = item[self.imdbpykey]
#		loc = str(parseLocation(raw).group('location'))
		location = getPart(raw, self.part)
		if location:
			return "%s(%s%d, '%s').\n" % (self.name, 
							self.entity.key_prefix, key, esc(location))
		else:
			return ""
		
class BirthState(BirthCountry): # '20', 'birth notes', '299548'
	"""State/province of birth.
	
	state_of_birth(p1006640, 'British Columbia').
	state_of_birth(p1006666, 'Ontario').
	state_of_birth(p1007023, 'New York').
	"""
	name = "state_of_birth"
	imdbpykey = "birth notes"
	part = 'state'

class BirthCity(BirthCountry): # '20', 'birth notes', '299548'
	"""City of birth.
	
	city_of_birth(p1001156, 'The Bronx').
	city_of_birth(p100116, 'New York City').
	city_of_birth(p1001358, 'Wilmington').
	city_of_birth(p1002308, 'Boston').
	"""
	name = "city_of_birth"
	imdbpykey = "birth notes"
	part = 'city'
	
class DeathCountry(BirthCountry): # '39', 'death notes', '84119'
	"""Country of death. 84119 entries"""
	name = "country_of_death"	
	imdbpykey = "birth notes"
	part = 'country'
	
class DeathState(BirthCountry): # '39', 'death notes', '84119'
	"""State/province of death."""
	name = "state_of_death"	
	imdbpykey = "birth notes"
	part = 'state'
	
class DeathCity(BirthCountry): # '39', 'death notes', '84119'
	"""City of death."""
	name = "city_of_death"	
	imdbpykey = "birth notes"
	part = 'city'
	
class BirthName(SimpleStringMixIn, ImdbAttribute): # '26', 'birth name', '114156'
	"""The name given at birth. 114156 entries."""
	name = "birth_name"
	imdbpykey = "birth name"
	
def parseDate(date):
	result = {}
	
	if re.match(".*\d{4}$", date):
		result['year'] = date[-4:]
		
	m = re.match(".*(?P<month>January|February|March|April|May|June|July|"
				"August|September|October|November|December).*", date, re.I)
	if m:
		result['month'] = m.group('month').lower()
		
		# try to grab date too then
		daymatch = re.match("^(?P<day>\d{1,2}).*", date)
		
		if daymatch:
			result['day'] = daymatch.group('day')		
	return result

class BirthYear(ImdbAttribute): # '21', 'birth date', '324041'
	"""The Birth year of the Person.
	324041 people have a birth date.
	
	birth_year(p1001122, 1922).
	birth_year(p1001156, 1947).
	birth_year(p100116, 1945).
	
	Irregular dates will be ignored:
	"18??"
	"15 June 19??"
	"3 October ????"""
	name = "birth_year"
	imdbpykey = "birth date"
	part = 'year'
	
	def generateProlog(self, key, item):
		date = parseDate(item[self.imdbpykey])
		if date.has_key(self.part):
			return "%s(%s%d, %s).\n" % (self.name, self.entity.key_prefix,
								key, date[self.part])
		else:
			return ""

	def __init__(self, *args, **kwargs):
		super(BirthYear, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(Year.minYear, Year.maxYear))
	
	def getValue(self, data):
		return int(parseDate(data[self.imdbpykey])[self.part])
	
class BirthMonth(BirthYear): # '21', 'birth date', '324041'
	"""The month of birth of the Person. See birth_year.
	
	birth_month(p100116, february).
	birth_month(p1001358, may).
	birth_month(p1002308, december).
	"""
	name = "birth_month"
	imdbpykey = "birth date"
	part = 'month'	
	
class BirthDay(BirthYear): # '21', 'birth date', '324041'
	"""The day of the month of birth of the Person.
	
	birth_day(p100116, 20).
	birth_day(p1001358, 21).
	birth_day(p1002308, 31)"""
	name = "birth_day"
	imdbpykey = "birth date"
	part = 'day'	
	
	def __init__(self, *args, **kwargs):
		super(BirthDay, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(1, 31))

class DeathYear(BirthYear): # '23', 'death date', '96828'
	"""The year of death of the Person. See birth_year.
	96828 people have a death date."""
	name = "death_year"
	imdbpykey = "death date"
	part = 'year'
	
class DeathMonth(BirthYear): # '23', 'death date', '96828'
	"""The month of death of the Person. See death_year."""
	name = "death_month"
	imdbpykey = "death date"
	part = 'month'
	
class DeathDay(BirthDay): # '23', 'death date', '96828'
	"""The day of death of the Person. See death_year."""
	name = "death_day"
	imdbpykey = "death date"
	part = 'day'
	
def parseSpouse(imdbpy_spouse_data):
	result = {}
	parts = imdbpy_spouse_data.split(';')
	if len(parts) == 2:
		# there are children
		m = re.match(" (?P<children>\d{1,2}) .*", parts[1], re.I)
		if m:
			result['children'] = int(m.group('children'))
	first = parts[0]
	
	# the person is in the db too
	result['indb'] = bool(re.match(".*\(qv\).*", first))
	first = first.replace(" (qv)", "")
	
	# check for separation
	r = "divorced|filed for divorce|annulled|separated|his death|her death"
	m = re.match(".*\((?P<reason>%s)\).*" % r, first, re.IGNORECASE)
	if m:
		result['reason'] = m.group('reason')
		
	# get name
	rnum = "(?i)M*(D?C{0,3}|C[DM])(L?X{0,3}|X[LC])(V?I{0,3}|I[VX])"
	m = re.match("^'?(?P<name>.+?)(' | \()(?!%s\)).*" % rnum, first, re.I)
	if m:
		# strip the imdbIndex, can raise IMDbParserError
		result.update(analyze_name(m.group('name')))
		# {'name': 'Susan Isaacs', 'imdbIndex': 'II'}
		assert result.has_key('name')
		# https://resume.imdb.com/help/show_leaf?romannumerals
		if result.has_key('imdbIndex'):
			result['indb'] = True
		
	# do the years if possible, skip the other date stuff
	m = re.match(".*\((?P<start>.+?) - (?P<end>.+?)\).*", first, re.IGNORECASE)
	if m:
		start = parseDate(m.group('start'))
		end = parseDate(m.group('end'))
		if start.has_key('year'):
			result['syear'] = start['year']
		if end.has_key('year'):
			result['eyear'] = end['year']
	
	return result
	
class Spouses(ImdbAttribute): # '24', 'spouse', '104259'
	"""The names of the spouses and whether or not that person has an entry
	in the IMDb database too. 104259 people have spouse info.
	
	spouse(p2081292, 'Jim Simpson', true).
	true: whether or not the person has an IMDb id too
	
	This way in the database:
	"'Susan Isaacs (II)' (qv) (11 August 1968 - present)"
	"'Jennifer Abram' (15 October 1997 - present); 2 children"
	"'Lynn Lempert' (20 January 2001 - 25 December 2010) (his death); 2 children"
	"'Deborah O'Grady' (? - ?); 2 children"
	"'?' (? - ?)"
	"'Loni Ackerman' (qv) (? - ?)"
	"'John Reid (XII)' (qv) (2002 - present)"
	"'?' (? - present); 2 children"
	"'Zélia Afonso' (? - 23 February 1987) (his death); 2 children"
	"'Nicole Kidman' (qv) (24 December 1990 - 8 August 2001) (divorced); 2 (adopted) children"

	Possible options for separation:
	divorced
	filed for divorce
	annulled
	separated
	his death
	her death """
	name = "spouse"
	imdbpykey = "spouse"
	
	def generateProlog(self, key, item):
		spouses = item[self.imdbpykey]
		ret = ""
		for spouse in spouses:
			s = parseSpouse(spouse)
			if s.get('name') and s.get('indb'):
				ret += "%s(%s%d, '%s', %s).\n" % (self.name, 
					self.entity.key_prefix, key, esc(s.get('name')),
					"true" if s.get('indb') else "false")
			else:
				ret += ""
		return ret
	
class Children(ImdbAttribute): # '24', 'spouse', '104259'
	"""The amount of children if the couple has children.
	The zero value (probably) won't be used here.
	
	104259 spouse records exist, but even less with children.
	Range constraint for the amount of children is for the children
	of ALL the spouses together.
	
	children(p100116, 'Louise Bergman', 2).
	children(p1002308, 'Atsuko Remar', 2).
	children(p1003416, 'Genevieve Reno', 2).
	"""
	name = "children"
	imdbpykey = "spouse"
	
	def generateProlog(self, key, item):
		ret = ""
		spouses = item[self.imdbpykey]
		for spouse in spouses:
			s = parseSpouse(spouse)
			if s.get('children') and s.get('name'):
				ret += "%s(%s%d, '%s', %s).\n" % (self.name, 
					self.entity.key_prefix, key, 
					esc(s.get('name')), s.get('children'))
			else:
				ret += ""
		return ret
	
	def __init__(self, *args, **kwargs):
		super(Children, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(0, 99))
	
	def getValue(self, data):
		children = 0
		spouses = data[self.imdbpykey]
		for spouse in spouses:
			s = parseSpouse(spouse)
			if s.get('children'):
				children += int(s.get('children'))
		return children

class FirstMarriageYear(ImdbAttribute): # '24', 'spouse', '104259'
	"""Year of this persons first marriage.
	
	first_marriage_year(p1000776, 1992).
	first_marriage_year(p1001122, 1943).
	first_marriage_year(p1001156, 1989).
	"""
	name = "first_marriage_year"
	imdbpykey = "spouse"

	def generateProlog(self, key, item):
		first_year = 0
		spouses = item[self.imdbpykey]
		for spouse in spouses:
			s = parseSpouse(spouse)
			if (not first_year and s.get('syear')) or (
				s.get('syear', 9999) < first_year):
				first_year = int(s.get('syear'))
		if first_year:
			return "%s(%s%d, %d).\n" % (self.name, 
					self.entity.key_prefix, key, 
					first_year)
		else:
			return ""
		
	def __init__(self, *args, **kwargs):
		super(FirstMarriageYear, self).__init__(*args, **kwargs)
		
		self.constraints.append(RangeConstraint(Year.minYear, Year.maxYear))
	
	def getValue(self, data):
		pl = self.generateProlog(007, data)
		if pl:
			match = re.match(".*, (?P<year>\d+)\).*", pl)
			return int(match.group('year'))
		else:
			raise KeyError("Not possible to find a value.")
			
class LastDivorceYear(FirstMarriageYear): # '24', 'spouse', '104259'
	"""Year of this persons last divorce/separation/death.
	
	last_divorce_year(p1001122, 2008).
	last_divorce_year(p1001156, 1979).
	last_divorce_year(p1003416, 1995)."""
	name = "last_divorce_year"
	imdbpykey = "spouse"
	
	def generateProlog(self, key, item):
		last_year = 0
		spouses = item[self.imdbpykey]
		for spouse in spouses:
			s = parseSpouse(spouse)
			if s.get('eyear', 0) > last_year:
				last_year = int(s.get('eyear'))
		if last_year:
			return "%s(%s%d, %d).\n" % (self.name, 
					self.entity.key_prefix, key, 
					last_year)
		else:
			return ""
	
class Gender(ImdbAttribute):
	"""Sex: male/female
	Only available for each actor/actress.
	
	gender(p1420838, female).
	gender(p142087, male).
	gender(p1420884, female)."""
	name = "gender"
	
	# TODO: gender available in newer IMDbPY version
	def generateProlog(self, key, item):
		gender = ""
		if item.get('actor'):
			gender = "male"
		elif item.get('actress'):
			gender = "female"
			
		if gender:
			return "%s(%s%d, %s).\n" % (self.name, self.entity.key_prefix,
										key, gender)
		else:
			return ""
		
def parseHeight(height):
	cm = 0
	try:
		if "cm" in height:
			height = height.replace(" cm", "")
			try:
				cm = int(height)
			except ValueError: # remove the .5
				cm = int(height[:-2]) + 1 # round to next number
		else:
			h = height.split(' ')
			if len(h) == 1:
				h = height.replace("'", "' ").split(' ')
			feet = int(h[0][:-1]) # remove '
			inches = half = 0
			if len(h) == 2 and h[1] != "":
				inches = int(h[1][:-1]) # remove "
			elif len(h) == 3:
				inches = int(h[1])
				# assume only 1/2 is ever used as third component
				half = 2.54/2
			inches += feet * 12
			cm = int(round(inches * 2.54 + half))
	except ValueError:
		print("Couldn't parse the height: ")
		print(height)
		raise KeyError # as if we didn't have the value
	return cm

class Height(ImdbAttribute): # '22', 'height', '110257'
	"""The height of the person in centimeters.
	110257 people have this attribute.
	The output is a number, excpressed in centimeters.
	
	height(p1006220, 180).
	height(p1006640, 188).
	height(p1007023, 183).
	
	The stored data is like this:
	"6' 0 1/2""
	"5' 2""
	"168 cm"
	"5' 5 1/2""
	"193.5 cm"
	"5'1"
	"6'"
	inches and centimeters are both used."""
	name = "height"
	imdbpykey = "height"
	
	def generateProlog(self, key, item):
		cm = parseHeight(item[self.imdbpykey])
		if cm:
			return "%s(%s%d, %s).\n" % (self.name, self.entity.key_prefix,
										key, cm)
		else:
			return ""
		
#'salary history': [
#u'_Interview with the Vampire: The Vampire Chronicles (1994)_ (qv)::$15,000,000',
#    u'_Eyes Wide Shut (1999)_ (qv)::$20,000,000',
#    u'_Mission: Impossible II (2000)_ (qv)::$20,000,000 + 12% of the gross',
#    u'_Vanilla Sky (2001)_ (qv)::$20,000,000 + 30% of Profits',
#    u'_Jerry Maguire (1996)_ (qv)::$20,000,000 against 15% (USA)',
#    u'_Minority Report (2002)_ (qv)::$25,000,000+',
#    u'_Risky Business (1983)_ (qv)::$75,000',
#    u'_Top Gun (1986)_ (qv)::$2,000,000',
#    u'_Far and Away (1992)_ (qv)::$13,000,000',
#    u'_Rain Man (1988)_ (qv)::$3,000,000+% of gross',
#    u'_Mission: Impossible (1996)_ (qv)::$ 70,000,000 (gross participation)',
#    u'_War of the Worlds (2005)_ (qv)::(20% profit participation)',
#    u'_The Last Samurai (2003)_ (qv)::$25,000,000 + % of profits',
#    u'_Taps (1981)_ (qv)::$50,000',
#    u'_Legend (1985)_ (qv)::$500,000',
#    u'_Cocktail (1988)_ (qv)::$3,000,000',
#    u'_Days of Thunder (1990)_ (qv)::$9,000,000',
#    u'_A Few Good Men (1992)_ (qv)::$12,500,000',
#    u'_The Color of Money (1986)_ (qv)::$1,000,000',
#    u'_The Firm (1993)_ (qv)::$12,000,000',
#    u'_Valkyrie (2008)_ (qv)::$20,000,000 against 20%',
#    u'_Knight and Day (2010)_ (qv)::$11,000,000 + % of profits',
#    u'_Mission: Impossible III (2006)_ (qv)::$75,000,000',
#    u'_Mission: Impossible - Ghost Protocol (2011)_ (qv)::$12,500,000'],

## Company attributes #########################################################

class CompanyCountry(ImdbAttribute):
	"""Saved IMDbPY string looks like '[us]'. The square brackets are
	removed for the output.
	
	company_country(co1, 'us').
	company_country(co10, 'us').
	company_country(co100, 'au').
	company_country(co1000, 'us').
	company_country(co10001, 'gb')."""
	name = "company_country"
	imdbpykey = "country"	

	def generateProlog(self, key, item):
		country = item[self.imdbpykey]
		try:
			country = country.replace("[", "").replace("]", "")
		except AttributeError:
			country = ""
		return "%s(%s%d, '%s').\n" % (self.name, self.entity.key_prefix,
								key, esc(country))

class CompanyName(SimpleStringMixIn, ImdbAttribute):
	"""The name of the company.
	Available for each entity.
	
	company_name(co1, 'E! Entertainment Television').
	company_name(co10, 'National Broadcasting Company (NBC)').
	company_name(co100, 'Nine Network Australia').
	company_name(co1000, 'Passport Video').
	company_name(co10001, 'Ideal')."""
	name = "company_name"
	imdbpykey = "name"


## Character attributes #######################################################

class CharacterName(SimpleStringMixIn, ImdbAttribute):
	"""Name of the character. (Often 'Himself').
	
	character_name(id, 'name')."""
	name = "character_name"
	imdbpykey = "name"
	#  'name': u'Himself'
	
###############################################################################
## Some tests #################################################################
###############################################################################

class TestAttributes(unittest.TestCase):
	def test_birth_country(self):
		p = parseLocation('Leningrad, USSR [now St. Petersburg, Russia]')
		self.assertEqual(p.group('location'), "Leningrad, USSR")
		p = parseLocation('British Guiana (now Guyana)')
		self.assertEqual(p.group('location'), "British Guiana")
		p = parseLocation('Dearborn, Michigan, USA')
		self.assertEqual(p.group('location'), "Dearborn, Michigan, USA")
		
		loc = "Dearborn, Michigan, USA"
		self.assertEqual(getPart(loc, 'country'), "USA")
		self.assertEqual(getPart(loc, 'state'), "Michigan")
		self.assertEqual(getPart(loc, 'city'), "Dearborn")
		loc = "Brooklyn, New York City, New York, USA"
		self.assertEqual(getPart(loc, 'country'), "USA")
		self.assertEqual(getPart(loc, 'state'), "New York")
		self.assertEqual(getPart(loc, 'city'), "New York City")
		loc = "British Guiana"
		self.assertEqual(getPart(loc, 'country'), "British Guiana")
		self.assertEqual(getPart(loc, 'state'), "")
		self.assertEqual(getPart(loc, 'city'), "")
		self.assertEqual(getPart("Brussel, Belgium", 'state'), "Brussel")
		self.assertEqual(getPart("Brussel, Belgium", 'city'), "")
		self.assertEqual(getPart("Brussel, Bruxelles, Belgium", 'city'), "Brussel")
		self.assertEqual(getPart("Belgium", 'country'), "Belgium")
		
		# no states in parser
		loc = "Paris, Ile-de-France, France"
		self.assertEqual(getPart(loc, 'country'), "France")
		self.assertEqual(getPart(loc, 'state'), "Ile-de-France")
		self.assertEqual(getPart(loc, 'city'), "Paris")
		loc = "Thonon-les-Bains, Haute-Savoie, Rhône-Alpes, France"
		self.assertEqual(getPart(loc, 'country'), "France")
		self.assertEqual(getPart(loc, 'state'), "Rhône-Alpes")
		self.assertEqual(getPart(loc, 'city'), "Haute-Savoie")
		loc = "Aubervilliers, Seine [now Seine-Saint-Denis], France"
		self.assertEqual(getPart(loc, 'country'), "France")
		self.assertEqual(getPart(loc, 'state'), "Seine")
		self.assertEqual(getPart(loc, 'city'), "Aubervilliers")
		
	def test_date_parser(self):
		self.assertEqual(parseDate("1999")['year'], "1999")
		self.assertEqual(parseDate("August 1999")['year'], "1999")
		self.assertEqual(parseDate("1 August 1999")['year'], "1999")
		self.assertEqual(parseDate("1 August").has_key('year'), False)
		
		self.assertEqual(parseDate("1 January")['month'], "january")
		self.assertEqual(parseDate("February 1999")['month'], "february")
		self.assertEqual(parseDate("1 March 1999")['month'], "march")
		self.assertEqual(parseDate("1999").has_key('month'), False)
		
		self.assertEqual(parseDate("1 April")['day'], "1")
		self.assertEqual(parseDate("13 May 1999")['day'], "13")
		self.assertEqual(parseDate("June 1999").has_key('day'), False)
		self.assertEqual(parseDate("June 1999").has_key('day'), False)
		
	def test_spouse_parser(self):
		a = "'Jennifer Abram' (15 October 1997 - present); 2 children"
		b = "'Susan Isaacs (II)' (qv) (11 August 1968 - present)"
		c = "'Deborah O'Grady' (? - ?); 2 children"
		d = "'Ray Danton' (qv) (20 February 1955 - 13 April 1978) (divorced); 2 children"
		e = "'Nicole Kidman' (qv) (24 December 1990 - 8 August 2001) (divorced); 2 (adopted) children"
		f = "Jim Simpson (I) (1 October 1984 - present); 1 child"
		self.assertEqual(parseSpouse(a)['children'], 2)
		self.assertEqual(parseSpouse(c)['children'], 2)
		self.assertEqual(parseSpouse(d)['children'], 2)
		self.assertEqual(parseSpouse(e)['children'], 2)
		self.assertEqual(parseSpouse(a)['indb'], False)
		self.assertEqual(parseSpouse(b)['indb'], True)
		self.assertEqual(parseSpouse(d)['indb'], True)
		self.assertEqual(parseSpouse(d)['reason'], "divorced")
		self.assertEqual(parseSpouse(a).has_key('reason'), False)
		self.assertEqual(parseSpouse(a)['name'], "Jennifer Abram")
		self.assertEqual(parseSpouse(b)['name'], "Susan Isaacs")
		self.assertEqual(parseSpouse(b)['imdbIndex'], "II")
		self.assertEqual(parseSpouse(c)['name'], "Deborah O'Grady")
		self.assertEqual(parseSpouse(d)['name'], "Ray Danton")
		
		self.assertEqual(parseSpouse(a)['syear'], "1997")
		self.assertEqual(parseSpouse(a).has_key('eyear'), False)
		self.assertEqual(parseSpouse(d)['syear'], "1955")
		self.assertEqual(parseSpouse(d)['eyear'], "1978")
		
		# without quotes around the name
		self.assertEqual(parseSpouse(f)['children'], 1)
		self.assertEqual(parseSpouse(f)['indb'], True)
		self.assertEqual(parseSpouse(f)['syear'], "1984")
		self.assertEqual(parseSpouse(f)['name'], "Jim Simpson")
		self.assertEqual(parseSpouse(f)['imdbIndex'], "I")
		
	def test_parse_height(self):
		a = '''5' 5 1/2"'''
		b = '''5' 2"'''
		c = "168 cm"
		d = "193.5 cm"
		e = '''5'1"'''
		f = "6'"
		self.assertEqual(parseHeight(a), 166)
		self.assertEqual(parseHeight(b), 157)
		self.assertEqual(parseHeight(c), 168)
		self.assertEqual(parseHeight(d), 194)
		self.assertEqual(parseHeight(e), 155)
		self.assertEqual(parseHeight(f), 183)
		
	def test_parse_runtime(self):
		a = "45::(149 episodes)"
		b = "USA:19::(DVD version)"
		c = "99"
		d = "Argentina:7"
		self.assertEqual(parseRuntime(a), ('45', '', '(149 episodes)'))
		self.assertEqual(parseRuntime(b), ('19', 'USA', '(DVD version)'))
		self.assertEqual(parseRuntime(c), ('99', '', ''))
		self.assertEqual(parseRuntime(d), ('7', 'Argentina', ''))
		
	def test_parse_tech_info(self): # and certificate, release dates
		a = "OFM:35 mm"
		b = "RAT:1.33 : 1::(16mm)"
		c = "UK:15::(re-rating) (2006) (uncut)"
		d = 'USA:27 March 1948::(re-release)'
		self.assertEqual(parseTechInfo(a), ('OFM', '35 mm', ''))
		self.assertEqual(parseTechInfo(b), ('RAT', '1.33 : 1', '(16mm)'))
		self.assertEqual(parseTechInfo(c), ('UK', '15', '(re-rating) (2006) (uncut)'))
		self.assertEqual(parseTechInfo(d), ('USA', '27 March 1948', '(re-release)'))
		
	def test_parse_budget(self):
		a = 'AUD 1,000'
		b = '$1,000'
		c = '£180'
		d = 'FFR 50,000'
		self.assertEqual(parseBudget(a), ('1000', 'AUD'))
		self.assertEqual(parseBudget(b), ('1000', '$'))
		self.assertEqual(parseBudget(c), ('180', '£'))
		self.assertEqual(parseBudget(d), ('50000', 'FFR'))
		
	def test_parse_weekend_gross(self):
		g = "$1,011,566 (USA) (27 June 1999) (1,139 screens)"
		self.assertEqual(parseWeekendGross(g), 
			('1011566', '$', 'USA', '27', 'june', '1999', '1139'))
	
	def test_parse_gross(self):
		g = '$175,400,000 (Worldwide) (15 August 1999) (except USA)'
		self.assertEqual(parseGross(g), 
			('175400000', '$', 'Worldwide', '15', 'august', '1999'))
		# admissions (the same, but with irregularities)
		a = '937,365 (Netherlands) (1950)'
		self.assertEqual(parseGross(a), 
			('937365', '', 'Netherlands', "''", "''", '1950'))
		a = '12,172 (Spain)'
		self.assertEqual(parseGross(a), 
			('12172', '', 'Spain', "''", "''", "''"))
		
	def test_parse_rental(self):
		r = 'PTE 95,000 (Portugal)'
		s= '$ 95.000'
		self.assertEqual(parseRental(r), ('95000', 'PTE', 'Portugal'))
		self.assertEqual(parseRental(s), ('95000', '$', ''))
		
	def test_parse_date_range(self):
		a = "19 September 2010 - 10 January 2011"
		b = "19 September 2010 - 10 January 2011 (EP Films)"
		c = "September 2010 - January 2011"
		d = "1893 - 1893"
		self.assertEqual(parseDateRange(a), 113)
		self.assertEqual(parseDateRange(b), 113)
		self.assertEqual(parseDateRange(c), 122)
		self.assertRaises(AttributeError, parseDateRange, d)
		
# when this file is not imported, but ran directly: run test code
if __name__ == '__main__':
	suites = list()
	suites.append(unittest.TestLoader().loadTestsFromTestCase(TestAttributes))
	alltests = unittest.TestSuite(suites)
	
	unittest.TextTestRunner(verbosity=2).run(alltests)

"""
SELECT info_type.info, movie_info.info_type_id, count(movie_info.info_type_id) as amount
FROM movie_info, info_type
WHERE movie_info.info_type_id = info_type.id
GROUP BY movie_info.info_type_id, info_type.info
ORDER BY amount DESC
LIMIT 1000 OFFSET 0;
 
"release dates";16;2208821
"genres";3;1164767
"tech info";7;1142249
"countries";8;984849
"color info";2;933272
"languages";4;933041
"runtimes";1;630287
"locations";18;525259
"quotes";15;505825
"certificates";5;421886
"sound mix";6;389647
"soundtrack";14;331107
"trivia";17;287618
"plot";98;242900
"goofs";13;148908
"gross";107;131771
"taglines";9;114860
"weekend gross";106;95535
"budget";105;82482
"printed media reviews";94;57357
"copyright holder";103;46082
"filming dates";104;29337
"admissions";110;29198
"novel";90;17281
"alternate versions";11;16995
"opening weekend";108;15853
"production dates";102;14283
"crazy credits";12;12838
"mpaa";97;12273
"other literature";96;8034
"LD number";85;6598
"LD laserdisc title";88;6598
"LD disc size";75;6597
"LD video standard";81;6597
"LD category";65;6597
"LD color information";61;6593
"LD year";41;6591
"LD group genre";62;6590
"LD disc format";40;6575
"LD official retail price";43;6574
"LD production country";51;6572
"LD quality program";63;6569
"LD analog right";71;6568
"LD language";47;6564
"LD subtitles";77;6556
"LD sound encoding";84;6555
"LD status of availablility";78;6545
"LD analog left";66;6517
"LD master format";76;6503
"LD digital sound";42;6488
"LD picture format";54;6459
"LD close captions-teletext-ld-g";64;6416
"LD number of sides";80;6415
"LD label";86;6401
"LD aspect ratio";70;6328
"LD certification";67;6251
"LD catalog number";87;6139
"LD length";46;6122
"LD release country";57;6012
"LD release date";50;5560
"essays";95;4442
"book";92;4261
"interviews";35;3672
"adaption";91;2751
"screenplay-teleplay";89;2528
"LD additional information";72;2512
"rentals";109;1821
"production process protocol";93;1581
"LD number of chapter stops";73;1427
"LD pressing plant";45;1415
"LD supplement";82;468
"LD review";48;15

SELECT info_type.info, movie_info_idx.info_type_id, count(movie_info_idx.info_type_id) as amount
FROM movie_info_idx, info_type
WHERE movie_info_idx.info_type_id = info_type.id
GROUP BY movie_info_idx.info_type_id, info_type.info
ORDER BY amount DESC
LIMIT 1000 OFFSET 0;
 
"votes";100;358612
"votes distribution";99;358612
"rating";101;358612
"top 250 rank";112;250
"bottom 10 rank";113;10

"""