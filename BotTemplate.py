import json
from abc import ABC, abstractmethod

class BotTemplate(ABC):
    """АБК бота."""
    user_id=0
    last_message_id=0
    api_url=""
    access_token=""
    path_to_config=""
    isValid=True
    def __init__(self, path_to_config):
        """Стандартная инициализация. На вход принимает путь к json-файлу конфигурации."""
        """Файл конфигурации должен содержать:"""
        """api_url: адресс api бота. Включает протокол."""
        """user_id: id пользователя, целое число"""
        """access_token: токен, строка"""
        """last_message_id: 0 при создании файла, должен изменяться ботом"""
        self.path_to_config=path_to_config
        try:
            open(path_to_config,"r")
        except:
            self.isValid=False
            return None
        with open(path_to_config,"r") as config:
            data=json.load(config)
        self.api_url=data["api_url"]
        self.user_id=data["user_id"]
        self.access_token=data["access_token"]
        self.last_message_id=data["last_message_id"]
        self.postInit()
    @abstractmethod
    def postInit():
        """Метод используется, если боту при инициализации требуется выполнить дополнительные действия"""
        pass
    @abstractmethod
    def getActions():
        """Метод должен возвращать список команд, полученных ботом от администратора."""
        pass
    @abstractmethod
    def sendMessage():
        """Метод отправляет сообщение"""
        pass
