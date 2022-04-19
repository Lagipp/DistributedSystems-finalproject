# # # # # # # # # # # # # # # # # # # # 
# Distributed Systems, final project:
# Author: Miika Pynttäri
# Course: CT30A3401 Distributed Systems
# Assignment: Wikipedia crawler, server-side
# key: value    



# SOURCES USED:
#   https://www.geeksforgeeks.org/how-to-scrape-multiple-pages-of-a-website-using-python/
#   https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/
#   https://www.mediawiki.org/wiki/API:Links
#   https://www.mediawiki.org/wiki/API:Query
#   https://docs.python.org/3/library/concurrent.futures.html 
#   https://testdriven.io/blog/building-a-concurrent-web-scraper-with-python-and-selenium/ 
#   https://stackoverflow.com/questions/51445418/how-do-i-build-a-basic-web-crawler-for-wikipedia-pages-to-gather-links 
#   https://stackoverflow.com/questions/53621682/multi-threaded-xml-rpc-python3-7-1 
#   https://stackoverflow.com/questions/10569438/how-to-print-unicode-character-in-python 
#   https://www.geeksforgeeks.org/python-map-function/ 
#   https://docs.python.org/3/library/xmlrpc.server.html 
#   https://en.wikipedia.org/wiki/Arrow_(symbol)
#   https://stackoverflow.com/questions/20457038/how-to-round-to-2-decimals-with-python 
#   https://www.youtube.com/watch?v=aA6-ezS5dyY 
#   https://betterprogramming.pub/asynchronous-tasks-in-python-with-the-concurrent-futures-module-7325dc555d 
#   https://www.youtube.com/watch?v=0NNV8FDuck8 
#  + other random mindless surfing in bed relating to the subject


import concurrent.futures
from socketserver import ThreadingMixIn
from xmlrpc.client import Fault
from xmlrpc.server import SimpleXMLRPCServer

import requests

S = requests.Session()
URL = "https://en.wikipedia.org/w/api.php"


# NOTE: using the english wikipedia when scraping for
# the function to work, use 2 proper en.wikipedia.org articles


# Checking that the page given is a valid wikipedia article

def validateArticle(title):
    
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": title,
        "prop": "links",
        "pllimit": "max",
    }
    
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["pages"]
    
    
    # if the mediawiki.query query returns "-1", 
    # nothing was found --> article is bad
    
    if "-1" in PAGES:
        print(f'\nInvalid article \'{title}\'')
        return False
    
    print(f'article \'{title}\' = oukkidouk :-D')
    return True



# saving the path from found links to an array

def savePath(articleTitle, currentPath):
    
    found = []
    
    PARAMS = {
        "action": "query",
        "format": "json",
        "titles": articleTitle,
        "prop": "links",
        "pllimit": "max",
    }
    
    R = S.get(url=URL, params=PARAMS)
    DATA = R.json()
    PAGES = DATA["query"]["pages"]
    
    
    # checking only valid links
    
    if "-1" not in PAGES:
        for k, v in PAGES.items():
            for l in v["links"]:
                found.append([l["title"], currentPath + " \u21B7  " + l["title"]])
    
    
    # looping if we can go further
    
    while 'continue' in DATA:
        PARAMS = {
            "action": "query",
            "format": "json",
            "titles": articleTitle,
            "prop": "links",
            "pllimit": "max",
            "plcontinue": DATA["continue"]["plcontinue"]
        }
        
        R = S.get(url=URL, params=PARAMS)
        DATA = R.json()
        PAGES = DATA["query"]["pages"]
        
        
        # appending only valid links
        
        if "-1" not in PAGES:
            for k, v in PAGES.items():
                for l in v["links"]:
                    found.append([l["title"], currentPath + " \u21B7  " + l["title"]])
    
    
    print(f'Found {len(found)} links.')
    
    
    # returning the array of found links
    
    return found



# function to run multiple workers in parallel using concurrent.futures library

def runInParallel(inputArr, endArticle):
    tempArr = []
    
    for i in range(0, len(inputArr), 10):
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:

            args = ((inputArr[k][0], inputArr[k][1]) for k in range(i, i+9))
            
            for out in executor.map(lambda m: savePath(*m), args):
                tempArr = tempArr + out
                    
        articles = [elem[0] for elem in tempArr]
        
        
        # checking to see if we found the end article
        
        for j in range(len(articles)):
            if articles[j].lower() == endArticle.lower():
                print(f'{tempArr[j][1]}')
                target = tempArr[j][1]
                
                return target, "end article found!"
    
    return tempArr, "couldn't find end article."



# function to loop over until we find the shortest path between articles

def findShortestPath(startArticle, endArticle):
    
    currentPath = startArticle
    startingArr = savePath(startArticle, currentPath)
    
    while len(startingArr) == 1:
        startingArr = savePath(startingArr[0][0], startingArr[0][1])
    
    
    # (while true :-D)
    # if the parallel function found something, stop
    # if not, loop over and keep going
        
    while (1 == 1):
        result, message = runInParallel(startingArr, endArticle)
        
        if message == "end article found!": return result
        else: startingArr = result
        



# running the server-side and registering the functions to the client

# https://stackoverflow.com/questions/53621682/multi-threaded-xml-rpc-python3-7-1

class SimpleThreadedXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    pass

def runServer(host="localhost", port=8000):
    serverAddr = (host, port)
    server = SimpleThreadedXMLRPCServer(serverAddr)
    
    server.register_function(findShortestPath)
    server.register_function(savePath)
    server.register_function(runInParallel)
    server.register_function(validateArticle)
    
    print(f'\nServer started...')
    print(f'Listening on {host} port {port}.\n')
    
    server.serve_forever()
    
if __name__ == "__main__":
    runServer()
