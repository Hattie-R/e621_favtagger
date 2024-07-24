import requests
import time
import os
import shutil


def downl_url_and_artist(post_id):
    api_url = f"https://e621.net/posts/{post_id}.json"
    headers = {'user-agent': 'hydrusBatchSauce/corposim'}
    response = requests.get(api_url, headers=headers)

    if response.status_code == 200:
        json_data = response.json()
        image_url = json_data["post"]["file"]["url"]
        artists = json_data["post"]["tags"]["artist"]
        deleted = json_data["post"]["flags"]["deleted"] #checks if the post was deleted or not
        if deleted == 'true':
            print('Post has been deleted, check it yourself')
        return image_url, artists, deleted
    else:
        print(f"Failed to get image URL. Status code: {response.status_code}")
        return None

def download_image(url, id, artist):
    response = requests.get(url)
    if response.status_code == 200:
        with open("{}-{}.{}".format('_'.join(artist), id, url.split('.')[-1]), "wb") as file:
            file.write(response.content)
        print("Image downloaded successfully.\n")
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def favorite_post(id):
    headers = {'user-agent': 'hydrusBatchSauce/corposim'}
    auth = requests.auth.HTTPBasicAuth(USERNAME, API_KEY)
    requests.post(url="https://e621.net/favorites.json", auth=auth, headers=headers, json={ "post_id": id })




                                        # Taking basic info
print("Hello!, may I help you with you yiff collection?\nBut first, I'd like to know where is your collection.\nProvide with smth like C:\\Users\\Hattie Ragales\\user\\yiff")
dir = input(r'Directory: ')
USERNAME = 'hattie_r'                   #INSERT YOUR USERNAME
API_KEY = 'youaresuchanaughtyboy'       #INSERT YOUR API KEY (if you don't know where to get it, read README.md file)
timeout = 5
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
     
        favorite_post(idp)
        Found.append(path)
        url1 = downl_url_and_artist(idp)
        download_image(url1[0], idp, url1[1])

    except:                              #It didn't find
        notFound.append(path)
        if len(list1) > 400:
            print('\'' + path + '\',')
        else:
            print(str(counter) + ". No results for: " + path + '\n')
    time.sleep(timeout)                 #That was made not to load servers too much
    files['file'].close()




os.mkdir('no_e621')
print('Found:' + '\n' + str(Found))
for i in Found:
    os.remove(i)
print('Not Found:' + '\n' + str(notFound))

for i in notFound:
    shutil.move(i, dir+'\\no_e621')
input("\n\nPress Enter to finish")
