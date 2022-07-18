import sys
# sys.path.append('pyFiles/DataModels/')
from PostData import *


class NatigationPage:
    def __init__(self):
        self.previousPageNumber = None
        self.previousPageLink = None

        self.nextPageNumber = None
        self.nextPageLink = None

        self.pageNumber = None
        self.pageLink = None
        self.pagePosts = []

        

class BlogInformation:
    def __init__(self):
        self.countTotalPages = None
        self.postsPerPage = None