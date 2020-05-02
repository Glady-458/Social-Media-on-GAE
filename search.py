#! python2
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
import os
from datastore import MyUser
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class Search(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        myuser = ndb.Key('MyUser',user.user_id()).get()
        template_values = {
            'myuser' : myuser,
        }
        template = JINJA_ENVIRONMENT.get_template('discover.html')
        self.response.write(template.render())

    def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		myuser = ndb.Key('MyUser',user.user_id()).get()
		name = ''
		list = []
		if self.request.get('button') == "Cancel":
			self.redirect('/')
		elif self.request.get('button') == "Search":
			if self.request.get('name') == '':
				list = MyUser.query().fetch()
			else:
				name = self.request.get('name')
				list = MyUser.query().filter(MyUser.name == name).fetch()
            	template_values = {
                'list' : list,
                'n' : name,
                'myuser' : myuser
            }
		template = JINJA_ENVIRONMENT.get_template('discover.html')
		self.response.write(template.render(template_values))
