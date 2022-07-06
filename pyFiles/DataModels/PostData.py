from msilib.schema import Property
import string

class PostData:
    def __init__(   self, 
                    id = None,
                    title = None, 
                    thumbImage= None, 
                    description = None, 
                    publishDate = None, 
                    link = None, 
                    author=None, 
                    categories = None,
                    comments = None,
                    numberViews = None,
                    pageAuthority = None):

        self._thumbImage = thumbImage
        self._description = description
        self._publishDate = publishDate
        self._link = link
        self._author = author
        self._title = title
        self._categories = categories
        self._numberComments = comments
        self._numberViews = numberViews
        self._pageAuthority = pageAuthority
        self._id = id

    @property
    def thumbImage(self):
        return self._thumbImage

    @thumbImage.setter
    def thumbImage(self, newValue):
        if(type(newValue) is str ):
            self._thumbImage = newValue

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, newValue):
        if(type(newValue) is str ):
            self._description = newValue

    @property
    def publishDate(self):
        return self._publishDate

    @publishDate.setter
    def publishDate(self, newValue):
        if(type(newValue) is str ):
            self._publishDate = newValue

    @property
    def link(self):
        return self._link

    @link.setter
    def link(self, newValue):
        if(type(newValue) is str ):
            self._link = newValue

    @property
    def author(self):
        return self._author

    @author.setter
    def author(self, newValue):
        if(type(newValue) is str ):
            self._author = newValue

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, newValue):
        if(type(newValue) is str ):
            self._title = newValue

    @property
    def categories(self):
        return self._categories

    @categories.setter
    def categories(self, newValue):
        if(type(newValue) is str ):
            self._categories = newValue

    @property
    def numberComments(self):
        return self._numberComments

    @numberComments.setter
    def numberComments(self, newValue):
        if(type(newValue) is str ):
            self._numberComments = newValue

    @property
    def numberViews(self):
        return self._numberViews

    @numberViews.setter
    def numberViews(self, newValue):
        if(type(newValue) is str ):
            self._numberViews = newValue
            
    @property
    def pageAuthority(self):
        return self._pageAuthority

    @pageAuthority.setter
    def pageAuthority(self, newValue):
        if(type(newValue) is str ):
            self._pageAuthority = newValue
            
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, newValue):
        if(type(newValue) is str ):
            self._id = newValue


if __name__ == '__main__':
    postData = PostData()
    postData.description = "Description"
    postData.link = "www.eletrogate.com"
    postData.publishDate = "12 jun"
    postData.thumbImage = "algum link"
    pass