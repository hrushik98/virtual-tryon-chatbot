import base64
import requests
import shutil
import uuid
import os
from typing import Optional


def upload_to_github(file_path_or_url: str) -> Optional[str]:
    """Uploads an image file to GitHub and returns the download URL."""
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    REPO = os.getenv("GITHUB_REPO")     
    BRANCH = 'main'  
    COMMIT_MESSAGE = 'Uploading image via Python script'  

    random_filename = str(uuid.uuid4()) + '.png'  

    if file_path_or_url.startswith("http://") or file_path_or_url.startswith("https://"):
        response = requests.get(file_path_or_url)
        if response.status_code == 200:
            FILE_PATH = random_filename
            with open(FILE_PATH, 'wb') as file:
                file.write(response.content)
            print(f"Image successfully downloaded from URL and saved as {FILE_PATH}")
        else:
            print(f"Failed to download image from URL. Status code: {response.status_code}")
            return None
    else:
        shutil.copy(file_path_or_url, random_filename)
        FILE_PATH = random_filename
        print(f"Using local file path: {FILE_PATH}")

    file_name = os.path.basename(FILE_PATH)

    url = f'https://api.github.com/repos/{REPO}/contents/{file_name}'

    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    response = requests.get(url, headers=headers)

    file_sha = None

    if response.status_code == 200:
        file_sha = response.json()['sha']

    with open(FILE_PATH, 'rb') as file:
        content = file.read()

    encoded_content = base64.b64encode(content).decode('utf-8')

    data = {
        'message': COMMIT_MESSAGE,
        'content': encoded_content,
        'branch': BRANCH
    }
    if file_sha:
        data['sha'] = file_sha
    response = requests.put(url, headers=headers, json=data)
    if response.status_code in [200, 201]:
        return response.json()['content']['download_url']
    else:
        print(f"Failed to upload file. Status code: {response.status_code}")
        print(response.json())
        return None
