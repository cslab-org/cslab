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
	description = ndb.TextProperty()
	# kind can be either of "blog", "project" or "private", but not enforcing it
	kind = ndb.StringProperty()


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
				self.write('You dont have permission write articles! Contact Admin')	

		else:
			self.redirect(users.create_login_url(self.request.url))	




