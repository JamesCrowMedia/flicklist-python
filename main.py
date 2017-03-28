import webapp2
import cgi

# html boilerplate for the top of every page
page_header = """
<!DOCTYPE html>
<html>
<head>
    <title>FlickList</title>
    <style type="text/css">
        html {
            width: 100%;
            text-align: center;
            background-color: #C7C7C7;
            font-family: Verdana, sans-serif;
        }
        article {
            background-color: #fff;
            width: 580px;
            height: 300px;
            margin: auto;
            margin-top: 20%;
        }

        h1 {
            font-size: 40px;
            padding-top: 40px;
            margin-bottom: .20em;
        }

        h1 a {
            text-decoration: none;
            color: #000;
        }

        h1 a:hover {
            color: #737373;
        }

        h3 {
            font-size: 20px;
            font-weight: 200;
            margin-bottom: 1em;
            padding: 5px;
            }
        form {
            display: block;
            width: 480px;
            height: 40px;
            padding: 0 10px;
            margin: 0 auto 10px auto;
            background-color: #F9F9F9;
            border-top:		1px solid #A1A1A1;
        	border-left:	1px solid #A1A1A1;
        	border-right:	1px solid #424242;
        	border-bottom:	1px solid #424242;
        }

        label {
            display: inline-block;
            font-size: 12px;
            margin: 10px 0 10px 0;
            float: left;

        }

        .submit {
            border-top:		2px solid #A1A1A1;
        	border-left:	2px solid #A1A1A1;
        	border-right:	2px solid #424242;
        	border-bottom:	2px solid #424242;
        	padding:		5px 10px !important;
        	font-size:		12px !important;
        	background-color:	#fff;
        	font-weight:	bold;
        	color:			#000;
            float: right;
            margin-top: 6px;
        }

        .submit:hover {
                background-color: #D0CBCB;
            }

        .submit:active {
            background-color: #000;
            color: #fff;
        }

        .error {
            color: red;
        }

        .goHome {
            display: block;
            margin-top: 4em;
        }

        a {
            text-decoration: none;
            color: #303030;
        }

        a:hover {
            color: #737373;
        }
    </style>
</head>
<body>
    <article>
        <h1>
            <a href="/">FlickList</a>
        </h1>
"""

# html boilerplate for the bottom of every page
page_footer = """
</article>
</body>
</html>
"""


# a list of movies that nobody should be allowed to watch
terrible_movies = [
    "Gigli",
    "Star Wars Episode 1: Attack of the Clones",
    "Paul Blart: Mall Cop 2",
    "Nine Lives"
]

goHome = '<a class="goHome" href="/">Click to return home</a>'


def getCurrentWatchlist():
    """ Returns the user's current watchlist """

    # for now, we are just pretending
    return [ "Star Wars", "Minions", "Freaky Friday", "My Favorite Martian" ]

def getDoNotWatchList():
    return terrible_movies


class Index(webapp2.RequestHandler):
    """ Handles requests coming in to '/' (the root of our site)
        e.g. www.flicklist.com/
    """

    def get(self):

        edit_header = "<h3>Edit My Watchlist</h3>"

        # a form for adding new movies
        add_form = """
        <form action="/add" method="post">
            <label>
                I want to add
                <input type="text" name="new-movie"/>
                to my watchlist.
            </label>
            <input type="submit" class="submit" value="Add It"/>
        </form>
        """

        # a form for crossing off movies
        # (first we build a dropdown from the current watchlist items)
        crossoff_options = ""
        for movie in getCurrentWatchlist():
            crossoff_options += '<option value="{0}">{0}</option>'.format(movie)

        crossoff_form = """
        <form action="/cross-off" method="post">
            <label>
                I want to cross off
                <select name="crossed-off-movie"/>
                    {0}
                </select>
                from my watchlist.
            </label>
            <input type="submit" class="submit" value="Cross It Off"/>
        </form>
        """.format(crossoff_options)

        # if we have an error, make a <p> to display it
        error = self.request.get("error")
        if error:
            error_esc = cgi.escape(error, quote=True)
            error_element = '<p class="error">' + error_esc + '</p>'
        else:
            error_element = ''

        # combine all the pieces to build the content of our response
        main_content = edit_header + add_form + crossoff_form + error_element
        content = page_header + main_content + page_footer
        self.response.write(content)


class AddMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/add'
        e.g. www.flicklist.com/add
    """

    def post(self):
        # look inside the request to figure out what the user typed
        new_movie = self.request.get("new-movie")

        # TODO 2
        # if the user typed nothing at all, redirect and yell at them
        if new_movie == '':
            error = "You have to add a movie to add a movie."
            self.redirect("/?error=" + error)
        # TODO 3
        # if the user wants to add a terrible movie, redirect and yell at them
        elif new_movie in getDoNotWatchList():
            error = "You don't want to watch {0}, I promise.".format(new_movie)
            self.redirect("/?error=" + error)

        # TODO 1
        # 'escape' the user's input so that if they typed HTML, it doesn't mess up our site
        # build response content
        new_movie_esc = cgi.escape(new_movie, quote=True)

        new_movie_element = "<strong>" + new_movie_esc + "</strong>"
        sentence = new_movie_element + " has been added to your Watchlist!"
        content = page_header + "<p>" + sentence + "</p>" + goHome + page_footer
        self.response.write(content)


class CrossOffMovie(webapp2.RequestHandler):
    """ Handles requests coming in to '/cross-off'
        e.g. www.flicklist.com/cross-off
    """

    def post(self):
        # look inside the request to figure out what the user typed
        crossed_off_movie = self.request.get("crossed-off-movie")

        if (crossed_off_movie in getCurrentWatchlist()) == False:
            # the user tried to cross off a movie that isn't in their list,
            # so we redirect back to the front page and yell at them

            # make a helpful error message
            error = "'{0}' is not in your Watchlist, so you can't cross it off!".format(crossed_off_movie)

            # redirect to homepage, and include error as a query parameter in the URL
            self.redirect("/?error=" + error)

        # if we didn't redirect by now, then all is well
        crossed_off_movie_element = "<strike>" + crossed_off_movie + "</strike>"
        confirmation = crossed_off_movie_element + " has been crossed off your Watchlist."
        content = page_header + "<p>" + confirmation + "</p>"+ goHome + page_footer
        self.response.write(content)


app = webapp2.WSGIApplication([
    ('/', Index),
    ('/add', AddMovie),
    ('/cross-off', CrossOffMovie)
], debug=True)
