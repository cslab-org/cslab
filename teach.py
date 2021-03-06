
import webapp2
import logging
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'teaching-templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),  autoescape = True)

class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
	
	def render_str(self, template, **params):
		try:
			return (jinja_env.get_template(template)).render(params)
		except:
			# TODO - Be careful about blog/blog-error.html
			return (jinja_env.get_template('teaching-error.html')).render()

	def render(self, template, **html_add_ins):
		self.write(self.render_str(template, **html_add_ins))



class TeachHandler(Handler):
	def get(self, url):
		#logging.error('\nurl is '+url)
		if url and url is not '/':
			self.render(url+'.html')
		else:
			self.render('teaching-home.html')		
		#self.response.out.write(url)