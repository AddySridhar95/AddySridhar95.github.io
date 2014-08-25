from flask import Flask, render_template, request, flash, session, redirect, url_for, abort
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
from springfieldView import SpringfieldView, SpringfieldFirstload
# from revSpringfieldModels import revSpringfieldModel  
from springfieldModel import SpringfieldModel
from insertCustomer import InsertCustomer
#from revInsertCustomers import revInsertCustomer
from insertCandidate import InsertCandidate
#from revInsertCandidates import revInsertCandidate
app = Flask(__name__)
app.config.from_object(__name__)
app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='development key',
    USERNAME='admin',
    PASSWORD='default'
))

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = "Not logged in"
    if request.method == 'POST':
        if request.form['username'] != 'administrator':
            error = 'Invalid username'
        elif request.form['password'] != 'P3t3r81':
            error = 'Invalid password'
        else:
            error = None
            session['logged_in'] = True
            flash('You were logged in')
            return redirect('/dashboard')
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('landingpage'))


@app.route('/')
def landingpage():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect('/login')
    return render_template('index.html')

@app.route('/pikachu/<start_date>/<end_date>/<has_retrieved>/<db>')
def populate_dashboard(start_date, end_date, has_retrieved, db):
    allData=SpringfieldModel.get_data(start_date, end_date, has_retrieved, db)
    return jsonify({
			'success': True,
			'allData': allData,
			})


@app.route('/compareDataForm/<client>/<year>', methods = ['POST'])
def compareDataFormClient(client, year):
    data = SpringfieldModel.compareSingleClient(client, year)
    return jsonify({
            'data': data
        });

@app.route('/singleClientDataFromLaunch/<client>/<weeks>/<launch_date>', methods = ['POST'])
def singleClientDataFromLaunch(client, weeks, launch_date):
    data = SpringfieldModel.singleClientDataFromLaunch(client, weeks, launch_date)
    return jsonify({
            'data': data
        });


@app.route('/multipleClientsDataFromLaunch/<client>/<weeks>/<launch_date>', methods = ['POST'])
def multipleClientsDataFromLaunch(client, weeks, launch_date):
    data = SpringfieldModel.multipleClientsDataFromLaunch(client, weeks, launch_date)
    return jsonify({
            'data': data
        });

@app.route('/compareDataForm/<year>', methods = ['POST'])
def compareDataForm(year):
    compareData = []
    selectedClients = request.data.replace(" ", "")                     
    compareData = SpringfieldModel.compareMultipleClients(selectedClients, year)
    return jsonify({
        'compareData': compareData
        })

@app.route('/addCustomer')
def addCustomer():
    return render_template('addCustomer.html')

@app.route('/AddUserProfile/<client>')
def addUserProfile(client):
    data = InsertCustomer.add_user_profile(client)
    return data
    #make call to insertCustomer.py


@app.route('/SQLRunner')
def SQLRunnerRoute():
    return render_template('index.html')



@app.route('/SQLRunner/<clients>', methods=['POST'])
def SQLRunner(clients):
    script = request.data
    print(clients)
    print(script)
    data = SpringfieldModel.SQLrunner(script, clients)
    return data



@app.route('/addCandidate/<db>')
def addCandidate(db):
    session['db'] = db
    return render_template('addCandidate.html', error = "no_error", db = db)

