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

class revInsertCandidate:
    global profileId
    global allstarcontactsId
    global referralKey
    global referrerFullName
    @classmethod
    def get_customers(cls, db):
        if db == "XP":
            dbConn = "mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net/"
        else:
            dbConn = "mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net/"
        #dbConn = "mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net/"
        MasterDB = create_engine(dbConn+'CareerifyMaster') #  mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net/   #mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net
        MasterDBConnection = MasterDB.connect()
        customerResult = MasterDBConnection.execute("SELECT * FROM Customers WHERE IsEnabled = 1")
        customerArray = []
        for customer in customerResult:
            customerArray.append(str(customer['Name']))
        return customerArray


    @classmethod
    def rev_insert_candidate(cls, client, ATSCandidateId, firstName, lastName, email, reqId, referrerEmail, db):
        if db == "XP":
            dbConnection = "mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net"
        else:
            dbConnection = "mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net"
        client = client.lower()

        LocalDB = create_engine(dbConnection+'/'+client) #  mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net/   #mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net
        LocalDBConnection = LocalDB.connect()  


        MasterDB = create_engine(dbConnection+'/CareerifyMaster') 
        MasterDBConnection = MasterDB.connect()
        ATSSettingsIdResult = MasterDBConnection.execute("SELECT ATSSettingId FROM Customers WHERE Name = '"+client+"'")
        ATSSettingId = None
        for x in ATSSettingsIdResult:
            ATSSettingId = x['ATSSettingId']
        ATSidResult = MasterDBConnection.execute("SELECT ATSId FROM ATSSettings WHERE Id = '"+str(ATSSettingId)+"'")
        ATSId = None
        for x in ATSidResult:
            ATSId = x['ATSId']
        #Error message for invalid referrerEmail
        checkReferrerEmailResult = LocalDBConnection.execute("SELECT * FROM Profiles WHERE IsActive = 1 AND Email = '"+referrerEmail+"'")
        checkEmpty = True
        
        for x in checkReferrerEmailResult:
            checkEmpty = False
        if checkEmpty == True:
            return "The referrer email does not exists."

        #Error message for invalid reqId
        checkReqId = LocalDBConnection.execute("SELECT * FROM EmploymentOpportunities WHERE requisitionidstring = '"+reqId+"'")
        checkEmpty = True
        for x in checkReqId:
            checkEmpty = False
        if checkEmpty == True:
            return "The ReqId does not exists."

        profileIdResult = LocalDBConnection.execute("SELECT p.id, p.firstname, p.lastname, l.name 'location', d.name 'department' FROM profiles p LEFT JOIN locations l ON p.locationid = l.id LEFT JOIN departments d ON p.departmentid = d.id where email = '"+referrerEmail+"'")
        profileId = None
        referrerFullName = None
        profileLocation = None
        profileFirstName = None
        profileLastName = None
        for x in profileIdResult:
            profileLocation = x['location']
            profileId = x[0]
            profileFirstName = x[1]
            profileLastName = x[2]
        referrerFullName = profileFirstName + " " + profileLastName
        allstarcontactsIdResult = LocalDBConnection.execute("SELECT id FROM allstarcontacts where firstname  = '"+firstName+"' and lastname = '"+lastName+"' and profileid = '"+profileId+"'")
        allstarcontactsId = None
        for x in allstarcontactsIdResult:
            allstarcontactsId = x[0]  

        if allstarcontactsId == None:
            print("INSERT INTO allstarcontacts VALUES ('"+profileId+"','"+firstName+"','"+lastName+"',getDate(),0,'"+email+"',NULL,9,NULL"+")")
            res = LocalDBConnection.execute("INSERT INTO allstarcontacts VALUES ('"+profileId+"','"+firstName+"','"+lastName+"',getDate(),0,'"+email+"',NULL,9,NULL"+")")
            allstarcontactsIds = LocalDBConnection.execute("SELECT xyz = SCOPE_IDENTITY()")
            for allstarcontact in allstarcontactsIds:
                allstarcontactsId = allstarcontact['xyz']
       

        referralKeyResult = LocalDBConnection.execute("SELECT top 1 referralkey FROM referrals where referrerprofileid = "+"'"+profileId+"'"+" and allstarcontactid ='"+str(allstarcontactsId)+"'")
        referralKey = None

        #if referralKeyResult != None:
        for x in referralKeyResult:
            referralKey = x[0]
            
        if referralKey == None:
            referralKeyResult = LocalDBConnection.execute("SELECT top 1 referralkey FROM referrals where referrerprofileid = "+"'"+profileId+"'"+" and allstarcontactid is null")
        
            for x in referralKeyResult:
                referralKey = x[0]
        
            if referralKey == None:
                return "Sorry, you don't have enough referral keys."
            
            LocalDBConnection.execute("UPDATE referrals set allstarcontactid = '"+str(allstarcontactsId)+"' where referralkey = '"+str(referralKey)+"'")
            print("UPDATE referrals set allstarcontactid = '"+str(allstarcontactsId)+"' where referralkey = '"+str(referralKey)+"'")

        if ATSId == 1 or ATSId == 8:
            LocalDBConnection.execute("INSERT INTO Candidates values ("+str(allstarcontactsId)+",getDate(),0,'"+str(referralKey)+"','"+str(ATSCandidateId)+"')")
            print("INSERT INTO Candidates values ("+str(allstarcontactsId)+",getDate(),0,'"+str(referralKey)+"','"+str(ATSCandidateId)+"')")
            CandidateIds = LocalDBConnection.execute("SELECT xyz = SCOPE_IDENTITY()")
        else:
            LocalDBConnection.execute("INSERT INTO Candidates values ("+str(allstarcontactsId)+",getDate(),'"+str(ATSCandidateId)+"','"+str(referralKey)+"',NULL)")
            print("INSERT INTO Candidates values ("+str(allstarcontactsId)+",getDate(),'"+str(ATSCandidateId)+"','"+str(referralKey)+"',NULL)")
            CandidateIds = LocalDBConnection.execute("SELECT xyz = SCOPE_IDENTITY()")

        for candidate in CandidateIds:
            candidateId = candidate['xyz']

        employmentOpportunityResult = LocalDBConnection.execute("SELECT e.id, l.name 'location', d.name 'department', rs.id 'reward' FROM employmentopportunities e LEFT JOIN rewardsettings rs on e.rewardsettingid = rs.id LEFT JOIN locations l ON e.locationid = l.id LEFT JOIN departments d ON e.departmentid = d.id  where requisitionidstring = '"+str(reqId)+"'")
        employmentOpportunityId = None
        employmentOpportunityReward = None
        employmentOpportunityDepartment = None
        employmentOpportunityLocation = None
        for x in employmentOpportunityResult:
            employmentOpportunityId = x[0]
            employmentOpportunityReward = x['reward']
            employmentOpportunityDepartment = x['department']
            employmentOpportunityLocation = x['location']
        LocalDBConnection.execute("INSERT INTO employmentopportunitycandidates VALUES ('"+firstName+"','"+lastName+"','"+email+"','"+str(employmentOpportunityId)+"',8,null,getDate(),'"+str(candidateId)+"')")
        print("INSERT INTO employmentopportunitycandidates VALUES ('"+firstName+"','"+lastName+"','"+email+"','"+str(employmentOpportunityId)+"',8,null,getDate(),'"+str(candidateId)+"')")
        



        LocalDBConnection.execute("INSERT INTO messagereports VALUES ('"+str(employmentOpportunityId)+"','DirectReferral-Application',getDate(),'"+str(profileId)+"',null,'"+profileLocation+"',null,'DirectReferral')")
        print("INSERT INTO messagereports VALUES ('"+str(employmentOpportunityId)+"','DirectReferral-Application',getDate(),'"+str(profileId)+"',null,'"+profileLocation+"',null,'DirectReferral')")
        



        messageReportIdResult = LocalDBConnection.execute("SELECT xyz = SCOPE_IDENTITY()")
        for x in messageReportIdResult:
            messageReportId = x['xyz']


            
        rewardvaluesResult2 = LocalDBConnection.execute("SELECT amount FROM rewardvalues where rewardsettingid = '"+str(employmentOpportunityReward)+"' and applicationstatusid = 8 and rewardtypeid = 2")
        rewardvalues = None
        for x in rewardvaluesResult2:
            rewardvalues2 = x[0]
        rewardvaluesResult3 = LocalDBConnection.execute("SELECT amount FROM rewardvalues where rewardsettingid = '"+str(employmentOpportunityReward)+"' and applicationstatusid = 8 and rewardtypeid = 3")
        rewardvalues3 = None
        for x in rewardvaluesResult3:
            rewardvalues3 = x[0]
        if db == "XP":
            LocalDBConnection.execute("INSERT INTO sentmessages VALUES (9,'"+referrerFullName+"','"+str(allstarcontactsId)+"','Application','"+str(messageReportId)+"','DirectReferral','"+str(rewardvalues2)+"','"+str(rewardvalues3)+"',getDate(),'"+str(employmentOpportunityDepartment)+"','"+str(employmentOpportunityLocation)+"',getDate(),0,76)")
            print("INSERT INTO sentmessages VALUES (9,'"+referrerFullName+"','"+str(allstarcontactsId)+"','Application','"+str(messageReportId)+"','DirectReferral','"+str(rewardvalues2)+"','"+str(rewardvalues3)+"',getDate(),'"+str(employmentOpportunityDepartment)+"','"+str(employmentOpportunityLocation)+"',getDate(),0,76)")
        else:
            LocalDBConnection.execute("INSERT INTO sentmessages VALUES (9,'"+referrerFullName+"','"+str(allstarcontactsId)+"','Application','"+str(messageReportId)+"','DirectReferral','"+str(rewardvalues2)+"','"+str(rewardvalues3)+"',getDate(),'"+str(employmentOpportunityDepartment)+"','"+str(employmentOpportunityLocation)+"',getDate(),76,0)")
            print("INSERT INTO sentmessages VALUES (9,'"+referrerFullName+"','"+str(allstarcontactsId)+"','Application','"+str(messageReportId)+"','DirectReferral','"+str(rewardvalues2)+"','"+str(rewardvalues3)+"',getDate(),'"+str(employmentOpportunityDepartment)+"','"+str(employmentOpportunityLocation)+"',getDate(),76,0)")
        return "success"