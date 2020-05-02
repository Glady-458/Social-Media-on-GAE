#!python2
import webapp2
import jinja2
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.blobstore import BlobKey
from google.appengine.ext.webapp import blobstore_handlers
import os
from datetime import datetime
from datastore import *
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class AdPost(blobstore_handlers.BlobstoreUploadHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user()
        if user:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			mypost = None
			post_key = ndb.Key('PostDb', user.user_id())
			mypost = post_key.get()
			upload_url = blobstore.create_upload_url('/adpost')
			key = BlobKey(str(myuser.DP))
			template_values = {
				'myuser' : myuser,
	            'user' : user,
				'upload_url' : upload_url,
				'mypost' : mypost,
				#'url' : url
			}
			template = JINJA_ENVIRONMENT.get_template('addpost.html')
			self.response.write(template.render(template_values))

    def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		# upload = self.get_uploads('file')[0]
		myuser_key = ndb.Key('MyUser', user.user_id())
		myuser = myuser_key.get()
		if user:
			if self.request.get('Button') == "Add":
				upload = self.get_uploads('file')[0]
				mypost = PostDb()
				mypost.pst=upload.key()
				mypost.cap=self.request.get('P_Caption')
				mypost.time=datetime.now()
				mypost.postby=ndb.Key('MyUser',myuser.key.id())
				mypost.put()
				myuser.post.append(ndb.Key('PostDb',mypost.key.id()))
				myuser.put()
				self.redirect('/')
			elif self.request.get('Button') == "Cancel":
				self.redirect('/')
