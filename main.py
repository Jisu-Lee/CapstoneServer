# [START app]
import logging
import cgi
import datetime
import webapp2
import datetime
from operator import itemgetter
#import numpy as np
#import matplotlib.pyplot as plt
#import tensorflow

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
  date = ndb.DateTimeProperty(indexed=True)
  location = ndb.StringProperty(indexed=True)
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


# [START expectation]
@app.route('/expectation')
def expectation() :
    # fetch database
    entities = ndb.gql('SELECT date, value '
                       'FROM FineDust '
                       'WHERE location = \'HJRoom\'',)
    x = []
    y = []
    for entity in entities:
        x.append(entity.date)
        y.append(entity.value)
    response = 'Average concentration at HyeongJune\'s room : ' + str(sum(y)/len(y)) + '<br>'

    entities = ndb.gql('SELECT date, value '
               'FROM FineDust '
               'WHERE location = \'5P\'',)
    x = []
    y = []
    for entity in entities:
        x.append(entity.date)
        y.append(entity.value)

    logging.info(x)
    logging.info(y)
   
    response = response + 'Average concentration at 5P : ' + str(sum(y)/len(y)) + '<br>'

    entities = ndb.gql('SELECT * '
                       'FROM FineDust '
                       'ORDER BY date ASC LIMIT 100'
                       ,)
    #from operator import itemgetter
    #newlist = sorted(list_to_be_sorted, key=itemgetter('name')) 
    # entities = sorted(r_entities, key=itemgetter('date'))

    # create response
    response += """<html>
<head>
  <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['line']});
      google.charts.setOnLoadCallback(drawChart);

    function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('datetime', 'date');
      data.addColumn('number', 'humidity');
      data.addColumn('number', 'temperature');
      data.addColumn('number', 'concentration');

      data.addRows([
        """
    #myDate = datetime.strptime(str(entity.date),'%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
    i = 1
    First = True
    for entity in entities:
        response += '[ new Date(' + str(entity.date.year) + ',' + str(entity.date.month) + ',' + str(entity.date.day) + ',' + str(entity.date.hour) + ',' + str(entity.date.minute) + ',' + str(entity.date.second) +'),'
        response += str(entity.humidity) + ','
        response += str(entity.temperature) + ','
        response += str(entity.value) + '],'
        
    response += '[new Date(2018, 6, 3, 03, 14, 30), 2, 3, 4]'

    response += """
      ]);

      var options = {
        chart: {
          title: '100 data collected most recently',
          subtitle: 'humidity, concentration, temperature'
        },
        width: 900,
        height: 500,
        axes: {
          x: {
            0: {side: 'top'}
          }
        }
      };

      var chart = new google.charts.Line(document.getElementById('line_top_x'));

      chart.draw(data, google.charts.Line.convertOptions(options));
    }
  </script>
</head>
<body>
  <div id="line_top_x"></div>
</body>
</html>"""

    return response
# [END expectation]


@app.errorhandler(500)
def server_error(e):
    # Log the error and stacktrace.
    logging.exception('An error occurred during a request.')
    return 'An internal error occurred.', 500
# [END app]