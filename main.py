import requests
import time
import os
import shutil
from functions import *

                                        # Taking basic info
print("Hello!, may I help you with you yiff collection?\nBut first, I'd like to know where is your collection.\nProvide with smth like C:\\Users\\Hattie Ragales\\Pictures\\yiff")
dir = input(r'Directory: ')
USERNAME = input("Enter your e621 username: ")    #INSERT YOUR USERNAME
API_KEY = input("Enter your e621 API key (README.md if don't knwo what is it): ")    #INSERT YOUR API KEY (if you don't know where to get it, read README.md file)
timeout = 5                             #Change this if you have too many requests problems
counter = 0
Found = []
notFound = []

                                        #Fetching files
os.chdir(dir)
list1 = os.listdir()
print('We found ' + str(len(list1)) + ' files')

                                        #Autorizing user
url = "https://e621.net/iqdb_queries.json"
headers = {'user-agent': 'hydrusBatchSauce/corposim'}
auth = requests.auth.HTTPBasicAuth(USERNAME, API_KEY)




for path in list1:
    counter+=1
    files = {'file': (open(path, 'rb'))}
    r = requests.post(url, files=files, headers=headers, auth=auth)

    if (r.status_code != 200):
        print("ERR:", r.status_code)
        break
    try:                                #Tries to find
        urls = "https://e621.net/posts/" + str(r.json()[0]['post_id']) + '\n'
        idp = str(r.json()[0]['post_id'])
        print(str(counter) + '. Success for: ' + path + ' : ' + urls)
     
        favorite_post(idp, USERNAME, API_KEY)
        Found.append(path)
        url1 = downl_url_and_artist(idp)
        os.remove(path)
        download_image(url1[0], idp, url1[1])

    except:                              #It didn't find
        notFound.append(path)
        if len(list1) > 400:
            print('\'' + path + '\',')
        else:
            print(str(counter) + ". No results for: " + path + '\n')
    time.sleep(timeout)                 #That was made not to load servers too much
    files['file'].close()



# Sortation of files found and not found on e621
os.mkdir('no_e621')
os.mkdir('e621')
print('Found:' + '\n' + str(Found))
for i in Found:
    shutil.move(i, dir+'\\e621')
print('Not Found:' + '\n' + str(notFound))

for i in notFound:
    shutil.move(i, dir+'\\no_e621')
input("\n\nPress Enter to finish")
