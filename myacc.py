#! python2
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext.blobstore import BlobKey
from google.appengine.api.images import *
import os
from datastore import MyUser
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class MyAc(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()
		post = []
		cap = []
		keys = []
		for key in reversed(myuser.post):
			ndbk = key.get()
			cap.append(ndbk.cap)
			keys.append(ndbk.pst)
		for key in keys:
			post.append(get_serving_url(key))
		if user:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()

			key = BlobKey(str(myuser.DP))
			mimg= get_serving_url(key)
			len1 = len(myuser.follows)
			len2 = len(myuser.followers)
			template_values = {
                'myuser' : myuser,
                'mimg' : mimg,
                'len1' : len1,
                'len2' : len2,
				'post' : post,
				'cap' : cap
			}
			template = JINJA_ENVIRONMENT.get_template('myac.html')
		else:
			template = JINJA_ENVIRONMENT.get_template("error.html")
			template_values = {
			"error" : "Please login first!" ,
			"url" : "/",
			}
		self.response.write(template.render(template_values))
