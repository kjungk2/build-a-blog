import webapp2
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                        autoescape = True)


class Handler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.write(*a, **kw)

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(params)

	def render(self, template, **kw):
		self.write(self.render_str(template, **kw))


class BlogPost(db.Model):
    title = db.StringProperty(required=True)
    post = db.TextProperty(required=True)
    post_preview = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)


class MainHandler(Handler):
    def render_main(self, blogposts):
        self.render("mainblog.html", blogposts=blogposts)

    def get(self):
        blogposts = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC LIMIT 5")
        self.render_main(blogposts)


class NewPostHandler(Handler):
    def render_newpost(self, title="", body="", error=""):
        self.render("newpost.html", title=title, body=body, error=error)

    def get(self):
        t = jinja_env.get_template("newpost.html")
        content = t.render()
        self.response.write(content)

    def post(self):
        new_title = self.request.get("title")
        new_body = self.request.get("body")

        if not new_title:
            error = "Provide a Title"
            self.render_newpost(new_title, new_body, error)

        elif not new_body:
            error = "Provide some content"
            self.render_newpost(new_title, new_body, error)

        elif new_title and new_body:
            b = BlogPost(title = new_title, post = new_body, post_preview = new_body[:30] + "...")
            b.put()
            id_int = b.key().id()
            self.redirect("/blog/" + str(id_int))

class ViewPostHandler(Handler):
    def get(self, id):
        blogpost = BlogPost.get_by_id(int(id))
        self.render("singlepost.html", blogpost=blogpost)
        
        #content = blogpost.post
        #self.response.write(content)

class AutoRedirect(webapp2.RequestHandler):
    def get(self):
        self.redirect("/blog")

app = webapp2.WSGIApplication([
    ('/', AutoRedirect),
    ('/blog', MainHandler),
    ('/newpost', NewPostHandler),
    webapp2.Route('/blog/<id:\d+>', ViewPostHandler)
], debug=True)
