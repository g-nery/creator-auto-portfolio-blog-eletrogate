import requests
from bs4 import BeautifulSoup


class BlogEletrogate:
    
    def __init__(self):
        # file = open("mainPage.html","r")
        totalRequests = 0
        totalPages = 1
        paginaRequerida = 1
        firstTime = True

        while(totalRequests < totalPages):     
            linkRequest = "https://blog.eletrogate.com/page/{}"

            file = requests.get(linkRequest.format(paginaRequerida))
            file = file.content 

            self.mainPage = file
            self.soup = BeautifulSoup(self.mainPage, "html.parser")

            sectionListPost = self.soup.find(class_ = 'list-post')

            if(firstTime == True):
                pageNumbers = self.soup.find_all(class_ = "page-numbers")
                totalPages = int(pageNumbers[4].contents[0])
                firstTime = False
                print(totalPages)


            list2 = sectionListPost.find_all(class_ = "col-md-11 d-none d-md-block")

            list3 = []

            
            for i in list2:
                l = i.find( "a", href = True)
                j = l.find(class_ = "item-atuacao" )
                j.decompose()
                k = l.get("href")
                print(k)


                # print(i)
            
            # print(list3)
            # list2.find_all_next()

            # print(self.soup.prettify())
            self.linkPosts = []
            totalRequests += 1
            paginaRequerida += 1
        

    def getLinkPosts(self):
        # d = [type(item) for item in list(self.soup.children)]
        # print(d)
        # html = list(self.soup.children)[4]
        # # print(html)
        # html2 = list(html.children)[0]
        # print(html2)
        pass


if __name__ == '__main__':
    blogEletrogate = BlogEletrogate()
    blogEletrogate.getLinkPosts()