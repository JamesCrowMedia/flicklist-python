import webapp2


header = """
<!DOCTYPE html>
<html>
<head>
    <title>FlickList</title>
</head>
    <body>
    <h1>FlickList</h1>
"""

footer = """
    </body>
</html>
"""

class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):
        form = """
        <h3>Edit My Watchlist</h3>

        <form action="/add" method="post">
            <label>I would like to add
                <input type="text" name="new-movie" />
                to my watchlist.
            </label>
            <input type="submit" value="Add it" />
        </form>"""

        content = header + form + footer
        self.response.write(content)


class AddMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """
    def get(self):
        self.response.write(header + "<p>Go home</p>" + footer)

    def post(self):
        moviename = self.request.get("new-movie")

        addedmovie = "<strong>" + moviename + "</strong> has been added to your list."

        content = header + addedmovie + footer
        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddMovie)
], debug=True)
