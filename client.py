# # # # # # # # # # # # # # # # # # # # 
# Distributed Systems, final project:
# Author: Miika Pynttäri
# Course: CT30A3401 Distributed Systems
# Assignment: Wikipedia crawler, client-side



# sources used listed on the server.py file


from time import time
import xmlrpc.client


# connecting to the server-side

proxy = xmlrpc.client.ServerProxy("http://localhost:8000/", allow_none=True)


# running main-loop

def run_UI():
    print(f'\n  -- WIKIPEDIA CRAWLER --  \n')
    print(f' This is a program to find the shortest path\n '
            'between two wikipedia articles supplied by you.\n')
    
    while True:
        source = input(' Give a starting article: ')
        target = input(' Give the ending article: ')
        
        
        # checking for empty strings
        
        if (len(source) == 0 or len(target) == 0):
            print(f'\n ** Empty strings are not proper articles.\n')
            continue
        
        
        # validating the articles
        
        startArticle = proxy.validateArticle(source)
        endArticle = proxy.validateArticle(target)
        
        
        # error handling for incorrect articles
        
        if startArticle == False and endArticle == False:
            print(f'\n   Both articles are invalid, try again!\n')
            continue
        elif startArticle == False:
            print(f'\n   Starting article \'{source}\' is not valid, try again.\n')
            continue
        elif endArticle == False:
            print(f'\n   Ending article \'{target}\' is not valid, try again.\n')
            continue
        
        
        # timing for the duration of the function execution
        
        else:
            start_time = time()
            
            print(f'\n  ::: Starting the program ... \n')
            
            
            # returning if both given articles are the exact same
            
            if (source == target):
                end_time = time()
                print(f'Both articles are the same.')
                print(f'Shortest path is the page itself:')
                print(f'{source}')
                print(f'\nTime taken to find the shortest path: {end_time - start_time} seconds.')
                print(f'\n  ::: Exiting ...\n')
                return
            
            
            # calling the main pathfinding function
                
            else:
                result = proxy.findShortestPath(source, target)
                
                end_time = time()
                
                print(f'Shortest path found!')
                print(f'{result}')
                print(f'\nTime taken to find the shortest path: {round((end_time - start_time), 2)} seconds.')
                print(f'\n  ::: Exiting ...\n')
                return
    
    
    
    
if __name__ == "__main__":
    try:
        run_UI()
        
        
     # error handling   
        
    except xmlrpc.client.Fault as error:
        print(f'  Fault error:\n  fault code: {error.faultCode}\n  fault string:  {error.faultString}')
    except xmlrpc.client.ProtocolError as error:
        print(f'  Protocol error:\n  URL: {error.url}\n  headers: {error.headers}\n  errcode: {error.errcode}\n  errmsg: {error.errmsg}')
    except ConnectionError as error:
        print(f'\n  Connection error: {error}')