#! python2
import webapp2
import jinja2
import os
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.ext import blobstore
from google.appengine.ext.blobstore import BlobKey
from google.appengine.api.images import *
from google.appengine.ext.webapp import blobstore_handlers
from datastore import MyUser

from google.appengine.api.blobstore.blob_storage import *
JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)
class Edit(webapp2.RequestHandler):
	def get(self):
		self.response.headers['Content-Type'] = 'text/html'
		user = users.get_current_user()
		if user:
			myuser_key = ndb.Key('MyUser', user.user_id())
			myuser = myuser_key.get()
			upload_url = blobstore.create_upload_url('/upload_photo')
			pic_key=myuser.DP
			key = BlobKey(str(myuser.DP))
			url= get_serving_url(key)
			template_values = {
				'myuser' : myuser,
	            'user' : user,
				'upload_url' : upload_url,
				'pic_key' : pic_key,
				'url' : url,
				}
			template = JINJA_ENVIRONMENT.get_template('edit.html')
		else:
			template = JINJA_ENVIRONMENT.get_template("error.html")
			template_values = {
			"error" : "Please login first!" ,
			"url" : "/",
			}

		self.response.write(template.render(template_values))

class PhotoUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		self.response.headers['Content-Type'] = 'text/html'
		if self.request.get('button') == 'Update':
			user = users.get_current_user()
			if user:
				upload = self.get_uploads('file')[0]
				myuser_key = ndb.Key('MyUser', user.user_id())
				myuser = myuser_key.get()
				myuser.name = self.request.get('users_name')
				myuser.age = int(self.request.get('users_age'))
				upload_url = blobstore.create_upload_url('file')
				myuser.DP = upload.key()
				myuser.put()

				# self.redirect('/show/%s' % upload.key())

			elif self.request.get('button') == 'Cancel':
				self.redirect('/')
class show(blobstore_handlers.BlobstoreDownloadHandler):
	def get(self, pic_key):
		if not blobstore.get(pic_key):
			self.error(404)
		else:
			return send_blob(pic_key)
			#self.send_blob(pic_key)
