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

import imdb.parser.sql
from imdb.parser.sql.alchemyadapter import getDBTables, IN
from sqlalchemy import func, INTEGER
from sqlalchemy.sql import select
from sqlalchemy.sql.expression import cast

# hack to make it work without adjusting IMDbPY
oldAccessSystem = imdb.parser.sql.IMDbSqlAccessSystem

class MyIMDbSqlAccessSystem(imdb.parser.sql.IMDbSqlAccessSystem):
	
	def __init__(self, uri, *args, **kwargs):
		oldAccessSystem.__init__(self, uri, *args, **kwargs)
		self.Q = {} # all the db tables used in building queries
		for t in getDBTables(uri):
			self.Q[t._imdbpyName] = t
			
	def addRandom(self, queryString, random=True):
		"""help function for applying randomness to the result"""
		if random and self._connection.dbName == "mysql":
			queryString = queryString.order_by(func.rand())
		elif random: # postgresql, sqlite
			queryString = queryString.order_by(func.random())
		return queryString
	
	# --- grabbing PKs --------------------------------------------------------
	
	def getTitles(self, categories=[1], offset=0, limit=100, 
				random=False, votes=None):
		"""Returns title ids"""
		T = self.Q['Title']
		I = self.Q['MovieInfoIdx']
		#basic = T._ta_select().where(IN(T.q.kindID, categories))
		basic = select([T.q.id]).where(IN(T.q.kindID, categories))
		basic = self.addRandom(basic, random)
		if votes: # let the db check the amount of votes
			# not super fast initially,
			# but huge speedup compared to the program
			basic = basic.where(T.q.id==I.q.movieID). \
						where(I.q.infoTypeID==100). \
						where(cast(I.q.info, INTEGER)>votes)
		result = basic.offset(offset).limit(limit).execute()
#		result = T._ta_select(IN(T.q.kindID, categories)).offset(offset).limit(limit).execute()
		return [r[0] for r in list(result)] # + [616975] 

	def getPersons(self, offset=0, limit=100, random=False):
		P = self.Q['Name']
		basic = select([P.q.id])
		basic = self.addRandom(basic, random)
		result = basic.offset(offset).limit(limit).execute()
		return [r[0] for r in list(result)]
			#CharName
			
	def getCompanies(self, offset=0, limit=100, random=False):
		C = self.Q['CompanyName']
		basic = select([C.q.id])
		basic = self.addRandom(basic, random)
		result = basic.offset(offset).limit(limit).execute()
		return [r[0] for r in list(result)]
	
	def getCharacters(self, offset=0, limit=100, random=False):
		C = self.Q['CharName']
		basic = select([C.q.id])
		basic = self.addRandom(basic, random)
		result = basic.offset(offset).limit(limit).execute()
		return [r[0] for r in list(result)]
	
	# --- grabbing count ------------------------------------------------------
			
	def getTitlesCount(self, categories=[1]):
		"""Returns the amount of possible titles for a given category"""
		T = self.Q['Title']
		#return func.count(T.q.id).scalar()
		return select('*').where(IN(T.q.kindID,
									categories)).alias().count().scalar()
	
	def getCompaniesCount(self):
		pass
	
	def getCompany(self, companyid):
		"""Return a company based on the ID without any further links.
		Used to speed up the generation process."""
		C = self.Q['CompanyName']
		query = select([C.q.id, C.q.name, C.q.countryCode])
		query = query.where(C.q.id == companyid)
		cid, name, country = query.execute().fetchone()
		result = imdb.Company.Company(companyID=cid, 
									  data={"country": country, "name": name,
									  'distributors': [None],
									  'production companies': [None],
									  'special effects companies': [None],
		                              'miscellaneous companies': [None]})
		return result
		
# replace IMDbPY SQL access system with our additions	
imdb.parser.sql.IMDbSqlAccessSystem = MyIMDbSqlAccessSystem

