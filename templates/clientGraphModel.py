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



class ClientGraphModel:
    #Input: A client   Output: applicationCount, interviewCount and hireCount for that client in a year 
    @classmethod
    def clientData(cls, client, year):
        client = client.replace(" ", "")
        applicationCountArray = []
        hireCountArray = []
        interviewCountArray = []
        client = client.replace(" ", "")
        print("mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net" + '/' + client)
        CustomerDB = create_engine("mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net" + '/' + client)
        CustomerDBConnection = CustomerDB.connect()
        applicationQuery = "SELECT count(Id) as applicationCount FROM SentMessages WHERE ApplicationStatus='Application'"
        interviewQuery = "SELECT count(Id) as interviewCount FROM SentMessages WHERE ApplicationStatus='Interview'"
        hireQuery = "SELECT count(Id) as hireCount FROM SentMessages WHERE ApplicationStatus='Hire'"        
        
        for x in range(1,13):
            applicationQuery = "SELECT count(Id) as applicationCount FROM SentMessages WHERE ApplicationStatus='Application'"
            interviewQuery = "SELECT count(Id) as interviewCount FROM SentMessages WHERE ApplicationStatus='Interview'"
            hireQuery = "SELECT count(Id) as hireCount FROM SentMessages WHERE ApplicationStatus='Hire'"
            if x in (1, 3, 5, 7, 8, 10, 12):
                endDate = 31
            elif x == 2:
                endDate = 28
            else:
                endDate = 30
            if x < 10:
                changeQuery = "AND DateCreated BETWEEN '"+str(year)+"-0"+str(x)+"-01 00:00:00.000' AND '"+str(year)+"-0"+str(x)+"-"+str(endDate)+" 23:59:59.999'"
            else:
                changeQuery = "AND DateCreated BETWEEN '"+str(year)+"-"+str(x)+"-01 00:00:00.000' AND '"+str(year)+"-"+str(x)+"-"+str(endDate)+" 23:59:59.999'"
            applicationQuery+=changeQuery
            interviewQuery+=changeQuery
            hireQuery+=changeQuery
            applicationResult = CustomerDBConnection.execute(applicationQuery)
            for app in applicationResult:
                applicationCount = app['applicationCount']
            applicationCountArray.append(applicationCount)
            interviewResult = CustomerDBConnection.execute(interviewQuery)
            for interview in interviewResult:
                interviewCount = interview['interviewCount']
            interviewCountArray.append(interviewCount)

            hireResult = CustomerDBConnection.execute(hireQuery)
            for hire in hireResult:
                hireCount = hire['hireCount']
            hireCountArray.append(hireCount)
        return dict(client = client, applicationCount = applicationCountArray, interviewCount = interviewCountArray, hireCount = hireCountArray)