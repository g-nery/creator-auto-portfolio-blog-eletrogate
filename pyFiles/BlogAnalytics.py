# Essa classe retorna uma lista de links de posts de um determinado autor
from multiprocessing import Pool, Process
import re
from bs4 import BeautifulSoup
import requests
import time
import os
import sys
import asyncio
import aiohttp
sys.path.append('pyFiles/DataModels/')

from DataModels.PostData import *



class BlogAnalytics:
    def __init__(self):
        self.mainAdress = "https://blog.eletrogate.com/"
        self.adressPages = "https://blog.eletrogate.com/page/{}"
        self.mainPage  = requests.get(self.mainAdress).content
        self.mainSoup = BeautifulSoup(self.mainPage, "html.parser")
        self.totalPagesOnBlog =None
        self.listInfoPosts = []
        self.listMainPages = [self.mainPage]
        self.listPostsPages = []

        urls = []
        for i in range(2, self.getNumberPagesOnBlog() + 1):
            urls.append(f"https://blog.eletrogate.com/page/{i}")
        # start = time.time()
        pages = asyncio.get_event_loop().run_until_complete(self.getPages(urls))
        self.listMainPages.extend(pages)
        # end = time.time()
        # print(f"Total time: {end - start}")
        pass

    async def requestAsync(self, url, session):
        try:
            async with session.get(url=url) as response:
                resp = await response.read()
                return resp
        except Exception as e:
            print("Unable to get url {} due to {}.".format(url, e.__class__))

    async def getPages(self, urls):
        ret = []
        async with aiohttp.ClientSession() as session:
            ret = (await asyncio.gather(*[self.requestAsync(url, session) for url in urls]))
        return ret
    
    def deleteMainPagesOnMemory(self):
        self.listMainPages.clear()
        del self.listMainPages

    def deletePostPagesOnMemory(self):
        self.listPostsPages.clear()
        del self.listPostsPages
    
    def getAllPosts(self):
        self.listInfoPosts = []
        for page in self.listMainPages:
            soup = BeautifulSoup(page, "html.parser")
            sectionListPost = soup.find(class_ = 'list-post')
            sectionIndividualPost = sectionListPost.find_all(class_ = "col-md-11 d-none d-md-block")
            for postIndividual in sectionIndividualPost:

                infoPost = PostData()
                try: infoPost.link = postIndividual.find( "a", href = True).get("href")
                except: pass
                try: infoPost.title = postIndividual.find(class_ = "title").text
                except: pass
                try: infoPost.description = postIndividual.find(class_ = "text-left").find("p").text
                except: pass
                try: infoPost.publishDate = postIndividual.find(class_ = "date").text.split(' - ')[1]
                except: pass
                try: infoPost.thumbImage = postIndividual.find("img").get("src")
                except: pass
                
                self.listInfoPosts.append(infoPost)

        self.loadPagesPosts()

        for index in range(len(self.listInfoPosts)):
            pagePost = self.listPostsPages[index]
            infoPost = self.listInfoPosts[index]
            soup = BeautifulSoup(pagePost, "html.parser")
            sectionTextPost = soup.find(class_ = 'col-md-9 px-4')
            soup.find
            sectionCommentsPost = soup.find(class_ ='comments-box pt-5')
            sectionAboutAuthor = sectionTextPost.findAll(class_ = "box-blog")[-1]
            try: 
                if(sectionAboutAuthor.find("h2").text.upper() == 'SOBRE O AUTOR'):
                    infoPost.author = sectionAboutAuthor.find("strong").text
                else:
                    infoPost.author = "Sem Autor"
            except: 
                infoPost.author = "Sem Autor"

        # self.deleteMainPagesOnMemory()
        # self.deletePostPagesOnMemory()

        return self.listInfoPosts

    def loadPagesPosts(self):
        urls = []
        for postInfo in self.listInfoPosts:
            urls.append(postInfo.link)
        
        self.listPostsPages = asyncio.get_event_loop().run_until_complete(self.getPages(urls))
        pass

    def getPostsByAuthor(self, authorName):
        if(len(self.listInfoPosts) == 0):
            self.getAllPosts()

        listPostsAuthor = []
        for post in self.listInfoPosts:
            if(post.author == authorName):
                listPostsAuthor.append(post)
        return listPostsAuthor

    def getDictPostsByAuthor(self):
        if(len(self.listInfoPosts) == 0):
            self.getAllPosts()
        
        dictPostsAuthor = {}
        for post in self.listInfoPosts:
            listPost = []
            try:
                listPost.extend(dictPostsAuthor[post.author])
            except: pass
            listPost.append(post)
            dictPostsAuthor[post.author] = listPost

        return dictPostsAuthor

    def countPostsOnBlog(self):
        if(len(self.listInfoPosts) > 0):
            return len(self.listInfoPosts)
        else:
            self.getAllPosts()
            return len(self.listInfoPosts)

    def countPostsByAuthor(self):
        pass
    
    def getNumberPagesOnBlog(self):

        if(self.totalPagesOnBlog == None):
            pageNumberLocation = self.mainSoup.find_all(class_ = "page-numbers")
            listNumbers = []
            for pnum in pageNumberLocation:
                try:
                    listNumbers.append(int(pnum.contents[0]))
                except:
                    pass
                
            if len(listNumbers) > 0:
                listNumbers.sort()
                self.totalPagesOnBlog = listNumbers[-1]
                return self.totalPagesOnBlog
            else:
                return None
        else:
            return self.totalPagesOnBlog

if __name__ == '__main__':
    blogAnalytics = BlogAnalytics()
    allPosts = blogAnalytics.getAllPosts()
    
    dictPosts = blogAnalytics.getDictPostsByAuthor()
    GustavoPosts = dictPosts["Gustavo Nery"]
    pass