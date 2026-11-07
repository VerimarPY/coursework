import requests
import os
import time

from dotenv import load_dotenv


load_dotenv()


class SaveCatsYandexDisc:
    yandex_url = 'https://cloud-api.yandex.net'
    cats_url = 'https://cataas.com/cat/says/'

    def __init__(self, token):
        self.headers = {'Authorization': f'OAuth {token}'}

    def create_folder(self, name_folder: str) -> str: 
        response = requests.put(f'{self.yandex_url}/v1/disk/resources',
        params={
            'path': name_folder
        }, 
        headers=self.headers
        )
        if response.status_code == 201:
            return name_folder
        
        elif response.status_code == 409:
            return name_folder

        else:
            return f'Ошибка создания папки: {response.status_code}'

    def create_file(self, name_folder:str, text:str) -> str:
        cats_url = f'{self.cats_url}{text}'
        folder = self.create_folder(name_folder)  

        response = requests.post(f'{self.yandex_url}/v1/disk/resources/upload',                
        params={
            'url': cats_url,
            'path': f'{folder}/{text}.jpg'
        },
        headers=self.headers
        )

        while True:
            response_status = requests.get(response.json()['href'], headers=self.headers)

            if response_status.json()['status'] == 'success':
                print(f'Картинка с названием {text} успешно загружена в папку {folder}')
                break

            elif response_status.json()['status'] == 'in-progress':
                time.sleep(1)
                continue

            else:
                print(f'Не удалось загрузить картинку')
                break


def main():
    text = input('Введите текст:\n')
    token = os.getenv('TOKEN')
    my_item = SaveCatsYandexDisc(token)
    my_item.create_file('PY-162', text)


if __name__ == '__main__':
    main()    