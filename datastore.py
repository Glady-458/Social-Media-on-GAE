#! python2
from google.appengine.ext import ndb

class MyUser(ndb.Model):
	email_address = ndb.StringProperty()
	name = ndb.StringProperty()
	age = ndb.IntegerProperty()
	DP = ndb.BlobKeyProperty()
	post = ndb.KeyProperty(kind='PostDb', repeated = True)
	follows = ndb.KeyProperty(kind='MyUser', repeated = True)
	followers = ndb.KeyProperty(kind='MyUser', repeated = True)

class PostDb(ndb.Model):
	pst = ndb.BlobKeyProperty()
	postby = ndb.KeyProperty(kind='MyUser')
	cap = ndb.StringProperty()
	time = ndb.DateTimeProperty()
	comment = ndb.KeyProperty(kind='Comment', repeated=True)
	like = ndb.KeyProperty(kind='MyUser', repeated = True)

class Comment(ndb.Model):
	user = ndb.KeyProperty(MyUser)
	pst = ndb.KeyProperty(PostDb)
	comment = ndb.StringProperty()
	time = ndb.DateTimeProperty()
