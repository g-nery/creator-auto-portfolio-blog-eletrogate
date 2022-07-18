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
import sqlite3
import json
from datetime import datetime

sys.path.append('pyFiles/DataModels/')

from DataModels.PostData import *
from DataModels.NavigationPage import *
from DataModels.Posts import *

from sqlalchemy.orm import sessionmaker



class BlogAnalytics:
    def __init__(self):
        self.blogInfo = BlogInformation()
        self.engine = create_engine("sqlite:///database.db")
        
        Session = sessionmaker(bind=self.engine)
        session = Session()
        
        postsPerPage = 8

        templateAdress = f'https://blog.eletrogate.com/wp-json/wp/v2/posts?_embed&per_page={postsPerPage}&page={{}}'
        
        initialAdress = templateAdress.format(1)
        response  = requests.get(initialAdress)
        header = response.headers
        self.listJsonWpData = [response.content]
        countTotalPages = int( header.get("X-WP-TotalPages") )
        
        urls = []
        for i in range(2, countTotalPages + 1):
            urls.append(templateAdress.format(i))
        
        self.listJsonWpData.extend(asyncio.get_event_loop().run_until_complete(self.getPages(urls)))
        
        listPosts = []
        id = 1
        for jsonWp in self.listJsonWpData:
            dicts = json.loads(jsonWp)
            
            for dict in dicts:
                post = Posts()
                post.id = id
                post.idWp = dict['id']
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
                session.add(post)
                id = id + 1
                
                pass
        try:
            session.commit()
        except Exception as e:
            pass
        session.rollback()
        allPosts = session.query(Posts).all()
        # teste = json.loads(self.listJsonWpData[0])
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

    def _updateNextAndPrevPage(self, navigation, header):
        listPages = header.get("Link").split(',')
        dictNavigation = {}
        for page in listPages:
            anPage = page.split(";")
            link = anPage[0].split("<")[1].split(">")[0]
            relWord = anPage[1].split("\"")[1].split("\"")[0]
            dictNavigation[relWord] = link
        try:
            navigation.nextPageLink = dictNavigation["next"]
            navigation.nextPageNumber = navigation.pageNumber + 1
        except: pass
            
        try:
            navigation.previousPageLink = dictNavigation["prev"]
            navigation.previousPageNumber = navigation.pageNumber -1
        except: pass

    def _updatePostsData(self, navigation, content):
        listPages = header.get("Link").split(',')
        dictNavigation = {}
        for page in listPages:
            anPage = page.split(";")
            link = anPage[0].split("<")[1].split(">")[0]
            relWord = anPage[1].split("\"")[1].split("\"")[0]
            dictNavigation[relWord] = link
        try:
            navigation.nextPageLink = dictNavigation["next"]
            navigation.nextPageNumber = navigation.pageNumber + 1
        except: pass
            
        try:
            navigation.previousPageLink = dictNavigation["prev"]
            navigation.previousPageNumber = navigation.pageNumber -1
        except: pass

if __name__ == "__main__":
    analytics = BlogAnalytics()
    pass