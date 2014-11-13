#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import os

import webapp2
import MySQLdb

from models import UserRequest

# Define your production Cloud SQL instance information.
_INSTANCE_NAME = 'simple-gae-app1:mydb'


class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Display existing guestbook entries and a form to add new entries.
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='simplegaeapp', user='root')
        else:
            db = MySQLdb.connect(host='127.0.0.1', port=3306, db='simplegaeapp', user='root', passwd="root")
            # Alternatively, connect to a Google Cloud SQL instance using:
            # db = MySQLdb.connect(host='ip-address-of-google-cloud-sql-instance', port=3306, user='root')

        cursor = db.cursor()

        user_request = UserRequest(self.request.get("api_key"), self.request.get("user_id"),
                                   self.request.get("encoded_user_email"))
        # Not required
        user_request.beacon_id = self.request.get("beacon_id")
        user_request.group = self.request.get("group")
        user_request.campaign = self.request.get("campaign")
        user_request.sent_date = self.request.get("sent_date")
        user_request.custom_1 = self.request.get("custom_1")
        user_request.custom_2 = self.request.get("custom_2")
        user_request.custom_3 = self.request.get("custom_3")
        # Set response type
        self.response.headers['Content-Type'] = 'application/json'
        # Validate required fields
        if not user_request.validate_on_submit():
            result = {"error": "api_key and user_id and encoded_user_email is required."}
            return self.response.out.write(json.dumps(result))

        #print(user_request.as_sql_string())
        cursor.execute(user_request.as_sql_string())
        db.commit()
        db.close()

        return self.response.out.write(json.dumps({"OK": True}))


class TableHandler(webapp2.RequestHandler):
    def get(self):
        # Display existing guestbook entries and a form to add new entries.
        if (os.getenv('SERVER_SOFTWARE') and
            os.getenv('SERVER_SOFTWARE').startswith('Google App Engine/')):
            db = MySQLdb.connect(unix_socket='/cloudsql/' + _INSTANCE_NAME, db='simplegaeapp', user='root')
        else:
            db = MySQLdb.connect(host='127.0.0.1', port=3306, db='simplegaeapp', user='root', passwd="root")
            # Alternatively, connect to a Google Cloud SQL instance using:
            # db = MySQLdb.connect(host='ip-address-of-google-cloud-sql-instance', port=3306, user='root')

        cursor = db.cursor()
        cursor.execute("SELECT * FROM requests LIMIT 1000;")

        requests = []
        for row in cursor.fetchall():
            requests.append(dict([('request_id', row[0]),
                                 ('api_key', row[1]),
                                 ('user_id', row[2]),
                                 ('encoded_user_email', row[3]),
                                 ('beacon_id', row[4]),
                                 ('group', row[5]),
                                 ('campaign', row[6]),
                                 ('sent_date', row[7]),
                                 ('custom_1', row[8]),
                                 ('custom_2', row[9]),
                                 ('custom_3', row[10])]))

        self.response.headers['Content-Type'] = 'application/json'
        return self.response.out.write(json.dumps({"First 1000 requests: ": requests}))


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/requests', TableHandler),
], debug=True)
