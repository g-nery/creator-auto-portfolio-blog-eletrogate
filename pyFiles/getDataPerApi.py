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
        adress = 'https://blog.eletrogate.com/wp-json/wp/v2/posts?_embed&per_page=8&page=2'
        response  = requests.get(adress)
        header = response.headers
        totalPages = header.get("X-WP-TotalPages")

        self.dictRelPage = self._updateDictRelPage(header)
        response  = requests.get(self.dictRelPage['next'])
        header = response.headers
        self.dictRelPage = self._updateDictRelPage(header)

        pass
    
    def _updateDictRelPage(self, header):
        listPages = header.get("Link").split(',')
        dictRelPage = {}
        for page in listPages:
            anPage = page.split(";")
            link = anPage[0].split("<")[1].split(">")[0]
            relWord = anPage[1].split("\"")[1].split("\"")[0]
            dictRelPage[relWord] = link
        return dictRelPage

if __name__ == "__main__":
    analytics = BlogAnalytics()
    pass