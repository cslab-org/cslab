from google.appengine.ext import ndb


# Keep the details of articles
class Article(ndb.Model):
	# The parent of an Entry is Account
	dateCreated = ndb.DateProperty()	
	lastEdited = ndb.DateProperty(indexed = True) # indexed = True is only useful for changing previous indexed = False
	content = ndb.TextProperty()
	title = ndb.StringProperty() # max 500 characters
	# description is max 500 characters - we won't enforce it but more will cause a write error
	description = ndb.StringProperty(indexed = False)
	# kind can be either of "blog", "project" or "private", but not enforcing it
	kind = ndb.StringProperty()
	# link is not a key. only keep newton-method in staed of cslab.org/blog/newton-method
	link = ndb.StringProperty(required=True)
