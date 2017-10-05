class rating():

    def __init__(self, UserID, MovieID, Rating, Timestamp):
        self.UserID = UserID
        self.MovieID = MovieID
        self.Rating = Rating
        self.Timestamp = Timestamp

    def getUserID(self):
        return self.UserID

    def getMovieID(self):
        return self.MovieID

    def getRating(self):
        return self.Rating

    def getTimestamp(self):
        return self.Timestamp

