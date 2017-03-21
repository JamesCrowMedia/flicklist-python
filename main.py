import webapp2
import random

class Index(webapp2.RequestHandler):

    def getRandomMovie(self):

        movieList = ["The Fast and the Furious", "2 Fast 2 Furious", "Fast & Furious", "Fast 5", "Fast & Furious 6", "The Fast and the Furious: Tokyo Drift", "Furious 7"]

        return movieList[random.randrange(0, len(movieList))]

    def get(self):
        # choose a movie by invoking our new function
        movie = self.getRandomMovie()
        tomorrow_movie = self.getRandomMovie()
        # build the response string
        content = "<h1>Movie of the Day</h1>"
        content += "<p>" + movie + "</p>"

        # TODO: pick a different random movie, and display it under
        # the heading "<h1>Tommorrow's Movie</h1>"
        content += "<h1>Tomorrow's Movie</h1>"
        content += "<p>" + tomorrow_movie + "</p>"

        self.response.write(content)

app = webapp2.WSGIApplication([
    ('/', Index)
], debug=True)
