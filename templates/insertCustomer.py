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

class InsertCustomer:
    global connectionId

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
    def post_to_database(cls, link, values, client):  
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
    def insert_customer(cls, name, domain, atscompanycode, atsId, isCustomerEnabled, isGamificationEnabled, isInternalMobilityEnabled, logo, avatar, LinkedInAvatar, baseReferralUrl, taleoCompanyCode, taleoUserName, taleoPassword, taleoInstance, taleoSourceIdentifier, taleoEndPoint, TaleoDepartment, TaleoLocation, SyncInterval, hostUri, FTPusername, FTPpassword, isFTP):
        
        obj = dict(name=name, domain=domain, atscompanycode=atscompanycode, atsId=atsId, isCustomerEnabled=isCustomerEnabled, isGamificationEnabled=isGamificationEnabled, isInternalMobilityEnabled=isInternalMobilityEnabled, logo=logo, avatar=avatar, LinkedInAvatar=LinkedInAvatar, baseReferralUrl=baseReferralUrl, taleoCompanyCode=taleoCompanyCode, taleoUserName=taleoUserName, taleoPassword=taleoPassword, taleoInstance=taleoInstance, taleoSourceIdentifier=taleoSourceIdentifier, taleoEndPoint=taleoEndPoint, TaleoDepartment=TaleoDepartment, TaleoLocation=TaleoLocation, SyncInterval=SyncInterval, hostUri=hostUri, FTPusername=FTPusername, FTPpassword=FTPpassword, isFTP=isFTP)
        print(obj)
        ans = cls.post_to_database('/WebApi/SpringField/AddCustomerData', obj, "duff")
        return ans


    @classmethod
    def add_user_profile(cls, client):
        ans = cls.get_json('/WebApi/SpringField/AddUserProfile/'+client)
        print(ans)
        return ans