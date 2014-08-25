# from flask import Flask, render_template, request
# from sqlalchemy import create_engine, MetaData, Table
# from sqlalchemy import Column, Integer, String
# from sqlalchemy.orm import relationship, backref
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import scoped_session, sessionmaker, Query
# import time
# from datetime import datetime as dt
# import datetime
# from time import mktime
# from flask.views import View
# from flask import jsonify

# class revInsertCustomer:
#     global connectionId
#     @classmethod
#     def rev_insert_customer(cls, name, domain, atscompanycode, atsId, isCustomerEnabled, isGamificationEnabled, isInternalMobilityEnabled, logo, avatar, LinkedInAvatar, baseReferralUrl, taleoCompanyCode, taleoUserName, taleoPassword, taleoInstance, taleoSourceIdentifier, taleoEndPoint, TaleoDepartment, TaleoLocation, SyncInterval, hostUri, FTPusername, FTPpassword, isFTP):
#         dbConnection = "mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net"
#         MasterDB = create_engine(dbConnection+'/CareerifyMaster') #  mssql+pyodbc://CareerifySQLAdmin:110311AllStars@yl5q7ll4kn.database.windows.net/   #mssql+pyodbc://CareerifySQLAdmin:+9y+h10ux#?@g48,,5r@xpl12qsdzu.database.windows.net
#         MasterDBConnection = MasterDB.connect()  

#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#         MasterDBConnection.execute("INSERT INTO ConnectionSettings VALUES( NULL, 'xpl12qsdzu.database.windows.net', " + "'"+name+"'"+", 'CareerifySQLAdmin@xpl12qsdzu', '+9y+h10ux#?@g48,,5r')" )
#         connId = MasterDBConnection.execute("SELECT xyz = SCOPE_IDENTITY()")
#         for conn in connId:
#             connectionId = conn['xyz']         
#         #print("INSERT INTO TaleoSettings VALUES("+ "'"+taleoCompanyCode+"',"+"'"+taleoUserName+"',""'"+taleoPassword+"',""'"+taleoInstance+"',""'"+'1900-01-01 01:00:00.000'+"',"+ "'"+baseReferralUrl+"',"+ "'"+taleoSourceIdentifier+"',"+ "'"+taleoEndPoint+"',"+ '0'+")")
        
#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#         MasterDBConnection.execute("INSERT INTO TaleoSettings VALUES("+ "'"+taleoCompanyCode+"',"+"'"+taleoUserName+"',""'"+taleoPassword+"',""'"+taleoInstance+"',""'"+'1900-01-01 01:00:00.000'+"',"+ "'"+baseReferralUrl+"',"+ "'"+TaleoDepartment+"',"+ "'"+TaleoLocation+"','"+ "0"+"'"+")")
#         taleoSettingsId = MasterDBConnection.execute("SELECT taleoid = SCOPE_IDENTITY()")
#         for taleo in taleoSettingsId:
#             taleoSettingId = taleo['taleoid']

#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        
#         MasterDBConnection.execute("INSERT INTO EmailSettings VALUES("+ "'"+"0"+"','"+name+"',"+"'"+"http://"+domain+".careerify.net"+"',""'"+logo+"',"+"'"+"info@careerify.net"+"','"+"smtp.sendgrid.net"+"',""'"+'587'+"',"+ "'"+"careerify"+"',"+ "'"+"e438Ds902h,nbdfVeytrTrB"+"',"+ "'"+"0"+"','"+ "info@careerify.net"+"',"+"'"+"1"+"',"+"'3','1000'"+")")
#         EmailSettingsId = MasterDBConnection.execute("SELECT emailid = SCOPE_IDENTITY()")
#         for email in EmailSettingsId:
#             EmailSettingId = email['emailid']

#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#         if isFTP == 1:
#             MasterDBConnection.execute("INSERT INTO FTPSettings VALUES("+ "'"+hostUri+"','22',"+"'"+name+"',"+"'"+FTPpassword+"',"+"'1',"+"NULL"+",NULL,NULL,'"+"/','/','0')")
#             FTPSettingsId = MasterDBConnection.execute("SELECT ftpid = SCOPE_IDENTITY()")
#             for ftp in FTPSettingsId:
#                 FTPSettingId = ftp['ftpid']
        
