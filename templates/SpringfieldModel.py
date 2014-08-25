from flask import Flask, render_template, request
#from flask.ext.sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData, Table
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker, Query
import time
from datetime import datetime as dt
import datetime
from time import mktime
from flask.views import View
from flask import jsonify
from clientGraphModel import ClientGraphModel
import urllib
import urllib2
import json
from urlparse import urlparse

information = []
profileArray = []
loginArray = []
referralArray = []
SociallyConnectedArray = []
applicationArray = []
interviewArray = []
hireArray = []
candidateArray = []
jobArray = []
emailArray = []
customerId = None
class SpringfieldModel:
    
    @classmethod
    def get_json(self, link):
        if urlparse(request.url_root).hostname == "127.0.0.1":
            api_location = 'http://localhost:47695'
        else:
            api_location = 'http://springfield-app.careerify.net'
        #api_location = 'http://localhost:47695'
        req = urllib2.Request(api_location+link)    #springfield-app.careerify.net
        response = urllib2.urlopen(req)
        the_page = response.read()
        decoded_string = the_page.decode('utf-8')
        json_data = json.loads(decoded_string)
        return json_data


    @classmethod
    def post_to_database(cls, link, values):  
        if urlparse(request.url_root).hostname == "127.0.0.1":
            api_location = 'http://localhost:47695'
        else:
            api_location = 'https://springfield-app.careerify.net'    
        #api_location = 'http://localhost:47695'                                                                                                                                                                                                                                                                             
        data = urllib.urlencode(values)
        req = urllib2.Request(api_location+link, data)
        response = urllib2.urlopen(req)
        the_page = response.read()
        print(the_page)
        return the_page

    @classmethod
    def get_clients(cls, db):

        result = cls.get_json('/WebApi/Springfield/GetClientsList')
        return result

    @classmethod
    def get_data(cls, start_date, end_date, has_retrieved, db):
        print("POPULATE DASHBOARD")
        start_date = dt.fromtimestamp(int(start_date)).strftime("%Y-%m-%d")
        end_date = dt.fromtimestamp(int(end_date)).strftime("%Y-%m-%d")
        result = cls.get_json('/WebApi/Springfield/PopulateDashboard/'+start_date+'/'+end_date)
        return result


    @classmethod
    def compareSingleClient(cls, client, year):
        print(client)
        result = cls.get_json('/WebApi/Springfield/CompareSingleClient/'+client+'/'+str(year))
        print(result)
        return result
    
    @classmethod
    def singleClientDataFromLaunch(cls, client, weeks, launch_date):
        print(client)
        print(weeks)
        result = cls.get_json('/WebApi/Springfield/SingleClientDataFromLaunch/'+client+'/'+str(weeks)+'/'+str(launch_date))
        print(result)
        return result


    @classmethod
    def multipleClientsDataFromLaunch(cls, client, weeks, launch_date):
        print(client)
        print(weeks)
        result = cls.get_json('/WebApi/Springfield/MultipleClientsDataFromLaunch/'+client+'/'+str(weeks)+'/'+str(launch_date))
        print(result)
        return result

    @classmethod
    def compareMultipleClients(cls, selectedClients, year):
        print(selectedClients)
        result = cls.get_json('/WebApi/Springfield/CompareMultipleClient/'+selectedClients+'/'+str(year))
        return result


    @classmethod
    def SQLrunner(cls, script, clients):
        print("SQLrunner")
        obj = dict(script = script, clients = clients)
        print(obj)
        result = cls.post_to_database('/WebApi/Springfield/SQLRunner', obj)
        return result