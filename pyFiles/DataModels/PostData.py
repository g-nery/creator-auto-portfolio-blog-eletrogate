from msilib.schema import Property
import string

class PostData:
    def __init__(self):

        self.id = None
        self.idBlog = None
        self.link = None
        self.title = None
        self.description = None
        self.thumbImage = None
        self.author = None
        self.publishDate = None
        self.categories = None
        self.numberComments = None
        
        self.numberViews = None
        self.pageAuthority = None
        

if __name__ == '__main__':
    postData = PostData()
    postData.description = "Description"
    postData.link = "www.eletrogate.com"
    postData.publishDate = "12 jun"
    postData.thumbImage = "algum link"
    pass