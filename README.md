AIMMS ESDL Universal Link
=========================

Requirements to use this translation software from ESDL to AIMMS:
1.	mySQL Database connection
2.	Python software
3.	Pandas, download on https://pandas.pydata.org/
4.	Pymsql, download on https://pypi.org/project/PyMySQL/
5.	Pyesdl, download on https://pypi.org/project/pyESDL/
6.	AIMSS software

The link includes two folders: a Python and a AIMMS folder.

Python
------
Let's start with the python folder. Inside this folder create a ```.env``` file based on the ```.env-template``` file and
change all settings according to your local needs. The ```.env``` file is listed in the ```.gitignore``` file and will not
be committed to this git repository 

Install all dependencies with (possibly inside a virtual environment):
```shell
pip install -r requirements.txt
```

AIMMS
-----
Then, open In de Aimms folder the project ‘TestFileSQLRead’ and then open the Mainproject folder. In this folder you see the ‘TestFileSQLRead.ams’-file. At the top of this file, the last three variables above should also be changed.
The steps to run the aimms code would be:

1.	Run: Uniform ESDL-AIMMS link.py
2.	Run: Uni_prReadInputFromSql
3.	Convert the ESDL parameters to model-specific parameters.
4.	Run: model.
5.	Change ESDL parameters to liking.
6.	Run: Uni_prWriteOutputToSql
7.	Run: Write_TO_ESDL.py

