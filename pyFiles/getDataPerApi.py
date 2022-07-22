# Essa classe retorna uma lista de links de posts de um determinado autor
from multiprocessing import Pool, Process
import re
from xmlrpc.client import Boolean
from bs4 import BeautifulSoup
import requests
import time
import os
import sys
import asyncio
import aiohttp
import sqlite3
import json
from datetime import datetime

sys.path.append('pyFiles/DataModels/')

from DataModels.PostData import *
from DataModels.NavigationPage import *
from DataModels.Posts import *

from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils.functions import database_exists



class BlogAnalytics:
    def __init__(self):
        self._dictBufferPages = {}
        self._session = self._createSessionOnDB()
        
        self.updateTablePosts()
        
        listPosts = []
        id = 1
        for jsonWp in self.listJsonWp:
            listDicts = json.loads(jsonWp)
            
            for dict in listDicts:
                post = Posts()
                post.id = dict['id']
                post.categoriesWp = json.dumps(dict['categories'])
                post.publishDate = datetime.strptime(dict['date'], '%Y-%m-%dT%H:%M:%S')
                try:
                    post.description = dict['yoast_head_json']['og_description']
                except: pass
                try:
                    post.thumbLink = dict['yoast_head_json']['og_image'][0]['url']
                except: 
                    try:
                        post.thumbLink = dict['yoast_head_json']['twitter_image']
                    except:
                        pass
                post.title = dict['yoast_head_json']['title']
                post.urlPost = dict['yoast_head_json']['og_url']
                listPosts.append(post)
                self.session.add(post)
                pass
        try:
            self.session.commit()
        except Exception as e:
            pass
        self.session.rollback()
        allPosts = self.session.query(Posts).get(2494)
        # teste = json.loads(self.listJsonWpData[0])
    
    def _createSessionOnDB(self):
        self._engine = create_engine("sqlite:///database.db")
        Session = sessionmaker(bind=self._engine)
        session = Session()
        return session
    
    def _getTemplateURL(self):
        self._postsPerPage = 12
        templateURL = f'https://blog.eletrogate.com/wp-json/wp/v2/posts?_embed&per_page={self._postsPerPage}&page={{}}'
        return templateURL
    
    def _fillAllDictBuffer(self):
        initialAdress = self._getTemplateURL().format(1)
        response  = requests.get(initialAdress)
        header = response.headers
        
        listJsonWp = [response.content]
        countTotalPages = int( header.get("X-WP-TotalPages") )
        
        urls = []
        for i in range(2, countTotalPages + 1):
            urls.append(self._getTemplateURL().format(i))
        
        listJsonWp.extend(asyncio.get_event_loop().run_until_complete(self.getPages(urls)))
        
        for i in range(len(listJsonWp)):
            self._dictBufferPages[i + 1] = listJsonWp[i]
    
    def _fillDictBufferBetweenPages(self, initialPage, finalPage):
        initialAdress = self._getTemplateURL().format(1)
        response  = requests.get(initialAdress)
        header = response.headers
        
        listJsonWp = [response.content]
        
        urls = []
        for i in range(initialPage, finalPage + 1):
            urls.append(self._getTemplateURL().format(i))
        
        listJsonWp.extend(asyncio.get_event_loop().run_until_complete(self.getPages(urls)))
        
        for i in range(len(listJsonWp)):
            self._dictBufferPages[i + 1] = listJsonWp[i]
    
    ''' 
    Este método recebe a lista de dicionários que foi desserializada e inclui no banco de dados
    Retorna True caso tenha encontrado o primeiro post que estava no banco de dados
    '''
    def _processAndIncludeOnDatabase(self, listDictsPosts) -> Boolean:
        for dictPost in listDictsPosts:
            containDB = self._session.query(Posts).get(dictPost['id'])
            if(containDB != None):
                return True
            post = Posts()
            post.id = dictPost['id']
            post.categoriesWp = json.dumps(dictPost['categories'])
            post.publishDate = datetime.strptime(dictPost['date'], '%Y-%m-%dT%H:%M:%S')
            try:
                post.description = dictPost['yoast_head_json']['og_description']
            except: pass
            try:
                post.thumbLink = dictPost['yoast_head_json']['og_image'][0]['url']
            except: 
                try:
                    post.thumbLink = dictPost['yoast_head_json']['twitter_image']
                except:
                    pass
            post.title = dictPost['yoast_head_json']['title']
            post.urlPost = dictPost['yoast_head_json']['og_url']
            self._session.add(post)
        return False
    
    def updateTablePosts(self):
        total = self._session.query(Posts).all()
        initialURL = self._getTemplateURL().format(1)
        response  = requests.get(initialURL)
        header = response.headers
        content = response.content
        listDictsPosts = json.loads(content)
        
        if(self._processAndIncludeOnDatabase(listDictsPosts)):
            self._session.commit()
            return
        
        countTotalPages = int( header.get("X-WP-TotalPages") )
        
        for i in range(2, countTotalPages + 1):
            url = self._getTemplateURL().format(i)
            response  = requests.get(url)
            header = response.headers
            content = response.content
            listDictsPosts = json.loads(content)
            if(self._processAndIncludeOnDatabase(listDictsPosts)):
                break
                
        self._session.commit()
        return
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

    


if __name__ == "__main__":
    analytics = BlogAnalytics()
    pass