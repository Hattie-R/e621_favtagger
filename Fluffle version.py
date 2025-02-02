#This is the faster version that uses Fluffle (https://fluffle.xyz/) to find the image on the e621
#It skips the videos in the chosen folder

import io
import os
import shutil
import urllib
import requests
from PIL import Image
from requests import post


def getting_files():
    dir = input("Enter the directory: ")
    os.chdir(dir)
    images = os.listdir()
    print('We found ' + str(len(images)) + ' files')

def video_check(files_list):
    for y in files_list:
        if y.split(".")[-1] == "mp4" or y.split(".")[-1] == "MP4" or y.split(".")[-1] == "webm":
            files_list.remove(y)

def calculate_size(width, height, target):
    def calculate_size(d1, d2, d1_target): return round(d1_target / d1 * d2)

    if width > height:
        return calculate_size(height, width, target), target

    return target, calculate_size(width, height, target)

def download_image(url):
    response = requests.get(url + ".json", headers = {'user-agent': 'hydrusBatchSauce/corposim'}, auth=requests.auth.HTTPBasicAuth(username, api))
    if response.status_code == 200:
        post_id = response.json()["post"]['id']
        artist = response.json()["post"]["tags"]["artist"][0]
        post_image = response.json()["post"]["file"]["url"]
        file_name = artist + "_" + str(post_id) + "." + post_image.split('.')[-1]
        urllib.request.urlretrieve(post_image, file_name)
        print("\tImage downloaded successfully.\n")
        return file_name
    else:
        print(f"Failed to download image. Status code: {response.status_code}")

def favorite_post(id, USERNAME, API_KEY):
    headers = {'user-agent': 'hydrusBatchSauce/corposim'}
    auth = requests.auth.HTTPBasicAuth(USERNAME, API_KEY)
    requests.post(url="https://e621.net/favorites.json", auth=auth, headers=headers, json={ "post_id": id })

def is_deleted_e621(url):
    response = requests.get(url + ".json", headers = {'user-agent': 'hydrusBatchSauce/corposim'}, auth=requests.auth.HTTPBasicAuth(username, api))
    if response.status_code == 200:
        isdeleted = response.json()["post"]["flags"]["deleted"]
        if isdeleted == True:
            return True
        else:
            return False
def look_in_FA():
    second_json_data = post("https://api.fluffle.xyz/v1/search", headers=headers, files=files, data = {"includeNsfw": True,"platforms": ["fur affinity"],"limit": 8}).json()
    print("\tFA: " + str(second_json_data["results"][0]["location"]) + "    " + str(round(second_json_data["results"][0]["score"]*100))+ "%")
    if round(second_json_data["results"][0]["score"]*100) >= 95:
        pass

def main():
    return 0

print("DISCLAIMER:\n\nThis is the faster version that uses Fluffle (https://fluffle.xyz/) to find the image on the e621 \nProblem may occure when the file is a video\nThis version DOES NOT substitutes the original file\n")
dir = input(r'Directory: ')
username = input("Enter e621 username: ")
api = input("Enter the API key: ")
os.chdir(dir)
image_list = os.listdir()
print('We found ' + str(len(image_list)) + ' files\n')
counter = 1

video_check(image_list)

os.mkdir("e621")
found_e621 = []

for i in image_list:
    # Preprocess the image as per Fluffle its documentation
    
    image = Image.open(i)
    width, height = image.size

    image.thumbnail(calculate_size(width, height, 256))
    buffer = io.BytesIO()
    image.save(buffer, "png")

    # And then reverse search the preprocessed image
    headers = {"User-Agent": "Fluffle Batch search (by hattie_ragales on Twitter)"}
    files = {"file": buffer.getvalue()}
    data = {
        "includeNsfw": True,
        "platforms": ["e621"],
        "limit": 8
    }

    json_data = post("https://api.fluffle.xyz/v1/search", headers=headers, files=files, data=data).json()
    
    res1 = []
    for g in range(1):
        res1.append(json_data["results"][g]["location"]) 
    print(str(counter) + ". ", json_data["results"][g]["location"], str(round(json_data["results"][g]["score"]*100)) + "%")
    ids = json_data["results"][g]["location"].split("/")[-1]
    
    if json_data["results"][g]["score"]*100 >= 95:
        if is_deleted_e621(json_data["results"][g]["location"]) == False:
            file_name = download_image(json_data["results"][g]["location"])
            favorite_post(ids, username, api)
            os.remove(i)
            image.close()
            shutil.move(dir + "\\" + file_name, dir+'\\e621')
        else:
            print("Warning! The post has been deleted from e621\n")
            look_in_FA()
    else:
        print("\tWarning! Low similarity score!\n")
        look_in_FA()
    counter+=1
    image.close()

if __name__ == "__main__":
    main()