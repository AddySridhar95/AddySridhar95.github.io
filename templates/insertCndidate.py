from flask import Flask, render_template, request
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
import urllib
import urllib2
import json
from urlparse import urlparse
class InsertCandidate:
    global profileId
    global allstarcontactsId
    global referralKey
    global referrerFullName



    @classmethod
    def post_to_database(cls, link, values, client):  
        if urlparse(request.url_root).hostname == "127.0.0.1":
            api_location = 'http://localhost:47695'
        #elif client.lower() == 'duff':
        #print("HERE")
        #api_location = 'http://springfield-app.careerify.net'  #http://springfield-test-app.careerify.net
        else:
            api_location = 'https://springfield-app.careerify.net' 
        print(api_location)     
        try:                                                                                                                                                                                                                                                                       
            data = urllib.urlencode(values)
            print(data)
            req = urllib2.Request(api_location+link, data)
            print(api_location+link)
            print(req)
            response = urllib2.urlopen(req)
            print(response)
            the_page = response.read()
            print(the_page)
            return the_page

        except Exception,e:
            print(str(e))

    @classmethod
    def insert_candidate(cls, client, ATSCandidateId, firstName, lastName, email, reqId, referrerEmail, db):
        print(firstName)
        obj = dict(client=client, ATSCandidateId=ATSCandidateId, firstName=firstName, lastName=lastName, email=email, reqId=reqId, referrerEmail=referrerEmail)
        print(obj)
        ans = cls.post_to_database('/WebApi/SpringField/AddCandidateData', obj, client)
        print(ans)
        return ans