@app.route('/submitCustomer', methods=['GET','POST'])
def submitCustomer():
    print("submitCustomer ROUTE HIT")
    # name=request.form['clientName']
    # domain=request.form['domainName']
    # atscompanycode=request.form['AtsCompanyCode']
    # atsId = request.form['atsId']
    # isCustomerEnabled = request.form['isCustomerEnabled']
    # if isCustomerEnabled == "yes":
    #     isCustomerEnabled = True
    # else:
    #     isCustomerEnabled = False

    # isGamificationEnabled = request.form['isGamificationEnabled']
    # if isGamificationEnabled == "yes":
    #     isGamificationEnabled = True
    # else:
    #     isGamificationEnabled = False


    # isInternalMobilityEnabled = request.form['isInternalMobilityEnabled']
    # if isInternalMobilityEnabled == "yes":
    #     isInternalMobilityEnabled = True
    # else:
    #     isInternalMobilityEnabled = False    


    # logo = request.form['logo']
    # avatar = request.form['avatar']
    # LinkedInAvatar = request.form['linkedin_avatar']
    # baseReferralUrl = request.form['baseReferralUrl']
    # taleoCompanyCode = request.form['taleoCompanyCode']
    # taleoUserName = request.form['taleoUserName']
    # taleoPassword = request.form['taleoPassword']
    # taleoInstance = request.form['taleoInstance']
    # taleoSourceIdentifier = request.form['taleoSourceIdentifier']
    # taleoEndPoint = request.form['taleoEndPoint']
    # TaleoLocation = request.form['TaleoLocation']
    # TaleoDepartment = request.form['TaleoDepartment']
    # SyncInterval = request.form['SyncInterval']
    # if request.form['isFTP'] == "yes":
    #     hostUri = request.form['hostUri']
    #     FTPusername = request.form['FTPusername']
    #     FTPpassword = request.form['FTPPassword']    
    #     isFTP = True
    # else:
    #     hostUri = ""
    #     FTPusername = ""
    #     FTPpassword = ""
    #     isFTP = False
    customerData = request.get_json(True)
    #print(request.POST('name'))
    ans = InsertCustomer.insert_customer(customerData['name'], customerData['domain'], customerData['atscompanycode'], customerData['atsId'], customerData['isCustomerEnabled'], customerData['isGamificationEnabled'], customerData['isInternalMobilityEnabled'], customerData['logo'], customerData['avatar'], customerData['linkedin_avatar'], customerData['baseReferralUrl'], customerData['taleoCompanyCode'], customerData['taleoUserName'], customerData['taleoPassword'], customerData['taleoInstance'], customerData['taleoSourceIdentifier'], customerData['taleoEndPoint'], customerData['TaleoDepartment'], customerData['TaleoLocation'], customerData['SyncInterval'], customerData['hostUri'], customerData['FTPusername'], customerData['FTPpassword'], customerData['ftp'])
    print(ans)
    #print(customerData)
    print(customerData)
    print(request.get_json(True))
    return ans
    #return render_template('addCustomer.html')
    

@app.route('/getCustomerList', methods=['GET','POST'])
def getCustomerList():
    customerArray = []
    customerArray = SpringfieldModel.get_clients("YL")
    session['customerArray'] = customerArray
    return jsonify({
        'customerArray': customerArray,
        'success': True,
        })


@app.route('/getCustomerListTemp', methods=['GET','POST'])
def getCustomerListTemp():
    customerArray = []
    customerArray = SpringfieldModel.get_clients("YL")
    session['customerArray'] = customerArray
    return jsonify({
        'customerArray': customerArray,
        'success': True,
        })

@app.route('/submitCandidate', methods=['GET','POST'])
def submitCandidate():
    client = request.form['client']
    ATSCandidateId=request.form['ATSCandidateId']
    firstName=request.form['firstName']
    lastName=request.form['lastName']
    email = request.form['email']
    reqId = request.form['reqId']
    referrerEmail = request.form['referrerEmail']
    message = InsertCandidate.insert_candidate(client, ATSCandidateId, firstName, lastName, email, reqId, referrerEmail, session['db'])
    error = message
    if error[1:-1] == "success":     # error is currently ""success"". we want it to be "success" error[1:-1] is a substring of error
        return render_template('addCandidate.html', error = "no_error", db = session['db'])
    else:
        return render_template('addCandidate.html', error = error[1:-1], db = session['db'])
if __name__ == '__main__':
    app.run(debug=True)