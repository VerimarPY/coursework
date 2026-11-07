import requests
import os

from dotenv import load_dotenv


load_dotenv()


class ApiYandexDisk:
    token = os.getenv('TOKEN')


