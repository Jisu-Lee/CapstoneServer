# [START app]
import logging
import cgi
import datetime
import webapp2
import datetime

# [START imports]
from flask import Flask, render_template, request
from google.appengine.ext import ndb
from google.appengine.api import users
# [END imports]

# [START create_db]
class FineDust(ndb.Model):
  value = ndb.FloatProperty()
  humidity = ndb.FloatProperty()
  temperature = ndb.FloatProperty()
  date = ndb.DateTimeProperty()
  location = ndb.StringProperty()
# [END create_db]

# [START create_app]
app = Flask(__name__)
# [END create_app]

# [START getdata]
@app.route('/getdata', methods=['GET', 'POST'])
def getdata() :
    app.logger.debug("JSON received...")
    app.logger.debug(request.json)

    if request.json:
        data = request.json
        entity = FineDust()

        entity.value = float(data['value'])
        entity.humidity = float(data['humidity'])
        entity.temperature = float(data['temperature'])
        entity.date = datetime.datetime.strptime(data['date'], '%Y-%m-%d_%H:%M:%S')
        entity.location = data['location']

        logging.info(entity)
        entity.put()

        return "Thanks. data is %s" % data
    else:
        return "no json recieved\n"

# [START form]
@app.route('/form')
def form():
    return render_template('form.html')
# [END form]


# [START submitted]
@app.route('/submitted', methods=['POST'])
def submitted_form():
    name = request.form['name']
    email = request.form['email']
    site = request.form['site_url']
    comments = request.form['comments']

    # [END submitted]
    # [START render_template]
    return render_template(
        'submitted_form.html',
        name=name,
        email=email,
        site=site,
        comments=comments)
    # [END render_template]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]