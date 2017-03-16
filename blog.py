
import webapp2
import logging
import os
import jinja2

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



class BlogHandler(Handler):
	def get(self, url):
		#logging.error('\nurl is '+url)
		if url and url is not '/':
			# self.render(link+'.html')
			# Dynamic pages not static as in earlier version
			link = url[1:]
			# Retrieve the article from the datastore
			qry = Article.query(ndb.AND(Article.link==link, Article.kind=="blog"))
			qry_result = qry.fetch()
			article = qry_result[0] # only one, but result is a list
			
			self.render('blog-article.html', title=article.title, content=article.content, date=article.dateCreated)

		else:
			self.render('blog-home.html')		
		#self.response.out.write(url)