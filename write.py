#!/usr/bin/env python
# @author Binu Jasim
# @created on 1 Mar 2017

import webapp2
from google.appengine.ext import ndb
from google.appengine.api import users
import logging
import datetime
import json

import os
import jinja2

from account import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),  autoescape = True)

# Keep the details of articles
class Article(ndb.Model):
	# The parent of an Entry is Account
	dateCreated = ndb.DateProperty()	
	lastEdited = ndb.DateProperty(indexed = True)
	content = ndb.TextProperty()
	title = ndb.StringProperty() # max 500 characters
	# description is max 500 characters - we won't enforce it but more will cause a write error
	description = ndb.StringProperty()
	# kind can be either of "blog", "project" or "private", but not enforcing it
	kind = ndb.StringProperty()
	# link is not a key. only keep newton-method in staed of cslab.org/blog/newton-method
	link = ndb.StringProperty(required=True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		try:
			return (jinja_env.get_template(template)).render(params)
		except:
			# TODO - Be careful about blog/blog-error.html
			return (jinja_env.get_template('site-error.html')).render()

	def render(self, template, **html_add_ins):
		self.write(self.render_str(template, **html_add_ins))


class WriteHandler(Handler):
	def get(self):
		# make sure the user is logged in
		user = users.get_current_user()
		if user:
			user_id = user.user_id()
			nickname = user.nickname()
			email = user.email()
			logout = users.create_logout_url('/')
			# Proceed only if an approved user
			if (is_approved_user(email)):
				# register user if not already registered
				status = Account.my_get_or_insert(user_id, nickname = nickname, email = email)
				
				self.render('write.html',
					user_name = user.nickname(), 
					logout_url = logout)		

			else:
				self.write('You dont have permission to write articles! Contact Admin')	

		else:
			self.redirect(users.create_login_url(self.request.url))	


	def post(self):
		
		user = users.get_current_user()
		if user is None: 
			# redirect doesn't work in ajax
			self.redirect(users.create_login_url(self.request.url))	
			
		else:
			user = users.get_current_user()
			user_ent_key = ndb.Key(Account, user.user_id())	

			t = datetime.date.today() # datetime.date(2017, 1, 10) 
			ndb_date = t#.replace(year = int(date[0:4]), month = int(date[5:7]), day = int(date[8:10]))

			article = Article(parent=user_ent_key, dateCreated=ndb_date, lastEdited=ndb_date, content="**bold** *article*", title="RNN", description="my first project", kind="project", link="rnn")		
			article.put()



class WriteAjaxHandler(Handler):
	# To retrieve the list of all articles
	def get(self):
		# make sure the user is logged in
		user = users.get_current_user()
		if user is None:
			# Redirect actually doesn't work in ajax - still... leave it 
			self.redirect(users.create_login_url(self.request.url))	
			
		else:
			user_id = user.user_id()
			user_ent_key = ndb.Key(Account, user_id)

			qry = Article.query(ancestor=user_ent_key).order(-Article.lastEdited)
			qry_result = qry.fetch()

			# The dates are has to be made JSON serializable
			response_data = []
			for entry in qry_result:
				date = entry.lastEdited
				last_date = ('0'+str(date.day) if date.day < 10 else str(date.day)) + '-' + ('0'+str(date.month) if date.month < 10 else str(date.month)) + '-' + str(date.year)

				temp = {"id":entry.key.id(), "lastEdited":last_date, "title":entry.title, "description":entry.description, "link":entry.link, "kind":entry.kind}
				response_data.append(temp)

			self.response.out.write(json.dumps(response_data))



# To render the writedown page where we write markdown 
class WriteDownHandler(Handler):
	# To render page with db query to the content
	def get(self):
		# make sure the user is logged in
		user = users.get_current_user()
		if user is None:
			# Redirect actually doesn't work in ajax - still... leave it 
			self.redirect(users.create_login_url(self.request.url))	
			
		else:
			user_id = user.user_id()
			id_article = str(self.request.get('id'))
			# It's weird that user_id is string but id_article is int
			article_key = ndb.Key('Account', user_id, 'Article', int(id_article))
			article = article_key.get()
			if article is None:
				logging.error('********Error********'+ str(article_key.parent()) + '******Error******')
				self.response.write('*****************Sorry Couldnt retrieve item************')
			else:	
				self.render('writedown.html', user_name = user.nickname(), content=article.content)	
			
