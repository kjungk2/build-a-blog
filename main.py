import webapp2
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                        autoescape = True)

class MainHandler(webapp2.RequestHandler):
    def get(self):
        t = jinja_env.get_template("base.html")
        content = t.render()
        self.response.write(content)

    def post(self):
        new_post = self.request.get("new_post")
        if new_post:
            self.response.write("thanks for the new post")
        else:
            self.response.write("you didn't type anything!")

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
