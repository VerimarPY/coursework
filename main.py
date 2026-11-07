import requests
import os
import time
import json

from dotenv import load_dotenv
from pprint import pprint
from tqdm import tqdm


load_dotenv()


class SaveCatsYandexDisc:
    '''
    Класс создает подписанную картинку с котом и сохраняет на яндекс диск в указанную папку
    Метод create_folder для создания папки, если указанной папки не существует
    Метод file_info сохраняет имя файла и размер в байтах в json и передает методу этот json в метод save_file
    Метод save_file сохраняет полученный файл в папку в указанном формате
    Метод create_file генерирует картинку с переданным текстом на сайте cataas и сохраняет ее в указанную папку
    '''
    yandex_url = 'https://cloud-api.yandex.net'
    cats_url = 'https://cataas.com/cat/says/'

    def __init__(self, token):
        self.headers = {'Authorization': f'OAuth {token}'}

    def create_folder(self, name_folder): 
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

    def file_info(self, name_folder, name_file):
        response = requests.get(f'{self.yandex_url}/v1/disk/resources', 
        params={
            'path': f'{name_folder}/{name_file}'
        },
        headers=self.headers)
        response_json = response.json()
        file_info = {'name': response_json['name'], 'size': f'{response_json['size']} b.'}
        file_json = json.dumps(file_info, indent=4)
        self.save_file(name_folder, name_file, 'json', file_json)

    def save_file(self, folder, name_file, expansion, file):
        response = requests.get(f'{self.yandex_url}/v1/disk/resources/upload',
        params={
            'path': f'{folder}/{name_file}.{expansion}'
        },
        headers=self.headers)
        
        response_put = requests.put(response.json()['href'], file)

        if response_put.status_code == 201:
            print('Файл сохранен успешно')

        else:
            print(f'Ошибка сохранения файла {response_put.status_code}')   

    def create_file(self, name_folder, text):
        print(f'Генерирую картинку с котиком и подписью {text}')
        cats_url = f'{self.cats_url}{text}'
        folder = self.create_folder(name_folder)  

        print(f'Сохраняю полученную картинку на диск {name_folder}')
        response = requests.post(f'{self.yandex_url}/v1/disk/resources/upload',                
        params={
            'url': cats_url,
            'path': f'{folder}/{text}.jpg'
        },
        headers=self.headers
        )

        with tqdm(desc='Загрузка картинки\n', total=None) as progress_bar:

            while True:
                response_status = requests.get(response.json()['href'], headers=self.headers)

                if response_status.json()['status'] == 'success':
                    print(f'Картинка с названием {text} успешно загружена в папку {folder}')
                    break

                elif response_status.json()['status'] == 'in-progress':
                    time.sleep(1)
                    progress_bar.update(1)
                    continue
                

                else:
                    print(f'Не удалось загрузить картинку')
                    break

        info = self.file_info(name_folder, f'{text}.jpg')        


def main():
    text = input('Введите текст:\n')
    token = os.getenv('TOKEN')
    my_item = SaveCatsYandexDisc(token)
    my_item.create_file('PY-162', text)


if __name__ == '__main__':
    main()    