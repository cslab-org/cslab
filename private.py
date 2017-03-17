
import webapp2
from google.appengine.api import users

import logging
import os
import jinja2

# import the Account ndb Model
from account import *
from model import *

template_dir = os.path.join(os.path.dirname(__file__), 'blog-articles')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),  autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		try:
			return (jinja_env.get_template(template)).render(params)
		except:
			# TODO - Be careful about blog/blog-error.html
			return (jinja_env.get_template('blog-error.html')).render()

	def render(self, template, **html_add_ins):
		self.write(self.render_str(template, **html_add_ins))


# Articles only viewable to myslef or a list of approved authors
class PrivateHandler(Handler):
	def get(self, url):
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
				
				if url and url is not '/':
					# Dynamic pages not static as in earlier version
					link = url[1:]
					# Retrieve the article from the datastore
					qry = Article.query(ndb.AND(Article.link==link, Article.kind=="private"))
					qry_result = qry.fetch()
					article = qry_result[0] # only one, but result is a list

					# format date properly
					date = article.dateCreated.strftime('%d %b %Y')

					self.render('blog-article.html', title=article.title, content=article.content, date=date, kind="Reminders")

				else:
					# retrieve the list of all blog articles and render
					# TODO - pagination with 20 blog articles at a time
					qry = Article.query(Article.kind=="private").order(-Article.lastEdited)
					qry_result = qry.fetch()

					# if qry_result is empty
					if (len(qry_result) == 0):
						self.render('blog-error.html', message="Sorry! The page doesn't exist")
					else:	
						# Add a date field which is in proper format
						for a in qry_result:
							a.date = a.dateCreated.strftime('%d %b %Y')
						self.render('blog-home.html', articles=qry_result, kind="private")	# this is for the link /private/link	



			# if not an approved user
			else:
				self.write('blog-error.html', message='Access Denied! Contact Admin')	

		# logging in is mandatory
		else:
			self.redirect(users.create_login_url(self.request.url))	


