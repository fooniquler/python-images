import os
from PIL import Image
import requests
import shutil
from urllib.parse import urlencode
import zipfile


def extract_images():
    zip_path = os.path.join(os.getcwd(), 'images.zip')
    folder_path = os.path.join(os.getcwd(), 'folder')
    os.makedirs(folder_path, exist_ok=True)

    with zipfile.ZipFile(zip_path, 'r') as zip_file:
        zip_file.extractall(folder_path)
    os.remove(zip_path)


def download_images(folder_list: list[str]):
    base_url = 'https://cloud-api.yandex.net/v1/disk/public/resources/download?'
    # public_key = 'https://disk.yandex.ru/d/V47MEP5hZ3U1kg' - download limit exceeded
    public_key = 'https://disk.yandex.ru/d/KjA8LdUE-0vmcw'

    for folder in folder_list:
        final_url = base_url + urlencode(dict(public_key=public_key)) + '&' + urlencode(dict(path=f'/{folder}'))

        response = requests.get(final_url)

        download_url = response.json()['href']

        download_response = requests.get(download_url)

        with open('images.zip', mode='wb') as file:
            file.write(download_response.content)

        extract_images()


def merge_images(folder_list: list[str]):
    images = []

    for folder in folder_list:
        folder_path = os.path.join(os.path.join(os.getcwd(), 'folder'), folder)

        for filename in os.listdir(folder_path):
            img_path = os.path.join(folder_path, filename)
            img = Image.open(img_path)
            images.append(img)

    images[0].save('Result.tif', save_all=True, append_images=images[1:])

    shutil.rmtree(os.path.join(os.getcwd(), 'folder'))


if __name__ == '__main__':
    # Example
    folder_list = ['1369_12_Наклейки 3-D_3', '1388_12_Наклейки 3-D_3']

    download_images(folder_list)
    merge_images(folder_list)
