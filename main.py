#! python2
import webapp2
import jinja2
from search import *
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from datastore import *
from edit import *
from addpost import *
from userinfo import *
from follow import *

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		url = ''
		url_string = ''
		welcome = 'Welcome back'
		myuser = None
		user = users.get_current_user()
		keys=[]
		post = []
		cap = []

		if user:
			url = users.create_logout_url(self.request.uri)
			url_string = 'logout'
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			if myuser == None:
				welcome = 'Welcome to the application'
				myuser = MyUser(id=user.user_id())
				myuser.email_address = user.email()
				myuser.put()

			if myuser.name==None:
				self.redirect('/edit')
			if myuser:
				for key in reversed(myuser.post):
					ndbk = key.get()
					cap.append(ndbk.cap)
					keys.append(ndbk.pst)
				for key in keys:
					post.append(get_serving_url(key))

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'
		template_values = {
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'myuser' : myuser,
			'key' : keys,
			'post' : post,
			'cap' : cap
		}
		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/', MainPage),
('/edit', Edit),
('/upload_photo', PhotoUploadHandler),
('/show/([^/]+)?',show),
('/search', Search),
('/adpost',AdPost),
('/User',User),
('/follower', Follower),
('/following', Following)
], debug=True)
