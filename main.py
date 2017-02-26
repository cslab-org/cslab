#!/usr/bin/env python
# @author Binu Jasim
# @created on 19-Sep-2015

import webapp2
import os
import jinja2

from timer import *
from blog import *

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
			self.redirect('/timer')			

		else:
			self.response.write('Access Denied')



class MainHandler(webapp2.RequestHandler):
    def get(self):
        #self.response.write('<h1> CS Laboratory</h1><h3>Author: <a href="https://github.com/bnjasim">Binu Jasim</a></h3><ul><li><a href="isl">Visualizing Indian Super Leageue Home Attendance</a></li><li><a href="paint">Paint Application</a></li><li><a href="texteditor">Rich Text Editor with Paint support in AngularJS</a></li></ul>')
        self.response.write('<h1> CS Laboratory</h1><li><a href="datamining">Data Mining, Monsoon Semester 2016</a></li><li><a href="dbms">Data Base Management Systems, Monsoon Semester 2016</a></li><br/><br/><li><a href="pattern">Pattern Recognition Winter 2016</a></li><li><a href="nlp">Natural Language Processing Winter 2016</a></li></ul>')

class BrowHandler(Handler):
	def get(self):
		self.render("browpad.html")

class IslHandler(Handler):
	def get(self):
		self.render("slopegraph-isl.html")

class PaintHandler(Handler):
	def get(self):
		self.render('paintangular.html')

class TEHandler(Handler):
	def get(self):
		self.render('angular-rte.html')	

class PatternRecognitionHandler(Handler):
	def get(self):
		self.render('pattern.html')

class NlpHandler(Handler):
	def get(self):
		self.render('nlp.html')

class DBMSHandler(Handler):
	def get(self):
		self.render('dbms.html')

class DMHandler(Handler):
	def get(self):
		self.render('dm.html')	


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/browpad', BrowHandler),
    ('/isl', IslHandler),
    ('/paint', PaintHandler),
    ('/texteditor', TEHandler),
    ('/pattern', PatternRecognitionHandler),
    ('/nlp', NlpHandler),
    ('/dbms', DBMSHandler),
    ('/datamining', DMHandler),
    (r'/blog(/.*)?', BlogHandler),
    ('/timer', TimerHandler),
    ('/timerajax', TimerAjaxHandler),
    ('/timerdata', TimerDataHandler),
    ('/login', RegisterUserHandler)
], debug=True)
