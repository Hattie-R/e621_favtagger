import requests


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

def favorite_post(id, USERNAME, API_KEY):
    headers = {'user-agent': 'hydrusBatchSauce/corposim'}
    auth = requests.auth.HTTPBasicAuth(USERNAME, API_KEY)
    requests.post(url="https://e621.net/favorites.json", auth=auth, headers=headers, json={ "post_id": id })

if __name__ == "__main__":
    pass
