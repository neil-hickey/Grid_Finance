import os, json, glob, csv
import pandas as pd

from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug import secure_filename
from uuid import uuid4
from algorithm import Categorise
from reconciliation_tool import app
# from model import db

################################
#           Routing            #
################################

c = None

# url  routing
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

# This route will show a form to perform an AJAX request
# jQuery is loaded to execute the request and update the
# value of the operation
@app.route('/')
def index():
    return render_template('index.html',active_page = "index")

@app.route('/old_reports')
def export():
    return render_template('old_reports.html',active_page = "old_reports")


# Route that will process the file upload
@app.route('/upload', methods=['POST'])
def upload():
    # Create a unique "session ID" for this particular batch of uploads.
    upload_key = str(uuid4())
    # Target folder for these uploads.
    target = "reconciliation_tool/static/uploads/{}".format(upload_key)
    # Check if the file is one of the allowed types/extensions

    session['target'] = target

    try:
        os.mkdir(target)
    except:
        return "Couldn't create upload directory: {}".format(target)

    for i in range(0,len(request.files)):
        s = 'file[' + str(i) + ']'
        uploaded_file = request.files.getlist(s)[0]

        # Check if the file is one of the allowed types/extensions
        if uploaded_file and allowed_file(uploaded_file.filename):
            # Make the filename safe, remove unsupported chars
            filename = secure_filename(uploaded_file.filename)

            fString = 'file' + str(i)
            session[fString] = filename

            # Move the file form the temporal folder to
            # the upload folder we setup
            destination = "/".join([target, filename])
            print "Accept incoming file:", filename
            print "Save it to:", destination
            uploaded_file.save(destination)
        else:
            return error_message()
    
    # Return json 
    return jsonify(filename_name=filename)
    
@app.route('/report')
def generateReport():
    if 'target' in session:
        global c 
        c = Categorise(session['file1'],session['file0'],session['target']) 
        # csvoutput = c.run()
        # session['report'] = csvoutput
        c.run()
        return c.getDataFrame1()
        # return render_template('report.html',data=csvoutput)
    else:
        return error_message()

@app.route('/report_matches')
def getReportMatches():
    global c
    return c.getDataFrame2()

@app.route('/files')
def viewFiles():     
    return render_template('files.html')   

@app.route('/file_fund')
def getFundFile():
    file_name = destination = "/".join([session['target'], session['file1']])
    file = pd.read_csv(file_name)
    return file.to_json(orient="records");

@app.route('/file_bank')
def getBankFile():
    file_name = destination = "/".join([session['target'], session['file0']])
    file = pd.read_csv(file_name)
    return file.to_json(orient="records");

@app.route('/testdb')
def testdb():
  if db.session.query("1").from_statement("SELECT 1").all():
    return 'It works.'
  else:
    return 'Something is broken.'

################################
#        Helper functions      #
################################

def error_message():
    return HttpResponse(
            json.dumps({"status": "error"}),
            content_type="application/json"
        )

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
     filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

