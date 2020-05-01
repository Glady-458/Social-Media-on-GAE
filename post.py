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
class Post(webapp2.RequestHandler):
    def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()
		if user:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			key = self.request.get('id')
			pic = ndb.Key('PostDb',int(self.request.get('id'))).get()
			mimg= get_serving_url(pic.pst)
			template_values = {
                'myuser' : myuser,
                'mimg' : mimg,
			}
			template = JINJA_ENVIRONMENT.get_template('post.html')
		else:
			template = JINJA_ENVIRONMENT.get_template("error.html")
			template_values = {
			"error" : "Please login first!" ,
			"url" : "/",
			}
		self.response.write(template.render(template_values))


    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser_key = ndb.Key('MyUser', user.user_id())
        myuser = myuser_key.get()
        if user:
            usr = ndb.Key('MyUser',self.request.get('id2')).get()
            if self.request.get("fb") == "Follow":
                myuser.follows.append(ndb.Key('MyUser',usr.key.id()))
                usr.followers.append(ndb.Key('MyUser',myuser.key.id()))
                myuser.put()
                usr.put()
                self.redirect('/')
            elif self.request.get("fb") == "Unfollow":
                myuser.follows.remove(ndb.Key('MyUser',usr.key.id()))
                usr.followers.remove(ndb.Key('MyUser',myuser.key.id()))
                myuser.put()
                usr.put()
                self.redirect('/')
