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
from post import *
from myacc import *
from datetime import datetime

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
		msg = ''
		myuser = None
		user = users.get_current_user()
		pic = []
		rcpic = []
		allpost = PostDb().query().order(-PostDb.time).fetch()
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
			if myuser.name == None:
				self.redirect('/edit')
			if myuser.post == [] and myuser.follows == []:
				msg='No post yet'

		if myuser:
			for post in allpost:
				if myuser.follows:
					for fp in myuser.follows:
						if (post.key in fp.get().post) or (post.key in myuser.post) :
							if(post not in pic):#allpost.remove(post)
								pic.append(post)
				else:
					if post.key in myuser.post:
						pic.append(post)
			for key in pic:
				rcpic.append(get_serving_url(key.pst))

		else:
			url = users.create_login_url(self.request.uri)
			url_string = 'login'
		template_values = {
			'url' : url,
			'url_string' : url_string,
			'user' : user,
			'welcome' : welcome,
			'myuser' : myuser,
			'allpost' : allpost,
			'pic' : pic,
			'rcpic' : rcpic,
			'msg': msg
		}
		template = JINJA_ENVIRONMENT.get_template('main.html')
		self.response.write(template.render(template_values))

app = webapp2.WSGIApplication([
('/', MainPage),
('/edit', Edit),
('/search', Search),
('/adpost',AdPost),
('/User',User),
('/follower', Follower),
('/following', Following),
('/post', Post),
('/myac', MyAc)
], debug=True)
