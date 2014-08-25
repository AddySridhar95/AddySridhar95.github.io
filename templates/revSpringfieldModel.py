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



class revSpringfieldModel:
    def __init__(self):
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
    @classmethod
    def get_data(cls, start_date, end_date, has_retrieved, db):
        #If you want yl then you need to do an if condition check here and make dbConnection equal to the yl string for connection.
        if db == "yl":
            dbConnection="mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net"
        else:
            dbConnection = "mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net"
        MasterDB = create_engine(dbConnection+'/CareerifyMaster') #  mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net/   #mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net
        MasterDBConnection = MasterDB.connect()
        #Gets the name of all the clients
        CustomerResults = MasterDBConnection.execute("SELECT * FROM Customers WHERE IsEnabled = 1 ").fetchall()
        
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

        for customer in CustomerResults:
            #Connects to a particular client's database

            MasterDBB = create_engine(dbConnection+'/CareerifyMaster') #  mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net/   #mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net
            MasterDBConnectionn = MasterDBB.connect()
            SyncTimeQuery = "SELECT * FROM ATSSettings WHERE Id="+str(customer['ATSSettingId'])
            SyncTimeResults = MasterDBConnectionn.execute(SyncTimeQuery)
            
            for synctimeresult in SyncTimeResults:
                synctime = synctimeresult['SyncTime']
                synctimeinterval = synctimeresult['SyncInterval']
            

            dbName = customer['Name'].replace(" ", "")
            print(dbName)
            CustomerDB = create_engine(dbConnection + '/' + dbName)

            if dbName == "GoodTechnology":
                dbName = "Good"
            urlClientName = dbName.lower()            
            CustomerDBConnection = CustomerDB.connect()



            #Query to connect to the profiles table to get total number of users
            profileQuery = "SELECT count(Id) as profileCount FROM Profiles WHERE IsActive = 1"

            loginQuery = "SELECT count(distinct(ProfileId)) as loginCount FROM loginactivity,profiles where profileid = profiles.id and profiles.isactive = 1"
            referralQuery = "SELECT count(*) FROM SentMessages WHERE ApplicationStatus IN ('StatusUpdate', 'PrivateMessage', 'CopyUrl', 'MatchMaker')"
            sociallyConnectedQuery = "SELECT count(distinct(profiles.id)) as sociallyConnectedCount from issuedtoken, profiles where issuedtoken.userid = profiles.id and profiles.isactive = 1"
            applicationQuery = "SELECT count(Id) as applicationCount FROM SentMessages WHERE ApplicationStatus='Application'"
            interviewQuery = "SELECT count(Id) as interviewCount FROM SentMessages WHERE ApplicationStatus='Interview'"
            hireQuery = "SELECT count(Id) as hireCount FROM SentMessages WHERE ApplicationStatus='Hire'"
            jobQuery = "SELECT count(*) as jobCount FROM EmploymentOpportunities WHERE IsActive = 1"
            emailQuery = "SELECT count(*) as emailCount FROM SendGridEmailLog WHERE Subject NOT LIKE 'Server Exception'"


            if has_retrieved=="true": #Applying date filters.
                changeQuery = " AND DateCreated BETWEEN '" + dt.fromtimestamp(int(start_date)).strftime("%Y-%m-%d %H:%M:%S") + "' AND'" + dt.fromtimestamp(int(end_date)).strftime("%Y-%m-%d %H:%M:%S") +"'"
                profileQuery+=changeQuery
                loginQuery+=" AND sessionstart BETWEEN '" + dt.fromtimestamp(int(start_date)).strftime("%Y-%m-%d %H:%M:%S") + "' AND'" + dt.fromtimestamp(int(end_date)).strftime("%Y-%m-%d %H:%M:%S") +"'"
                referralQuery+=changeQuery
                sociallyConnectedQuery+=" AND CreatedOn BETWEEN '" + dt.fromtimestamp(int(start_date)).strftime("%Y-%m-%d %H:%M:%S") + "' AND'" + dt.fromtimestamp(int(end_date)).strftime("%Y-%m-%d %H:%M:%S") +"'"
                applicationQuery+=changeQuery
                interviewQuery+=changeQuery
                hireQuery+=changeQuery
                emailQuery+=changeQuery

            ProfileResults = CustomerDBConnection.execute(profileQuery)
            for x in ProfileResults:
                profileCount = x[0]

            #Gets total number of users logged in
            LoginResults = CustomerDBConnection.execute(loginQuery).fetchall()
            for x in LoginResults:
                loginCount = x[0]
            #Gets total numbers of referrals
            print(referralQuery)
            ReferralResults = CustomerDBConnection.execute(referralQuery).fetchall()
            for x in ReferralResults:
                referralCount = x[0]
            #Gets the total number of users socially connected

            SociallyConnectedResults = CustomerDBConnection.execute(sociallyConnectedQuery).fetchall()
            for x in SociallyConnectedResults:
                sociallyConnectedCount = x[0]
            #Gets the total number of applications

            ApplicationsResults = CustomerDBConnection.execute(applicationQuery).fetchall()
            for x in ApplicationsResults:
                applicationCount = x[0]
            #Gets the total number of interviews

            InterviewsResults = CustomerDBConnection.execute(interviewQuery).fetchall()
            for x in InterviewsResults:
                interviewCount = x[0]
            #Gets the total number of hires

            HireResults = CustomerDBConnection.execute(hireQuery).fetchall()
            for x in HireResults:
                hireCount = x[0]
            EmailResults = CustomerDBConnection.execute(emailQuery).fetchall()
            for x in EmailResults:
                emailCount = x[0]

            candidateTempQuery = "SELECT TOP 1 * FROM Candidates"
            CandidateTempResults = CustomerDBConnection.execute(candidateTempQuery).fetchall()
            for x in CandidateTempResults:
                if x['ATSCandidateId'] == 0:
                    candidateQuery = "SELECT count(distinct(ATSCandidateIdString)) FROM Candidates"
                    if has_retrieved=="true":
                        changeQuery = " WHERE DateCreated BETWEEN '" + dt.fromtimestamp(int(start_date)).strftime("%Y-%m-%d %H:%M:%S") + "' AND'" + dt.fromtimestamp(int(end_date)).strftime("%Y-%m-%d %H:%M:%S") +"'"
                        candidateQuery+=changeQuery
                    CandidateResults = CustomerDBConnection.execute(candidateQuery).fetchall()
                    for x in CandidateResults:
                        candidateCount = x[0]
                else:
                    candidateQuery = "SELECT count(distinct(ATSCandidateId)) FROM Candidates"
                    if has_retrieved=="true":
                        changeQuery = " WHERE DateCreated BETWEEN '" + dt.fromtimestamp(int(start_date)).strftime("%Y-%m-%d %H:%M:%S") + "' AND'" + dt.fromtimestamp(int(end_date)).strftime("%Y-%m-%d %H:%M:%S") +"'"
                        candidateQuery+=changeQuery
                    CandidateResults = CustomerDBConnection.execute(candidateQuery).fetchall()
                    for x in CandidateResults:
                        candidateCount = x[0]
                break
            #print(candidateQuery)
            #Gets the total number of jobs
            if has_retrieved=="true":
                changeQuery = " AND DateCreated BETWEEN '" + dt.fromtimestamp(int(start_date)).strftime("%Y-%m-%d %H:%M:%S") + "' AND'" + dt.fromtimestamp(int(end_date)).strftime("%Y-%m-%d %H:%M:%S") +"'"
                jobQuery+=changeQuery
            JobResults = CustomerDBConnection.execute(jobQuery)

            #for job in JobResults:
            #    jobArray.append(job['Id'])
            for x in JobResults:
                print(x[0])
                jobCount = x[0]
            #The variable thats passed to the front-end is a list of dictionaries
            information.append(dict(name=dbName, url='http://'+urlClientName+'.careerify.net/Admin/SyncTaleoService', mainUrl="http://"+urlClientName+".careerify.net", usersCount=profileCount, loginCount=loginCount,
                                referralCount=referralCount, sociallyConnectedCount=sociallyConnectedCount,
                                applicationCount=applicationCount, interviewCount=interviewCount,
                                hireCount=hireCount, candidateCount=candidateCount, jobCount=jobCount, emailCount=emailCount, synctime=synctime, synctimeinterval=synctimeinterval, synctimered=0))
            #Resets variables
            profileArray = []
            loginArray = []
            referralArray = []
            SociallyConnectedArray = []
            applicationArray = []
            interviewArray = []
            hireArray = []
            candidateArray = []
            jobArray = []
        return information

    @classmethod
    def compareMultipleClients(cls, selectedClients, year):
        print(year)
        IndustryArray = []
        CustomerArray = []
        information = []
        Information = []
        MasterDB1 = create_engine("mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net" + '/' + "CareerifyMaster")
        MasterDBConnection1 = MasterDB1.connect()

        MasterDB2 = create_engine("mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net" + '/' + "CareerifyMaster")
        MasterDBConnection2 = MasterDB2.connect()

        MasterDB3 = create_engine("mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net" + '/' + "CareerifyMaster")
        MasterDBConnection3 = MasterDB3.connect()

        temp = []
        IndustryArray = []
        information = []
        #selectedClientas is an array of multiple clients that are to be compared
        for selectedClient in selectedClients:
            applicationCountArray1 = []
            hireCountArray1 = []
            interviewCountArray1 = []
            
            #print(selectedClient)

            #Fetching the id for each client to be compared
            CustomerResult = MasterDBConnection1.execute("SELECT * FROM Customers WHERE Name = '"+selectedClient+"'").fetchall()
            for x in CustomerResult:
                customerId = x['Id']
            #print(customerId)
            
    
            IndustryQuery = "SELECT * FROM IndustryCustomerMappings WHERE CustomerId = '"+str(customerId)+"'";
            IndustryResult = MasterDBConnection2.execute(IndustryQuery).fetchall()

            applicationQuery = "SELECT count(Id) as applicationCount FROM SentMessages WHERE ApplicationStatus='Application'"
            interviewQuery = "SELECT count(Id) as interviewCount FROM SentMessages WHERE ApplicationStatus='Interview'"
            hireQuery = "SELECT count(Id) as hireCount FROM SentMessages WHERE ApplicationStatus='Hire'"


            IndustryQuery = "SELECT * FROM IndustryCustomerMappings WHERE CustomerId = '"+str(customerId)+"'";
            IndustryResult = MasterDBConnection2.execute(IndustryQuery).fetchall()
            for x in IndustryResult:
                IndustryArray.append(x['IndustryId'])        
                              
            print(IndustryArray)
            IndustryArray = list(set(IndustryArray))   #Eliminating duplicates
            print(IndustryArray)


        for industry in IndustryArray:
            IndustryNameResult = MasterDBConnection2.execute("SELECT IndustryName FROM Industry WHERE Id = '"+str(industry)+"'")
            for i in IndustryNameResult:
                industryName = i['IndustryName']
            clientDictionary = dict(industry = industryName, applicationCount = [0,0,0,0,0,0,0,0,0,0,0,0], interviewCount = [0,0,0,0,0,0,0,0,0,0,0,0], hireCount = [0,0,0,0,0,0,0,0,0,0,0,0])
            CustomerPerIndustryResult = MasterDBConnection3.execute("SELECT * FROM IndustryCustomerMappings WHERE IndustryId = '"+str(industry)+"'").fetchall()
            print(CustomerPerIndustryResult)

            for cpi in CustomerPerIndustryResult:
                customerPerIndustryId = cpi['CustomerId']
                customerResult = MasterDBConnection3.execute("SELECT * FROM Customers WHERE Id = '"+str(customerPerIndustryId)+"'").fetchall()
                for cus in customerResult:
                    CustomerArray.append(cus['Name'])
            CustomerArray = list(set(CustomerArray))
            print(CustomerArray)
            #add the selected customer to the customer array
            print(clientDictionary.get('industry'))
            for customer in CustomerArray:
                data = ClientGraphModel.clientData(customer, year)
                clientDictionary = dict(industry = clientDictionary.get('industry'), applicationCount = map(sum, zip(data.get('applicationCount'), clientDictionary.get('applicationCount'))), interviewCount = map(sum, zip(data.get('interviewCount'), clientDictionary.get('interviewCount'))), hireCount = map(sum, zip(data.get('hireCount'), clientDictionary.get('hireCount'))))
            clientDictionary = dict(industry = clientDictionary.get('industry'), applicationCount = [float(x)/float(len(CustomerArray)) for x in clientDictionary.get('applicationCount')], interviewCount = [float(x)/float(len(CustomerArray)) for x in clientDictionary.get('interviewCount')], hireCount = [float(x)/float(len(CustomerArray)) for x in clientDictionary.get('hireCount')])
            CustomerArray = []
            information.append(clientDictionary)  
        for selectedClient in selectedClients:
            data = ClientGraphModel.clientData(selectedClient, 2014)
            information.append(dict(industry = selectedClient, applicationCount = data.get('applicationCount'), interviewCount = data.get('interviewCount'), hireCount = data.get('hireCount')))

        Information.append(information)
        return Information


    @classmethod
    def compareSingleClient(cls, selectedClient, year):
        IndustryArray = []
        CustomerArray = []
        information = []
        Information = []
        MasterDB1 = create_engine("mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net" + '/' + "CareerifyMaster")
        MasterDBConnection1 = MasterDB1.connect()

        MasterDB2 = create_engine("mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net" + '/' + "CareerifyMaster")
        MasterDBConnection2 = MasterDB2.connect()

        MasterDB3 = create_engine("mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net" + '/' + "CareerifyMaster")
        MasterDBConnection3 = MasterDB3.connect()

        CustomerResult = MasterDBConnection1.execute("SELECT * FROM Customers WHERE Name = '"+selectedClient+"'").fetchall()
        for x in CustomerResult:
            customerId = x['Id']
        print(customerId)
        IndustryQuery = "SELECT * FROM IndustryCustomerMappings WHERE CustomerId = '"+str(customerId)+"'";
        IndustryResult = MasterDBConnection2.execute(IndustryQuery).fetchall()
        for x in IndustryResult:
            IndustryArray.append(x['IndustryId'])

        

        for industry in IndustryArray:
            IndustryNameResult = MasterDBConnection2.execute("SELECT IndustryName FROM Industry WHERE Id = '"+str(industry)+"'")
            for i in IndustryNameResult:
                industryName = i['IndustryName']
            clientDictionary = dict(industry = industryName, applicationCount = [0,0,0,0,0,0,0,0,0,0,0,0], interviewCount = [0,0,0,0,0,0,0,0,0,0,0,0], hireCount = [0,0,0,0,0,0,0,0,0,0,0,0])
            CustomerPerIndustryResult = MasterDBConnection3.execute("SELECT * FROM IndustryCustomerMappings WHERE IndustryId = '"+str(industry)+"'").fetchall()
            print(CustomerPerIndustryResult)

            for cpi in CustomerPerIndustryResult:
                customerPerIndustryId = cpi['CustomerId']
                customerResult = MasterDBConnection3.execute("SELECT * FROM Customers WHERE Id = '"+str(customerPerIndustryId)+"'").fetchall()
                for cus in customerResult:
                    CustomerArray.append(cus['Name'])
            CustomerArray = list(set(CustomerArray))
            print(CustomerArray)
            #add the selected customer to the customer array
            print(clientDictionary.get('industry'))
            for customer in CustomerArray:
                data = ClientGraphModel.clientData(customer, year)
                clientDictionary = dict(industry = clientDictionary.get('industry'), applicationCount = map(sum, zip(data.get('applicationCount'), clientDictionary.get('applicationCount'))), interviewCount = map(sum, zip(data.get('interviewCount'), clientDictionary.get('interviewCount'))), hireCount = map(sum, zip(data.get('hireCount'), clientDictionary.get('hireCount'))))
            clientDictionary = dict(industry = clientDictionary.get('industry'), applicationCount = [float(x)/float(len(CustomerArray)) for x in clientDictionary.get('applicationCount')], interviewCount = [float(x)/float(len(CustomerArray)) for x in clientDictionary.get('interviewCount')], hireCount = [float(x)/float(len(CustomerArray)) for x in clientDictionary.get('hireCount')])
            CustomerArray = []
            information.append(clientDictionary)   
        data = ClientGraphModel.clientData(selectedClient, 2014)
        information.append(dict(industry = selectedClient, applicationCount = data.get('applicationCount'), interviewCount = data.get('interviewCount'), hireCount = data.get('hireCount')))
        Information.append(information)
        return Information