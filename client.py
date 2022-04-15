# # # # # # # # # # # # # # # # # # # # 
# Distributed Systems, final project:
# Author: Miika Pynttäri
# Course: CT30A3401 Distributed Systems
# Assignment: Wikipedia crawler, client-side



# sources used listed on the server.py file


from time import time
import xmlrpc.client


proxy = xmlrpc.client.ServerProxy("http://localhost:8000/", allow_none=True)


def run_UI():
    print(f'\n  -- WIKIPEDIA CRAWLER --  \n')
    print(f' This is a program to find the shortest path\n '
            'between two wikipedia articles supplied by you.\n')
    
    while True:
        s = input(' Give a starting article: ')
        e = input(' Give the ending article: ')
        
        startArticle = proxy.validateArticle(s)
        endArticle = proxy.validateArticle(e)
        
        if startArticle == False and endArticle == False:
            print(f'\n   Both articles are invalid, try again!\n')
            continue
        elif startArticle == False:
            print(f'\n   Starting article \'{s}\' is not valid, try again.\n')
            continue
        elif endArticle == False:
            print(f'\n   Ending article \'{e}\' is not valid, try again.\n')
            continue
        
        else:
            start_time = time()
            
            print(f'\n  ::: Starting the program ... \n')
            
            if (s == e):
                end_time = time()
                print(f'Both articles are the same.')
                print(f'Shortest path is the page itself:')
                print(f'{s}')
                print(f'\nTime taken to find the shortest path: {end_time - start_time} seconds.\n')
                print(f'\n  ::: Exiting ...\n')
                return
                
            else:
                result = proxy.findShortestPath(s, e)
                
                end_time = time()
                
                print(f'Shortest path found!')
                print(f'{result}')
                print(f'\nTime taken to find the shortest path: {round((end_time - start_time), 2)} seconds.\n')
                print(f'\n  ::: Exiting ...\n')
                return
    
if __name__ == "__main__":
    try:
        run_UI()
    except xmlrpc.client.Fault as error:
        print(f'  Fault error: {error.faultString}')
    except xmlrpc.client.ProtocolError as error:
        print(f'  Protocol error:\nURL: {error.url}\nheaders: {error.headers}\nerrcode: {error.errcode}\nerrmsg: {error.errmsg}')
    except ConnectionError as error:
        print(f'\n  Connection error: {error}')