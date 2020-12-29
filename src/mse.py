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

# Calculates the mean squared error (MSE) for the rating
# Calculates the root mean squared error (RMSE) for the rating

import re
import math

infile = "../outputs/20-50kvote-budget_r.pl"
#infile = "../outputs/5000r-5000votes-USAUK-rating.pl"

numbers = []
sqerrors = []

pl = open(infile, "r")
for line in pl:
	match = re.match("^rating\(t\d+, (?P<rating>.+)\)\..*$", line)
	if match:
		numbers.append(float(match.group("rating")))
pl.close()
		
average = sum(numbers) / len(numbers)
print("Average:"),
print(average)

for number in numbers:
	error = average - number
	sqerrors.append(error * error)
	
mse = sum(sqerrors) / len(sqerrors)
print("MSE:"),
print(mse)
		
print("RMSE:"),
print(math.sqrt(mse))
	
	
	