#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#         MasterDBConnection.execute("INSERT INTO ATSSettings VALUES("+ "'"+atscompanycode+"','"+taleoUserName+"',"+"'"+taleoPassword+"',"+"'"+taleoEndPoint+"',"+"'"+taleoInstance+"','1900-01-01 01:00:00.000','"+baseReferralUrl+"',"+"'"+TaleoDepartment+"','"+TaleoLocation+"','0',"+ "'"+atsId+"',"+ "'0','"+"0"+"','"+ taleoSourceIdentifier+"',"+"'1900-01-01 01:00:00.000','"+SyncInterval+"')")
#         ATSSettingsId = MasterDBConnection.execute("SELECT atsid = SCOPE_IDENTITY()")
#         for ats in ATSSettingsId:
#             ATSSettingId = ats['atsid']
        
#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#         MasterDBConnection.execute("INSERT INTO CustomerSettings VALUES("+"'"+isGamificationEnabled+"','"+isInternalMobilityEnabled+"')")

#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

#         CustomerSettingsId = MasterDBConnection.execute("SELECT customersettingsid = SCOPE_IDENTITY()")
#         for customersetting in CustomerSettingsId:
#             CustomerSettingId = customersetting['customersettingsid']
#         if isFTP == 1:
#             MasterDBConnection.execute("INSERT INTO Customers VALUES("+"'"+name+"', NULL, NULL ,"+"'"+domain+"','"+"careerify.net"+"',"+"'"+domain+".careerify.net"+"','"+str(connectionId)+"','"+str(taleoSettingId)+"',"+"'"+str(EmailSettingId)+"','"+isCustomerEnabled+"','"+logo+"',"+ "'"+avatar+"','"+str(FTPSettingId)+"','"+ baseReferralUrl+"','"+str(CustomerSettingId)+"','"+str(ATSSettingId)+"','"+LinkedInAvatar+"','76')")
#         else:
#             MasterDBConnection.execute("INSERT INTO Customers VALUES("+"'"+name+"', NULL, NULL ,"+"'"+domain+"','"+"careerify.net"+"',"+"'"+domain+".careerify.net"+"','"+str(connectionId)+"','"+str(taleoSettingId)+"',"+"'"+str(EmailSettingId)+"','"+isCustomerEnabled+"','"+logo+"',"+ "'"+avatar+"',NULL,'"+ baseReferralUrl+"','"+str(CustomerSettingId)+"','"+str(ATSSettingId)+"','"+LinkedInAvatar+"','76')")

#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        
#         #ADD ADMIN


#         loweredName = name.lower()
#         MembershipDB = create_engine(dbConnection+'/CareerifyMembership')
#         MembershipDBConnection = MembershipDB.connect()
#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#         MembershipDBConnection.execute("INSERT INTO aspnet_Applications VALUES("+"'"+name+"','"+loweredName+"',newid(),"+"NULL"+")")
#         asp_appId = MembershipDBConnection.execute("SELECT ApplicationId FROM aspnet_applications WHERE ApplicationName="+"'"+name+"'")
#         for asp in asp_appId:
#             appId = asp['ApplicationId']
#         #-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#         MembershipDBConnection.execute("INSERT INTO aspnet_users VALUES("+"'"+str(appId)+"',newid(),'"+loweredName+"admin@careerify.net','"+loweredName+"admin@careerify.net',NULL,"+"'0', getdate()"+")")
#         asp_userId = MembershipDBConnection.execute("SELECT UserId FROM aspnet_users WHERE ApplicationId="+"'"+str(appId)+"'")
#         for asp in asp_userId:
#             userId = asp['UserId']
#         #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------     
#         MembershipDBConnection.execute("INSERT INTO aspnet_Membership VALUES("+"'"+str(appId)+"','"+str(userId)+"','L3VasKxMcMaJTNX/nDmu1ki3mW4=','1','Fp/5zbQIh5mtiHO6RRB3WA==',NULL,'"+loweredName+"admin@careerify.net','"+loweredName+"admin@careerify.net', NULL, NULL, '1', '0', getdate(), getdate(), getdate(), '1754-01-01 00:00:00.000', '0', '1754-01-01 00:00:00.000', '0', '1754-01-01 00:00:00.000', null)")
#         #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#         MembershipDBConnection.execute("INSERT INTO aspnet_roles VALUES("+"'"+str(appId)+"', newid(), 'Administrator', 'administrator', null)")
#         asp_roleId = MembershipDBConnection.execute("SELECT RoleId FROM aspnet_roles WHERE ApplicationId="+"'"+str(appId)+"'")
#         for asp in asp_roleId:
#             roleId = asp['RoleId']
#         #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#         MembershipDBConnection.execute("INSERT INTO aspnet_roles VALUES("+"'"+str(appId)+"', newid(), 'Employee', 'employee', null)")
#         #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#         MembershipDBConnection.execute("INSERT INTO aspnet_UsersInRoles VALUES("+"'"+str(userId)+"','"+str(roleId)+"'"+")")
#         #--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------