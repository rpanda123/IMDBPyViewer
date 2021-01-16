# IMDBPyViewer
A program written in Python to generate relational datasets in Prolog format. It uses data from the Internet Movie Database in combination with IMDbPY as backend. A graphical user interface written in pyQt allows the user to link multiple entities together as model for the generation process. The big four entities are Title, Person, Company and Character. Many attributes can be chosen for adding to the output .pl file. Three types of constraints on attributes are available to limit the output: an availability constraint, a range constraint and a value constraint. It works with both MySQL and PostgreSQL as database backend.

![Sample Image](https://github.com/rpanda123/IMDBPyViewer/blob/main/IMDBPYsampleImage.png)

Install:
--------

1)PyQt4
2)SQLAlchemy
3)IMDbPY

Run imdbpy2sql.py to populate the database.
Grab the plain text data files from http://www.imdb.com/interfaces

Start the program:
python main.py

Caveats:
--------

-Votes: requirement constraint and range constraint will speed up the process
 Only titles with the correct amount of votes are tried.
 
-all companies selected in upper box + no further links to other entities
 will speed up the companies generation
 (no IMDbPY is used because it grabs links and this can take a while)
 
-Miniseries do not exist in the database

For developers:
---------------

QtDesigner enables you to edit the .ui files.
