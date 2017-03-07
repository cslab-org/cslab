#!/usr/bin/env python
# @author Binu Jasim
# @created on 19-Sep-2015

import webapp2
import os
import jinja2

from timer import *
from blog import *
from demo import *
from teach import *
from projects import *
from private import *
from write import *

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), 
								autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		try:
			return (jinja_env.get_template(template)).render(params)
		except:
			return (jinja_env.get_template('blog/blog-error.html')).render()

	def render(self, template, **html_add_ins):
		self.write(self.render_str(template, **html_add_ins))
	



class RegisterUserHandler(webapp2.RequestHandler):
	"Redirected to here from the login page. So always user is not None"
	def get(self):
		user = users.get_current_user()
		if user:
			user_id = user.user_id()
			nickname = user.nickname()
			email = user.email()
			status = Account.my_get_or_insert(user_id, 
				nickname = nickname, 
				email = email)
			# Login successful Redirecting to timer. But may have to change later
			# self.redirect('/timer')			

		else:
			self.response.write('Access Denied')



class MainHandler(Handler):
    def get(self):
        self.render('home.html')

class BrowHandler(Handler):
	def get(self):
		self.render("browpad.html")



app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/browpad', BrowHandler),
    
    (r'/blog(/.*)?', BlogHandler),
    (r'/demo(/.*)?', DemoHandler),
    (r'/teaching(/.*)?', TeachHandler),
    (r'/projects(/.*)?', ProjectsHandler),
    (r'/private(/.*)?', PrivateHandler),

    ('/timer', TimerHandler),
    ('/timerajax', TimerAjaxHandler),
    ('/timerdata', TimerDataHandler),

    ('/write', WriteHandler),
    ('/writeajax', WriteAjaxHandler),
    ('/writecheck', WriteCheckAvailability),    
    ('/writedown', WriteDownHandler),


    ('/login', RegisterUserHandler)
], debug=True)
