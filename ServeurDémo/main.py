# -*- coding: utf-8 -*-
import md5
from flask import Flask, request, make_response, Response
import json, os, psycopg2, urlparse
from db import Db
from functools import wraps 
from datetime import datetime
from math import sqrt

######################################
# OBLIGATOIRE SINON ERREUR
import sys
reload(sys)
sys.setdefaultencoding("latin-1")
######################################

app = Flask(__name__)
app.debug = True

##################################################################

map = [
        [
				{"x":"00","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"00","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"00","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"00","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "potion","skin": "0000"}},
				{"x":"02","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"01","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"02","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"02","isObstacle":False,"skin":"020503","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"02","isObstacle":False,"skin":"020301","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "coin","skin": "FF00"}},
                {"x":"17","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"02","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"02","isObstacle":False,"skin":"020201","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"02","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"03","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"03","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"03","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"03","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"03","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"03","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"03","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"03","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"03","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"04","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"04","isObstacle":True,"skin":"010503","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"04","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"04","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"04","isObstacle":True,"skin":"010201","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"04","isObstacle":True,"skin":"05FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"04","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"04","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"04","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"04","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"04","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"04","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"04","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"05","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"05","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"05","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"05","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"05","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"05","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"05","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"05","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"05","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"05","isObstacle":False,"skin":"020203","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"05","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"05","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"05","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"05","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"05","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"05","isObstacle":False,"skin":"020201","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"05","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"05","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"05","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"05","isObstacle":False,"skin":"020203","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"05","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"06","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"06","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "chest","skin": "0101"}},
                {"x":"07","y":"06","isObstacle":True,"skin":"05FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"06","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"06","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"06","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"06","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"06","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"06","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"06","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"07","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"07","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"07","isObstacle":True,"skin":"05FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"07","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"07","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"07","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"07","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"07","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"07","isObstacle":True,"skin":"010200","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"07","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"07","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"07","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"07","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"07","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"07","isObstacle":True,"skin":"010201","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"07","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"07","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"07","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"07","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"07","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"07","isObstacle":False,"skin":"010200","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"08","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"08","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "coin","skin": "FF00"}},
				{"x":"02","y":"08","isObstacle":True,"skin":"05FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"08","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"08","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"08","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"08","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"08","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"08","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"08","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"08","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"08","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"08","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"08","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"08","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"08","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"08","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"08","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"08","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"08","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"08","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"09","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"09","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"09","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"09","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"09","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"09","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"09","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"09","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"09","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"09","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"09","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"09","isObstacle":False,"skin":"020200","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"09","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"09","isObstacle":False,"skin":"020201","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"09","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"09","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"09","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"09","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"09","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"09","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"09","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"10","isObstacle":True,"skin":"010203","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"10","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"10","isObstacle":True,"skin":"010301","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"10","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"10","isObstacle":True,"skin":"010202","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"10","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"10","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"10","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"10","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"10","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"10","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"10","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"11","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "coin","skin": "FF00"}},
                {"x":"10","y":"11","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"11","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"11","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"11","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"11","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"11","isObstacle":False,"skin":"020300","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"11","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"11","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"11","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"11","isObstacle":False,"skin":"020201","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"11","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"12","isObstacle":False,"skin":"010200","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"12","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"12","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"12","isObstacle":False,"skin":"010501","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"12","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"12","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"12","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"12","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"12","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"12","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"12","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"12","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"12","isObstacle":False,"skin":"010203","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"13","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"13","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"13","isObstacle":False,"skin":"020200","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"13","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"13","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"13","isObstacle":False,"skin":"020202","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"13","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"13","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"13","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"13","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "potion","skin": "0000"}},
                {"x":"17","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"13","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"13","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"13","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
				{"x":"00","y":"14","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"01","y":"14","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"02","y":"14","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"03","y":"14","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
				{"x":"04","y":"14","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"14","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"14","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"14","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"14","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"14","isObstacle":False,"skin":"010200","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"14","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"14","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"14","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"14","isObstacle":False,"skin":"020302","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"14","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"14","isObstacle":False,"skin":"010300","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"14","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"14","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"14","isObstacle":False,"skin":"010201","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"14","isObstacle":False,"skin":"020203","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"14","isObstacle":False,"skin":"020101","players": [],"contains": {"kind": "","skin": ""}}
		],
        [
                {"x":"00","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"01","y":"15","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"02","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"03","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "potion","skin": "FF00"}},
                {"x":"04","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"15","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"15","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"15","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"15","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"15","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"15","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"15","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"15","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
        ],
        [
                {"x":"00","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"01","y":"16","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"02","y":"16","isObstacle":False,"skin":"020500","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"03","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"04","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"16","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"16","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"16","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"16","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"16","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"16","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"16","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "potion","skin": "0100"}},
                {"x":"19","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"16","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
        ],
        [
                {"x":"00","y":"17","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"01","y":"17","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"02","y":"17","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"03","y":"17","isObstacle":True,"skin":"010503","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"04","y":"17","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"17","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"17","isObstacle":True,"skin":"010202","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"17","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"17","isObstacle":False,"skin":"020300","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"17","isObstacle":False,"skin":"010202","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"17","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"17","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"17","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"17","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"17","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"17","isObstacle":False,"skin":"010502","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"17","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"17","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"17","isObstacle":False,"skin":"010203","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"17","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"17","isObstacle":False,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}}
        ],
        [
                {"x":"00","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"01","y":"18","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"02","y":"18","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"03","y":"18","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"04","y":"18","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"18","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"18","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"18","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"18","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"18","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "potion","skin": "FF00"}},
                {"x":"14","y":"18","isObstacle":True,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"18","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"18","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
        ],
        [
                {"x":"00","y":"19","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"01","y":"19","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"02","y":"19","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"03","y":"19","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"04","y":"19","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"19","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"19","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"19","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"19","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"19","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"19","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"19","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"19","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"19","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"19","isObstacle":True,"skin":"010203","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"19","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"19","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"19","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"19","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"19","isObstacle":True,"skin":"010101","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"19","isObstacle":True,"skin":"010201","players": [],"contains": {"kind": "","skin": ""}}
        ],
        [
                {"x":"00","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"01","y":"20","isObstacle":False,"skin":"010100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"02","y":"20","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"03","y":"20","isObstacle":True,"skin":"020000","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"04","y":"20","isObstacle":True,"skin":"020000","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"05","y":"20","isObstacle":True,"skin":"020000","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"06","y":"20","isObstacle":False,"skin":"04FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"07","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"08","y":"20","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"09","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"10","y":"20","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"11","y":"20","isObstacle":True,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"12","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"13","y":"20","isObstacle":False,"skin":"020100","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"14","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"15","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"16","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"17","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"18","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"19","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}},
                {"x":"20","y":"20","isObstacle":False,"skin":"03FF00","players": [],"contains": {"kind": "","skin": ""}}
        ]
]

##################################################################

def check_auth(username, password):
	db = Db()
	result = db.select('SELECT COUNT(login_id) AS nb FROM Login '
                       'WHERE login_name=%(Username)s AND login_password=%(Password)s;', {
                           'Username': username,
                           'Password': md5.new(password.encode('utf-8')).hexdigest()
                       })
	db.close()
	return result[0]['nb'] >= 1

def check_auth_admin(username, password):
    db = Db()
    result = db.select('SELECT COUNT(login_id) AS nb FROM Login '
                       'WHERE login_name=%(Username)s AND login_password=%(Password)s AND login_isadmin = True;', {
                           'Username': username,
                           'Password': md5.new(password.encode('utf-8')).hexdigest()
                       })
    db.close()
    return result[0]['nb'] >= 1

def requires_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return Response('Authentification FAIL', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)
    return decorated
	
def requires_auth_admin(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth_admin(auth.username, auth.password):
            return Response('Authentification FAIL', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
        return f(*args, **kwargs)

    return decorated

def currentPlayer(gameId):
  db = Db()
  resTurn = db.select("SELECT count(1) as nb FROM Turn WHERE game_id = %(gameId)s", {
    "gameId": gameId
  })
  resPlayer = db.select("SELECT count(1) as nb FROM Player WHERE game_id = %(gameId)s", {
    "gameId": gameId
  })
  db.close()
  
  if len(resTurn) == 1 and len(resPlayer) == 1 and resPlayer[0]['nb'] > 0:
    return resTurn[0]['nb'] % resPlayer[0]['nb']
  else:
    return 0

def is_admin(username, password):
	db = Db()
	result = db.select('SELECT login_isadmin FROM Login '
						'WHERE login_name=%(Username)s AND login_password=%(Password)s;', {
							'Username': username,
							'Password': md5.new(password.encode('utf-8')).hexdigest()
						})
	db.close()
	return result[0]['login_isadmin']
	
def get_ranking(id):
	db = Db()
	
	result = db.select('SELECT COUNT(player_id) FROM Item '
						'WHERE game_id = %(id)s AND type_item_id = (SELECT type_item_id FROM Type_Item WHERE type_item_name = \'coin\') '
						'GROUP BY player_id '
						'ORDER BY COUNT(player_id)', {
							'id': id
						})
	
	
	ranking = []
	
	rankingcount = True
	for count in result:
		if count['count'] == 0:
			rankingcount = False
		else:
			rankingcount = True
	
	if rankingcount == True:
		for player in result:
			name = db.select('SELECT player_name FROM Player WHERE player_id = %(id)s', {
				'id' : player['player_id']
			})
			if name:
				ranking.append(name[0]['player_name'])
	else:
		result = db.select('SELECT player_name FROM Player WHERE game_id = %(id)s ORDER BY player_id', {
			'id': id
		})
		for player in result:
			ranking.append(player['player_name'])
		
	db.close()
	
	return ranking

def get_posX(username, id):
	db = Db()
	x = db.select('SELECT player_posx FROM Player WHERE player_name = %(username)s AND game_id = %(id)s', {
		'username': username,
		'id': id
	})
	
	db.close()
	
	return x[0]['player_posx']

def get_posY(username, id):
	db = Db()
	y = db.select('SELECT player_posy FROM Player WHERE player_name = %(username)s AND game_id = %(id)s', {
		'username': username,
		'id': id
	})
	
	db.close()
	
	return y[0]['player_posy']
	
def get_fov(username, id):
	db = Db()
	fov = db.select('SELECT player_fov FROM Player WHERE player_name = %(username)s AND game_id = %(id)s', {
		'username': username,
		'id': id
	})
	
	db.close()
	
	return fov[0]['player_fov']
	
def get_coins(username, id):
	db = Db()
	id = db.select('SELECT player_id FROM Player WHERE player_name = %(username)s AND game_id = %(id)s', {
		'username': username,
		'id': id
	})
	
	coins = db.select('SELECT COUNT(item_id) FROM Item WHERE player_id = %(id)s AND type_item_id = (SELECT type_item_id FROM Type_Item WHERE type_item_name = \'coin\')', {
		'id':id[0]['player_id']
	})
	
	db.close()
	
	return coins[0]['count']

def get_potions(username, id):
	db = Db()
	id = db.select('SELECT player_id FROM Player WHERE player_name = %(username)s AND game_id = %(id)s', {
		'username': username,
		'id': id
	})
	
	potions = []
	
	potionsID = db.select('SELECT subtype_item_id FROM Item WHERE player_id = %(id)s AND type_item_id = (SELECT type_item_id FROM Type_Item WHERE type_item_name = \'potion\')', {
		'id':id[0]['player_id']
	})
	
	for potion in potionsID:
		kind = db.select('SELECT subtype_item_name FROM Subtype_Item WHERE subtype_item_id = %(id)s', {
			'id':potion['subtype_item_id']
		})
	
		potions.append({
			"kind":kind['subtype_item_name']
		})
	
	db.close()
	
	return potions
	
def get_activePotion(username, id):
	# en cours
	return
	
def get_map(username, id):
	fov = get_fov(username, id)
	x = get_posX(username, id)
	y = get_posY(username, id)
	
	retour = []
	
	map_json = []
	
	cpt = 0
	
	for i in range(-fov, fov+1):
		ligne = []
		for j in range(-fov, fov+1):
			# Affichage pour Tests
			#print str(map[y+i][x+j]['x']) + "     " + str(map[y+i][x+j]['y'])  + "               " + str(x+j) + "     " + str(y+i)
			if (int(map[y+i][x+j]['x']) == x+j) and (int(map[y+i][x+j]['y']) == y+i):
				ligne.append(map[y+i][x+j])
				cpt += 1
			else:
				cpt += 1
				ligne.append({})
		map_json.append(ligne)
		
	retour.append(sqrt(cpt))
	retour.append(sqrt(cpt))
	retour.append(json.dumps(map_json))
		
	return retour
	
##################################################################

# Route OK
@app.route('/debug/db/reset', methods=['GET'])
def route_dbinit():
  	"""Cette route sert à initialiser (ou nettoyer) la base de données."""
  	db = Db()
  	db.executeFile("database_resetb.sql")
  	db.close()
  	return "Done."
	
#-----------------------------------------------------------------

# Route OK
@app.route('/users_authtest', methods=['GET'])
@requires_auth
def authentification():
	return Response('Authentification OK', 200, {'WWW-Authenticate': 'Basic realm="Credentials valid"'})
	
#-----------------------------------------------------------------

# Route OK
@app.route('/admin', methods=['GET'])
@requires_auth_admin
def authentification_admin():
	return Response('Authentification OK', 200, {'WWW-Authenticate': 'Basic realm="Credentials valid"'})
	
#-----------------------------------------------------------------

# Route OK
@app.route('/users', methods=['GET'])
@requires_auth_admin
def get_user():
	db=Db()
	
	result = db.select('SELECT login_name AS username, login_password AS password FROM Login')
	
	db.close()
	resp = make_response(json.dumps(result),200)
	return resp
	
#-----------------------------------------------------------------

# Route OK
@app.route('/users', methods=['POST'])
def create_user():
	db=Db()
	data = request.get_json()
		
	db.execute('INSERT INTO Login (login_name, login_password, login_isadmin) VALUES (%(username)s , %(password)s, False)',{
		'username' : data['username'],
		'password' : md5.new(data['password'].encode('utf-8')).hexdigest()
	})
	db.close()
	resp = make_response('Compte créé avec succès',200)
	return resp

#-----------------------------------------------------------------

# Route OK
@app.route('/games', methods=['GET'])
@requires_auth
def games_fetchall():
  	db = Db()
	game = db.select('SELECT * FROM Game')
	returned=[]
	for data in game :
		
		playersList = db.select('SELECT player_name AS name, player_posx AS x, player_posy AS y FROM Player WHERE game_id = %(id)s ORDER BY player_id',{
			'id' : data['game_id']
		})
		nbCoin = db.select('SELECT COUNT(*) FROM Item WHERE type_Item_id = (SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s) AND game_id = %(id)s',{
			'name': 'coin',
			'id' : data['game_id']
		})
		nbChest = db.select('SELECT COUNT(*) FROM Item WHERE type_Item_id = (SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s) AND game_id = %(id)s',{
			'name': 'chest',
			'id' : data['game_id']
		})
		nbPotion = db.select('SELECT COUNT(*) FROM Item WHERE type_Item_id = (SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s) AND game_id = %(id)s',{
			'name': 'potion',
			'id' : data['game_id']
		})

		if playersList:
			curPlayer = playersList[currentPlayer(data['game_id'])]['name']
		else:
			curPlayer = ""
		
		result = {'id' : data['game_id'],
			'name' : data['game_name'],
			'width' : data['game_width'],
			'height' : data['game_height'],
			'players' : playersList,
			'maxPlayers' : data['game_max_players'],
			'fovDefault' : data['game_fov_default'],
			'nbItems' : { 'coins' : nbCoin[0]['count'],
					'potions' : nbPotion[0]['count'],
					'chest' : nbChest[0]['count']},
			'timeout' : data['game_time_max'],
			'victoryOn' : {'rule' : data['game_victory_rule'],
					'value' : data['game_victory_value']},
			'status' : data['game_status'] ,			
			'turn' : data['game_turn'],
			'currentPlayer' : curPlayer
			}
		returned.append(result)
	
	db.close()
	resp = make_response(json.dumps(returned), 200)
	resp.mimetype = 'application/json'
	return resp

#-----------------------------------------------------------------

# Route OK
@app.route('/games', methods=['POST'])
@requires_auth_admin
def games_create():
	db=Db()
	data = request.get_json()
	
	new = db.select('''INSERT INTO Game (game_name,game_width,game_height,game_max_players,game_time_max,game_victory_rule, game_victory_value,game_url_file,game_status, game_fov_default) 
			   VALUES (%(name)s,%(width)s,%(height)s,%(max_player)s,%(timeout)s,%(victoryRule)s,%(victoryValue)s,%(file)s,%(status)s, %(fov)s) RETURNING game_id''',{
		   'name' : data['name'],
		   'width' : data['width'],
		   'height' : data['height'],
		   'max_player' : data['maxPlayers'],
		   'timeout' : data['timeout'],
		   'victoryRule' : data['victoryOn']['rule'],
		   'victoryValue' : data['victoryOn']['value'],
		   'file' : '"010101"0111011011011011011010000100100010010110110100',
		   'status': 'OPENED',
		   'fov' : data['fovDefault']
        })
	
	for i in range(0,data['nbItems']['coins']) :
		db.execute('INSERT INTO Item (game_id, type_Item_id) VALUES (%(game_id)s,(SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s))',{
			'game_id' : new[0]['game_id'],
			'name': 'coin'
		})
	for i in range(0,data['nbItems']['chest']) :
		db.execute('INSERT INTO Item (game_id, type_Item_id) VALUES (%(game_id)s,(SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s))',{
			'game_id' : new[0]['game_id'],
			'name': 'chest'
		})
	for i in range(0,data['nbItems']['potions']) :
		db.execute('INSERT INTO Item (game_id, type_Item_id) VALUES (%(game_id)s,(SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s))',{
			'game_id' : new[0]['game_id'],
			'name': 'potion'
		})		
	db.close()
	resp = make_response('OK', 201)
	resp.mimetype = 'application/json'
	return resp

#-----------------------------------------------------------------

# Route OK
@app.route('/games/<int:id>/players', methods=['GET'])
@requires_auth
def get_player_by_game(id):
	db = Db()
	
	result =db.select('SELECT player_id, player_name as player FROM Player WHERE game_id = %(id)s',{
		'id' : id
	})
	db.close()
	resp = make_response(json.dumps(result),200)
	return resp

#-----------------------------------------------------------------

# Route OK
@app.route('/games/<int:id>/players', methods=['POST'])
@requires_auth
def connect_to_game(id):
	db = Db()
	data = request.get_json()

	result = db.select('SELECT COUNT(player_id) FROM Player WHERE game_id = %(id)s', {
		'id': id
	})
	
	result_Game = db.select('SELECT game_max_players, game_status, game_fov_default FROM Game WHERE game_id = %(id)s', {
		'id': id
	})
	
	if result[0]['count'] < result_Game[0]['game_max_players'] and result_Game[0]['game_status'] == 'OPENED' :
		now = datetime.now()
		db.execute('''INSERT INTO Player (player_name, player_fov, game_id, login_id, player_join_game) 
				VALUES (%(pseudo)s, %(fov)s, %(game_id)s, (SELECT login_id FROM Login WHERE login_name = %(username)s), %(date)s)''',{
				'pseudo' : data['username'],
				'fov' : result_Game[0]['game_fov_default'],
				'game_id': id,
				'username' : data['username'],
				'date' : now
		})
	
	result = db.select('SELECT COUNT(player_id) FROM Player WHERE game_id = %(id)s', {
		'id': id
	})
	
	if result[0]['count'] == result_Game[0]['game_max_players']:
		db.execute('UPDATE Game SET game_status = \'ACTIVE\' WHERE game_id = %(id)s', {
			'id': id
		})
	
	db.close()
	resp = make_response(("games/" + str(id)),204)
	return resp

#-----------------------------------------------------------------

@app.route('/games/<int:gameid>', methods=['GET'])
@requires_auth
def games_getone(gameid):
	result = []
	
	ranking = get_ranking(gameid)
	
	db = Db()
	game = db.select('SELECT * FROM Game WHERE game_id = %(gameid)s',{
		"gameid":gameid
	})
		
	for data in game :
		playersList = db.select('SELECT player_name AS name FROM Player WHERE game_id = %(gameid)s',{
			'gameid' : data['game_id']
		})
		nbCoin = db.select('SELECT COUNT(*) FROM Item WHERE type_Item_id = (SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s) AND game_id = %(gameid)s',{
			'name': 'coin',
			'gameid' : data['game_id']
		})
		nbChest = db.select('SELECT COUNT(*) FROM Item WHERE type_Item_id = (SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s) AND game_id = %(gameid)s',{
			'name': 'chest',
			'gameid' : data['game_id']
		})
		nbPotion = db.select('SELECT COUNT(*) FROM Item WHERE type_Item_id = (SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s) AND game_id = %(gameid)s',{
			'name': 'potion',
			'gameid' : data['game_id']
		})
		
		nbCoinLeft = db.select('SELECT COUNT(*) FROM Item WHERE type_Item_id = (SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s) AND game_id = %(gameid)s AND player_id IS NULL',{
			'name': 'coin',
			'gameid' : data['game_id']
		})
		nbPotionLeft = db.select('SELECT COUNT(*) FROM Item WHERE type_Item_id = (SELECT type_Item_id FROM Type_Item WHERE type_Item_name = %(name)s) AND game_id = %(gameid)s AND player_id IS NULL',{
			'name': 'potion',
			'gameid' : data['game_id']
		})
		
		if playersList:
			curPlayer = playersList[currentPlayer(data['game_id'])]['name']
		else:
			curPlayer = ""
			
		players = []	
		for player in playersList:
			players.append(player['name'])

		auth = request.authorization
		if is_admin(auth.username, auth.password):
		
			allPlayers = []
			for player in players:
				allPlayers.append({
					"username": player,
					"x": get_posX(player, gameid),
					"y": get_posY(player, gameid),
					"fov": get_fov(player, gameid),
					"inventory": {
						"coins" : get_coins(player, gameid),
						"potions": get_potions(player, gameid)
					},
					"activePotion": get_activePotion(player, gameid)
				})
		
			result.append({
				'name' : data['game_name'],
				'id' : data['game_id'],
				'width' : data['game_width'],
				'height' : data['game_height'],
				'status' : data['game_status'],
				'turn' : data['game_turn'],
				'currentPlayer' : curPlayer,
				"players": allPlayers,
				'maxPlayers' : data['game_max_players'],
				'timeout' : data['game_time_max'],
				'nbItems' : { 'coins' : nbCoin[0]['count'], 'potions' : nbPotion[0]['count'], 'chest' : nbChest[0]['count']},
				'nbItemsLeft' : { 'coins' : nbCoinLeft[0]['count'], 'potions' : nbPotionLeft[0]['count']},
				'fovDefault' : data['game_fov_default'],
				'victoryOn' : {'rule' : data['game_victory_rule'], 'value' : data['game_victory_value']},
				'ranking' : ranking,
				'mapView' : map
			})
		else:
			player_map = get_map(auth.username, gameid)
			result.append({
				'name' : data['game_name'],	'id' : data['game_id'],
				'width' : player_map[0],	'height' : player_map[1],
				'status' : data['game_status'],
				'turn' : data['game_turn'],	'currentPlayer' : curPlayer,
				'players' : players,	'maxPlayers' : data['game_max_players'],
				'timeout' : data['game_time_max'],
				'nbItems' : { 'coins' : nbCoin[0]['count'], 'potions' : nbPotion[0]['count'], 'chest' : nbChest[0]['count']},
				'nbItemsLeft' : { 'coins' : nbCoinLeft[0]['count'], 'potions' : nbPotionLeft[0]['count']},
				'fovDefault' : data['game_fov_default'],
				'victoryOn' : {'rule' : data['game_victory_rule'], 'value' : data['game_victory_value']},
				'ranking' : ranking,
				'inventory' : { 'coins' : get_coins(auth.username, gameid), 'potions' : get_potions(auth.username, gameid) },
				'activePotion' : get_activePotion(auth.username, gameid),
				'mapView' : player_map[2]
			})	
	db.close()
			
	resp = make_response(json.dumps(result), 200)
	resp.mimetype = 'application/json'
	return resp
  	
#-----------------------------------------------------------------

@app.route('/games/<int:gameid>/moves', methods=['POST'])
@requires_auth
def moves_addone(gameid):
	db = Db()
	data = request.get_json()
	result = db.select('SELECT * FROM Player WHERE player_name = %(username)s', {
		'username': request.authorization.username
	})
	playersList = db.select('SELECT player_name AS name FROM Player WHERE game_id = %(gameid)s',{
		'gameid' : gameid
	})
	
	if playersList:
		curPlayer = playersList[currentPlayer(gameid)]['name']
	else:
		curPlayer = ""

	if result[0]["player_name"] == curPlayer:
		if data["action"] == "move":
			posX = result[0]["player_posx"]
			posY = result[0]["player_posy"]
			db.execute('INSERT INTO Turn (turn_move, player_id, game_id) '
						'VALUES(%(move)s, %(playerId)s, %(gameid)s)', {
				'move': data['value'],
				'playerId': result[0]["player_id"],
				'gameid': gameid
			})
			if data["value"] == "up":
				db.execute('UPDATE Player SET player_posy = player_posy - 1 WHERE player_id = %(playerId)s', {
					'playerId': result[0]["player_id"]				
				})
			elif data["value"] == "down":
				db.execute('UPDATE Player SET player_posy = player_posy + 1 WHERE player_id = %(playerId)s', {
					'playerId': result[0]["player_id"]				
				})
			elif data["value"] == "left":
				db.execute('UPDATE Player SET player_posx = player_posx - 1 WHERE player_id = %(playerId)s', {
					'playerId': result[0]["player_id"]				
				})
			elif data["value"] == "right":
				db.execute('UPDATE Player SET player_posx = player_posx + 1 WHERE player_id = %(playerId)s', {
					'playerId': result[0]["player_id"]				
				})
			db.close()
			return make_response('', 204)
		elif data["action"] == "potion":
			db.close()
			return make_response('NOT IMPLEMENTED', 404)
	else:
		db.close()
		return make_response('NOT YOUR TURN', 403)

#-----------------------------------------------------------------
	
if __name__ == "__main__":
	app.run(host='0.0.0.0')