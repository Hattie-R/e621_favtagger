#This is the faster version that uses Fluffle (https://fluffle.xyz/) to find the image on the e621
#Problem may occure when the file is a video
#This version DOES NOT substitutes the original file

import io
import os
from pprint import pprint
from PIL import Image
from requests import post
from functions import favorite_post

print("DISCLAIMER:\n\nThis is the faster version that uses Fluffle (https://fluffle.xyz/) to find the image on the e621 \nProblem may occure when the file is a video\nThis version DOES NOT substitutes the original file\n")
dir = input(r'Directory: ')
username = input("Enter e621 username: ")
api = input("Enter the API key: ")
os.chdir(dir)
image_list = os.listdir()
print('We found ' + str(len(image_list)) + ' files')

for y in image_list:
    if y.split(".")[-1] == "mp4" or y.split(".")[-1] == "MP4" or y.split(".")[-1] == "webm":
        print("!!!This program works only with IMAGES, please replace all the videos in a separete folder!!!")

for i in image_list:
    # Preprocess the image as per Fluffle its documentation
    
    image = Image.open(i)
    width, height = image.size

    #fetching all the files
    def getting_files():
        dir = input("Enter the directory: ")
        os.chdir(dir)
        images = os.listdir()
        print('We found ' + str(len(images)) + ' files')

    def calculate_size(width, height, target):
        def calculate_size(d1, d2, d1_target): return round(d1_target / d1 * d2)

        if width > height:
            return calculate_size(height, width, target), target

        return target, calculate_size(width, height, target)

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
    print(json_data["results"][g]["location"], str(round(json_data["results"][g]["score"]*100))+"%")
    ids = json_data["results"][g]["location"].split("/")[-1]
    
    if json_data["results"][g]["score"]*100 >= 95:
        favorite_post(ids, username, api)
        os.remove(i)
    else:
        print("\nWarning! Low similarity score!\nThe post was not dowloaded and wasnot added to your favourites on e621!")
        second_json_data = post("https://api.fluffle.xyz/v1/search", headers=headers, files=files, data = {"includeNsfw": True,"platforms": ["fur affinity"],"limit": 8}).json()
        print("Go check " + str(second_json_data["results"][0]["location"]) + "    " + str(round(second_json_data["results"][0]["score"]*100))+ "%")
    image.close()
